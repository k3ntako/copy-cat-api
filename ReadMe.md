# CopyCat API

CopyCat is a webapp that allows users to share text and files (currently in development).

This repo hosts the code for CopyCat's backend server. You can find the frontend code in the [k3ntako/copy-cat-web](https://github.com/k3ntako/copy-cat-web) repo.

Production Health Check: <http://copy-cat-api-prod.us-east-1.elasticbeanstalk.com/health>

## Requirements

- PostgreSQL >= 12
- Python >= 3.8

## Getting Started

1. Clone this repo

2. Install dependencies

```
$ pip install -r requirements.txt
```

2. Start `venv`

```
$ . venv/bin/activate
```

3. Set environment variable

```
$ export FLASK_APP=src.copycat:create_app
```

4. Setup database

```
$ flask db upgrade
```

5. Start flask app

```
$ flask run
```

## Testing

Run the tests:

```
$ pytest
```

## Initial Database Setup

Create a database locally.

```
$ psql
$ CREATE DATABASE copy_cat;
```

If there is no `migrations` directory in the root of this directory, you will need to run the following to create the migrations.

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
