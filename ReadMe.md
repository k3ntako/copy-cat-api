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

Create local PostgreSQL databases: `copy_cat` and `copy_cat_testing`. Make sure it's accessible at `localhost:5432`. One way to create it is by using the [`psql`](https://www.postgresql.org/docs/current/app-psql.html) command line tool as demostrated below.

```
$ psql -c 'CREATE DATABASE copy_cat;'
$ psql -c 'CREATE DATABASE copy_cat_testing;'
```

Unless you deleted the `migrations` directory, you can ignore this step. A `migrations` directory will be present in the root directory of this project, but if it does not exist, you will need to run the following commands to create the migrations.

```
$ export FLASK_APP=src.copycat:create_app
$ flask db init
$ flask db migrate
$ flask db upgrade
```

## Initial Deploy to AWS Elastic Beanstalk

You probably do not need to follow these steps.

1.  Assume role for AWS role for deploying.

2.  Initialize application

    ```
    $ eb init
    ```

3.  Create environment

    ```
    $ eb create
    ```

4.  Create database using Terraform

    - Change anything inside brackets (`[]`) below.

    ```
    $ export TF_VAR_RDS_USERNAME=[database username]
    $ export TF_VAR_RDS_PASSWORD=[database password]
    $ export TF_VAR_RDS_PORT=[database port]
    $ TF_VAR_RDS_DB_NAME=[database name]
    $ terraform init
    $ terraform apply
    ```

    - After deploying the database using Terraform, you should see an output in the console that starts with `rds_hostname =`. You will need the URL after the `=` (RDS hostname) in the next step.

5.  Save secrets in repo.

    - Create JSON in root directory called: `decrypted-secrets-[env].json`. Change `[env]` with environment (`prod`, `dev` or `testing`).
    - Update the JSON with the secrets (get the `RDS_HOSTNAME` from the previous step):

    ```
    {
       "RDS_USERNAME": [username],
       "RDS_PASSWORD": [password],
       "RDS_HOSTNAME": [hostname],
       "RDS_PORT": [port],
       "RDS_DB_NAME": [db name],
    }
    ```

    - Follow the steps in `Update Secrets File` below to encrypt the secrets.

6.  Once Elastic Beanstalk is done deploying, you will need to allow the environment to access the database.
    - Determine the Elastic Beanstalk Environment's Security Group ID. Under the "Configuration" page, click the "Edit" button next to "Instances". It should start with `sg-`.
    - Go to the [RDS console](https://console.aws.amazon.com/rds/home) and find the database created by Terraform.
    - Inside the "Connectivity & security" tab, click on the "VPC security groups" link.
    - Click the "Actions" dropdown and select "Edit inbound rules".
    - Click "Add rule".
    - Set the "Type" to "PostgreSQL".
    - Start typing the Elastic Beanstalk enviornment's Security Group into the input under "Source" and select the one for the current environment.
    - Click "Save rules".
    - Restart the Elastic Beanstalk server.
    - More on this [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/rds-external-defaultvpc.html).

## Deploy New Version to Production

1. Assume role for AWS role for deploying.

2. Deploy the last commit. Anything that is not committed will not be deployed.

   ```
   $ eb deploy
   ```

3. If there were Terraform changes, make sure to apply them:
   ```
   $ terraform apply
   ```

## Update Secrets File

1. Decrypt existing secrets. Skip if no secrets exist for the environment.

   - Replace `[env]` with environment: `prod`, `dev`, or `testing`.
   - Replace `[password]` with the password found in 1Password.

   ```
     $ python3 ./src/utilities/decrypt_secrets.py [env] [password]
   ```

   - There will be a newly generated file called `decrypted-secrets-prod.json` in the root directory. It is ignored by git, so it might be a bit harder to find.

2. Update the JSON file with new environment variables (case sensitive).

3. Encrypt the env variables. Make sure to use the env and password from 1Password.

   ```
   $ python3 ./src/utilities/encrypt_secrets.py [env] [password]
   ```

   - Confirm that the output looks correct.

4. If the password has changed save it to 1Password.

   - If the password for production is new, make sure to update the environment variable:

   ```
   $ eb setenv SECRETS_KEY=[password]
   ```

5. Commit the encrypted file and do NOT commit the decrypted file.
