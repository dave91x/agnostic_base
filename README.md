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
        export VAULT_ADDR=http://0.0.0.0:8200
        export POSTGRES_PASSWORD=<choose a good password>

* Note that you should only set the ```VAULT_DEV_ROOT_TOKEN_ID``` if you are 
planning to run Vault in dev mode (which is an in-memory mode, meaning you 
have to reload your secrets every time you restart).  You would also need to put
this in the ```docker-compose.yml``` file under the vault service environment
section.

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
