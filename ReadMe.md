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

Run the tests:

```
$ pytest
```

## Initial Database Setup

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

1. Assume role for AWS role for deploying.

2. Initialize application

   ```
   $ eb init
   ```

3. Create environment

   ```
   $ eb create
   ```

4. Go AWS console and add a Postgres database.

   - Select application's environment
   - Go to "Configuration"
   - Scroll to bottom and click "Edit" next to "Database"
   - Set the Postgres config and click "Apply"

5. Set the environment variable for configuration

   ```
   eb setenv APP_CONFIG=config.ProductionConfig
   ```

## Deploy New Version to Production

1. Assume role for AWS role for deploying.

2. Deploy the last commit. Anything that is not committed will not be deployed.

   ```
   $ eb deploy
   ```
