#!/bin/sh

# shellcheck disable=SC2039
if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
    LOGLEVEL="CRITICAL"
else
    LOGLEVEL="DEBUG"
fi

echo "Creating Log File"
if [ ! -f /var/log/celery-beat/info.log ]; then
    touch /var/log/celery-beat/info.log
fi

echo "Running celery beat worker..."
celery -A config beat --loglevel=$LOGLEVEL -f /var/log/celery-beat/info.log
