#!/bin/sh
# Use sh instead of bash for maximum compatibility

# Simple logging function
echo "[$(date)] Starting entrypoint script"

# Wait for PostgreSQL if configured
if [ "$DB_DEFAULT_NAME" = "postgres" ]; then
  echo "[$(date)] Waiting for PostgreSQL at $DB_DEFAULT_HOST:$DB_DEFAULT_PORT..."
  
  while ! nc -z $DB_DEFAULT_HOST $DB_DEFAULT_PORT 2>/dev/null; do
    sleep 1
  done
  
  echo "[$(date)] PostgreSQL is available"
fi

# Wait for Redis if configured
if [ "$REDIS_HOST" ]; then
  echo "[$(date)] Waiting for Redis at $REDIS_HOST:$REDIS_PORT..."
  
  while ! nc -z $REDIS_HOST $REDIS_PORT 2>/dev/null; do
    sleep 1
  done
  
  echo "[$(date)] Redis is available"
fi

# Change to application directory
cd /code/app/

# Always run migrations
echo "[$(date)] Running database migrations"
python manage.py migrate
echo "[$(date)] Database migrations completed"

# Collect static files in production mode
if [ "$DEBUG" = "False" ] || [ "$DEBUG" = "false" ] || [ "$DEBUG" = "0" ]; then
  echo "[$(date)] Collecting static files"
  python manage.py collectstatic --noinput
  echo "[$(date)] Static files collected"
fi

# Execute the command passed to docker
echo "[$(date)] Executing command: $@"
exec "$@"