### Initial database setup

The current configuration is set to provide persistence of the postgres database.

Once you have started your cluster for the first time, you can enter the postgres container/service
to do the initial setup.  Use the following command while the cluster is running

    docker-compose run postgres bash

This will bring you to a command prompt where you will actually connect to the running database:

    psql -h postgres -U agnostic agnostic

The service (host) is ```postgres``` and the initial user is named ```agnostic``` connecting to 
the database named ```agnostic```.  Remember that inside the cluster, you use the service names
as opposed to things like ```localhost``` or IP addresses.

You will need to enter the password that you established in your environment variables for ```POSTGRES_PASSWORD```
as described in the main README.

Now it is time to create the main table:

    CREATE TABLE events (
        id BIGSERIAL PRIMARY KEY,
        event_name character varying(75),
        action character varying(100),
        status character varying(100),
        user_id integer,
        object_parent_id bigint,
        object_id bigint,
        object_name character varying(1024),
        object_type character varying(100),
        output character varying(1024),
        notes jsonb,
        created_at timestamp with time zone DEFAULT now(),
        modified_at timestamp with time zone
    );

Next, you will want to create a new user/role named ```vidado_serverless``` for connecting to the database from the app:

    CREATE ROLE vidado_serverless LOGIN PASSWORD '<choose your password>';
    GRANT CONNECT ON DATABASE agnostic TO vidado_serverless;
    GRANT USAGE ON SCHEMA public TO vidado_serverless;
    GRANT ALL ON public."events" TO vidado_serverless;
    GRANT USAGE, SELECT ON SEQUENCE events_id_seq to vidado_serverless;

For now, you will probably find it easiest to set the password to the same value as the environment
variable ```POSTGRES_PASSWORD```.

In this mode, you can also run normal SQL queries:

    SELECT * FROM events;
