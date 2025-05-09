#!/usr/bin/env bash
set -e

BASE_DIR=$(dirname $(dirname $(realpath $0)))
#echo $BASE_DIR

source "$BASE_DIR"/.env

PGPASSWORD="$DB_DEFAULT_PWD" createdb -h "$DB_DEFAULT_HOST" -p "$DB_DEFAULT_PORT" -U postgres "$DB_DEFAULT_NAME" 2> /dev/null || echo "database already exists"
