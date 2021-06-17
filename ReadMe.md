# CopyCat API

CopyCat is a webapp that allows users to share text and files (currently in development).

This repo hosts the code for CopyCat's backend server. You can find the frontend code in the [k3ntako/copy-cat-web](https://github.com/k3ntako/copy-cat-web) repo.

Production Health Check: <http://copy-cat-api-prod.us-east-1.elasticbeanstalk.com/health>

## Requirements

- PostgreSQL >= 12
- Python >= 3.8

### Deployment Tools

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)
- [Terraform CLI](https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/aws-get-started)

## Getting Started Locally

1. Clone this repo

   ```
   $ git clone https://github.com/k3ntako/copy-cat-api.git
   $ cd copy-cat-api
   ```

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

   - Follow the steps in the _Initial Local Database Setup_ section

6. Start flask app

   ```
   $ flask run
   ```

7. Go to `localhost:5000/health` to confirm that the status is `"UP"`.

## Testing

Make sure you have installed the dependencies and setup the database first.

Run the tests:

```
$ pytest
```

### Test Coverage

```
$ pytest --cov=src tests/
```

## Initial Local Database Setup

Create local PostgreSQL databases: `copy_cat` and `copy_cat_testing`. Make sure it's accessible at `localhost:5432`. One way to create it is by using the [`psql`](https://www.postgresql.org/docs/current/app-psql.html) command line tool as demonstrated below:

```
$ psql -c 'CREATE DATABASE copy_cat;'
$ psql -c 'CREATE DATABASE copy_cat_testing;'
```

Unless you deleted the `migrations` directory, you can ignore this step.

- This step is not required for applying the migrations to the database. It will be applied when the server starts.
- A `migrations` directory will be present in the root directory of this project, but if it does not exist, you will need to run the following commands to create the migrations.

```
$ export FLASK_APP=src.copycat:create_app
$ flask db init
$ flask db migrate
$ flask db upgrade
```

## Initial Deploy to AWS Elastic Beanstalk

1. If you haven't already, create a user and role for this project. Follow the instruction in _Setup AWS User and Role_ section below.

2. Assume the role by following the instructions in _Assume Role_ section below.

3. Initialize Elastic Beanstalk application

   ```
   $ eb init
   ```

4. Create Elastic Beanstalk environment

   ```
   $ eb create
   ```

5. Create database using Terraform

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

6. Save secrets in repo.

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

7. Once Elastic Beanstalk is done deploying, you will need to allow the environment to access the database.
   - Determine the Elastic Beanstalk Environment's Security Group ID. Under the "Configuration" page, click the "Edit" button next to "Instances". It should start with `sg-`.
   - Go to the [RDS console](https://console.aws.amazon.com/rds/home) and find the database created by Terraform.
   - Inside the "Connectivity & security" tab, click on the "VPC security groups" link.
   - Click the "Actions" dropdown and select "Edit inbound rules".
   - Click "Add rule".
   - Set the "Type" to "PostgreSQL".
   - Start typing the Elastic Beanstalk environment's Security Group into the input under "Source" and select the one for the current environment.
   - Click "Save rules".
   - Restart the Elastic Beanstalk server.
   - More on this [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/rds-external-defaultvpc.html).

## Deploy New Version to Production

1.  Assume the role by following the instructions in _Assume Role_ section below.

2.  Deploy the last commit. Anything that is not committed will not be deployed.

    ```
    $ eb deploy
    ```

3.  If there were Terraform changes, make sure to apply them.

    - You will be asked for the credentials for the database. You can find them how to decrypt the file in _Update Secrets File_.

    ```
    $ terraform apply
    ```

## Update Secrets File

1. Decrypt existing secrets. Skip if no secrets exist for the environment.

   - Replace `[env]` with environment: `prod`, `dev`, or `testing`.
   - Replace `[password]` with the password found in 1Password.

   ```
     $ python3 ./src/utilities/decrypt_secrets.py --env [env] --key [password]
   ```

   - There will be a newly generated file called `decrypted-secrets-prod.json` in the root directory. It is ignored by git, so it might be a bit harder to find.

2. Update the JSON file with new environment variables (case sensitive).

3. Encrypt the env variables. Make sure to use the env and password from 1Password.

   ```
   $ python3 ./src/utilities/encrypt_secrets.py --env [env] --key [password]
   ```

   - Confirm that the output looks correct.

4. If the password has changed save it to 1Password.

   - If the password for production is new, make sure to update the environment variable:

   ```
   $ eb setenv SECRETS_KEY=[password]
   ```

5. Commit the encrypted file and do NOT commit the decrypted file.

## Migrations

If you have made a change to a database model, make sure to create the migrations.

- When the server starts, it will run the migrations.

```
$ flask db migrate
```

## Setup AWS User and Role

1. Create a new AWS user in the [AWS console](https://console.aws.amazon.com/iam/home)

   - More on how to assume role: <https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/>

2. Login as the user in AWS CLI

   ```
   $ aws configure
   ```

3. Create a role with `sts:AssumeRole` permission

   - Attach this role to the the user from above

4. Create another role

   - Give it all the permissions required (e.g., Elastic Beanstalk, S3, and/or RDS)

5. Assume role by following the directions in _Assume Role_.

## Assume Role

1. Assume role for AWS role for deploying.

   - Retrieve the credentials for the session. For the role ARN go to the IAM page in the AWS Console.

   ```
   $ aws sts assume-role --role-arn "[AWS role ARN]" --role-session-name AWSCLI-Session
   ```

   - Export the credentials as environment variables:

   ```
   $ export AWS_ACCESS_KEY_ID=[Access Key Id]
   $ export AWS_SECRET_ACCESS_KEY=[Secret Access Key]
   $ export AWS_SESSION_TOKEN=[Session Token]
   ```
