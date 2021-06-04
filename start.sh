#!/bin/bash

flask db upgrade
waitress-serve --port=5000 --call copycat:create_app