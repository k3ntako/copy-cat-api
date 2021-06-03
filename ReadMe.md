# CopyCat API

## Requirements

- PostgreSQL >= 13
- Python >= 3.9

## Getting Started

1. Clone this repo
2. Start `venv`

```
$ . venv/bin/activate
```

2. Install dependencies

```
$ pip install -r requirements.txt
```

3. Set environment variable

```
$ export FLASK_APP=copycat
```

4. Setup database

```
$ flask db init
$ flask db migrate
$ flask db upgrade
```

5. Start flask app

```
$ flask run
```
