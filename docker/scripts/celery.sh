#!/bin/sh

# shellcheck disable=SC3010
if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
    LOGLEVEL="CRITICAL"
else
    LOGLEVEL="DEBUG"
fi

echo "Preparing Log File"
if [ ! -f /var/log/celery/info.log ]; then
    touch /var/log/celery/info.log
fi

echo "Running celery worker..."
celery -A config worker --loglevel=$LOGLEVEL -f /var/log/celery/info.log
