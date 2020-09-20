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
        | |___ data/   # ignored by git

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

        export POSTGRES_PASSWORD=<choose a good password>
        export BASE_URL=https://staging.captricity.com

* Build your cluster with

        docker-compose build

* Start your cluster with

        docker-compose up -d

* Once you are done using your cluster, you can shut it down with

        docker-compose rm -sf

* The postgres data is configured to persist at this time-- but, on the first
run locally, you will have to go through the steps to set up the database schema.

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
