#!/bin/sh

set -e

envsubst '${API_HOST},${API_PORT}' < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'