# Agnostic Appliance

### Disclaimer
* This code is currently in development.
* **Do not use this for any production workflow!**

### Overview
This appliance can be installed anywhere Docker containers will run.

### Quick Start
* Ensure that you have Docker and Docker Compose installed on your local machine
* Create a project directory.
* Clone this repo into your project directory.
* Create any of the missing "empty" directories.  Your project directory
should now look like this:

        .
        |___ app_src/
        | |___ queue_reader.py
        | |___ requirements.txt

        |___ certs/
        | |___ README.md

        |___ datastore/
        | |___ conf/
        | | |___ README.md
        | | |___ postgres.conf
        | |___ data/

        |____vault
        | |___ config/
        | | |___ vault-config.json
        | |___ data/
        | |___ logs/
        | |___ policies/

        |___ web_src/
        | |___ event_web.py
        | |___ queue_writer.py
        | |___ requirements.txt

        |___ .dockerignore
        |___ .gitignore
        |___ docker-compose.yml
        |___ Dockerfile_app
        |___ Dockerfile_web
        |___ README.md

* You will need to set some local environment variables:

        export VAULT_DEV_ROOT_TOKEN_ID=<choose a nice long alphanumeric string>
        export VAULT_ADDR=http://0.0.0.0:8200
        export VAULT_API_ADDR=http://0.0.0.0:8200
        export POSTGRES_PASSWORD=<choose a good password>
        export VAULT_ROLE_ID=<established role id for accessing vault secrets>
        export VAULT_SECRET_ID=<established secret id for accessing vault secrets>
        export BASE_URL=https://staging.captricity.com

* **NOTE:**  you should only set the ```VAULT_DEV_ROOT_TOKEN_ID``` if you are
planning to run Vault in dev mode (which is an in-memory mode, meaning you 
have to reload your secrets every time you restart).  You would also need to put
this in the ```docker-compose.yml``` file under the vault service environment
section.  Also, if you want to run vault in dev mode, in the ```docker-compose.yml``` file,
change the ```command``` line in the vault service from 

        command: vault server -config=/vault/config/vault-config.json
        
    to this

        command: vault server -dev

* Build your cluster with

        docker-compose build

* Start your cluster with

        docker-compose up -d

* You will need to go in and create any required secrets in Vault.
 You can do this in the web UI provided by Vault:

        http://localhost:8200/ui

* Once you are done using your cluster, you can shut it down with

        docker-compose rm -sf

* The Vault and postgres data is configured to persist at this time-- but, on the first
run locally, you will have to go through the steps to initialize and unseal the vault,
along with setting up the database schema.

### Mac OSX Docker Desktop "fix" for redis container
If you are running Docker Desktop on Mac OSX, after you start Docker Desktop, but **before**
you start your full cluster, you will want to execute the following in the terminal:

    docker run -ti --privileged ubuntu /bin/bash

This will drop you into a bash shell in an Ubuntu container, where you will do:

    echo never | tee /sys/kernel/mm/transparent_hugepage/enabled
    echo never | tee /sys/kernel/mm/transparent_hugepage/defrag
    exit

If you have to restart Docker Desktop (or your machine), you will need to do this again.

### Things on the horizon
* Initial database schema
* SSL cert capability for api endpoints
* Additional authentication mechanisms
* Dead Letter Queues (DLQ)
* Dashboards
* Polyglot service discovery functionality
