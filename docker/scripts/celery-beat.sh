#!/bin/sh

# shellcheck disable=SC3010
if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
    LOGLEVEL="CRITICAL"
else
    LOGLEVEL="DEBUG"
fi

echo "Preparing Log File"
if [ ! -f /var/log/celery-beat/info.log ]; then
    touch /var/log/celery-beat/info.log
fi

echo "Running celery beat worker..."
celery -A config beat --loglevel=$LOGLEVEL -f /var/log/celery-beat/info.log
