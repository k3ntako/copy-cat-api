# CopyCat API

CopyCat is a webapp that allows users to share text and files (currently in development).

This repo hosts the code for CopyCat's backend server. You can find the frontend code in the [k3ntako/copy-cat-web](https://github.com/k3ntako/copy-cat-web) repo.

Production Health Check: <http://copy-cat-api-prod.us-east-1.elasticbeanstalk.com/health>

## Requirements

- PostgreSQL >= 12
- Python >= 3.8

## Getting Started

1. Clone this repo

2. Initialize `venv` (only first time you clone the repo)

   ```
   $ python3 -m venv venv
   ```

3. Start `venv`

   ```
   $ . venv/bin/activate
   ```

4. Install dependencies

   ```
   $ pip install -r requirements.txt
   ```

5. Create database (only first time you clone the repo)

   - Follow the steps in the _Initial Database Setup_ section

6. Set environment variable

   ```
   $ export FLASK_APP=src.copycat:create_app
   ```

7. Run migrations on database

   ```
   $ flask db upgrade
   ```

8. Start flask app

   ```
   $ flask run
   ```

## Testing

Make sure you have installed the dependencies first.

Run the tests:

```
$ pytest
```

## Initial Local Database Setup

Create a local PostgreSQL database with the name `copy_cat`. Make sure it's accessible at `localhost:5432`. One way to create it is by using the [`psql`](https://www.postgresql.org/docs/current/app-psql.html) command line tool as demostrated below.

```
$ psql
$ CREATE DATABASE copy_cat;
```

Unless you deleted the `migrations` directory, you can ignore this step. A `migrations` directory will be present in the root directory of this project, but if it does not exist, you will need to run the following commands to create the migrations.

```
$ export FLASK_APP=src.copycat:create_app
$ flask db init
$ flask db migrate
$ flask db upgrade
```

## Initial Deploy to AWS Elastic Beanstalk

1.  Assume role for AWS role for deploying.

2.  Create database using Terraform

    - Make sure to change anything inside brackets (`[]`) below.

    ```
    $ export TF_VAR_RDS_USERNAME=[database username]
    $ export TF_VAR_RDS_PASSWORD=[database password]
    $ export TF_VAR_RDS_PORT=[database port]
    $ TF_VAR_RDS_DB_NAME=[database name]
    $ terraform init
    $ terraform apply
    ```

3.  Save database config as secret

    - If you have an existing password for your secrets set it as an environment variable. If left blank, it will generate and print it out.

    ```
    $ export SECRETS_KEY=[secret password]
    ```

    - After deploying the database using Terraform, you should see an output in the console that starts with `rds_hostname =`. Copy the URL after the `=` (RDS endpoint), and set it as an environment variable as shown below (replace the bracket (`[]`) and everything inside with the URL).

    ```
      $ export RDS_HOSTNAME=[RDS enpoint]
      $ python3 ./src/utilities/encrypt_secrets.py
    ```

    - Double check that the output looks correct.
    - If the password is new or it has changed save it to 1Password and deploy it to the environment.

    ```
    $ eb setenv=[secret password]
    ```

4.  Initialize application

    ```
    $ eb init
    ```

5.  Create environment

    ```
    $ eb create
    ```

6.  Once Elastic Beanstalk is done deploying, you will need to allow the environment to access the database.
    - Determine the Elastic Beanstalk Environment's Security Group ID. Under the "Configuration" page, click the "Edit" button next to "Instances". It should start with `sg-`.
    - Go to the [RDS console](https://console.aws.amazon.com/rds/home) and find the database created by Terraform.
    - Inside the "Connectivity & security" tab, click on the "VPC security groups" link.
    - Under the "Actions" dropdown, click "Edit inbound rules".
    - Click "Add rule".
    - Set the "Type" to "PostgreSQL".
    - Start typing the Elastic Beanstalk enviornment's Security Group into the input under "Source" and select the one for the current environment.
    - Click "Save rules".
    - More on this [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/rds-external-defaultvpc.html).

## Deploy New Version to Production

1. Assume role for AWS role for deploying.

2. Deploy the last commit. Anything that is not committed will not be deployed.

   ```
   $ eb deploy
   ```
