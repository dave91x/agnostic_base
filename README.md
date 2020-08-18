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
* You will need to set some environment variables:

        export VAULT_DEV_ROOT_TOKEN_ID=<choose a nice long alphanumeric string>
        export POSTGRES_PASSWORD=<choose a good password>

* Build your cluster with

        docker-compose build

* Start your cluster with

        docker-compose up -d

* You will need to go in and create any required secrets in Vault.
 You can do this in the web UI provided by Vault:

        http://localhost:8200/ui

* Once you are done using your cluster, you can shut it down with

        docker-compose rm -sf

* The Vault and postgres data should persist at this time

### Things on the horizon
* SSL cert capability for api endpoints
* Additional authentication mechanisms
* Dead Letter Queues (DLQ)
* Dashboards
* Polyglot service discovery functionality
