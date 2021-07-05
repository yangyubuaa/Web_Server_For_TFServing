#!/usr/bin/env bash

docker exec -it yangyutorch bash
cd /opt/app/indus-cls-api
cd MultiModel
sh start_tfserving.sh
