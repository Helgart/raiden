#!/bin/sh

docker build -t raiden ./nginx
docker run --name raiden -ti -p 80:80
