#!/usr/bin/env sh
set -eu

#envsubst '${DOMAIN_NAME}' < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf

exec "$@"
