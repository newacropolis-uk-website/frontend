#!/bin/bash
set +e

ENV=development
www_dir="www-$ENV"

port=5100

if [ ! -z "$1" ]; then
    www_dir="www-$1"
    cd $www_dir
    port="$(python app/config.py -e $1)"

    ENV=$1
fi

# kill any existing services running on port
# fuser -k -n tcp $port

echo "hosting on $www_dir"

python main.py runserver --port $port

if [ $www_dir != "www" ]; then
    exit 0
fi
