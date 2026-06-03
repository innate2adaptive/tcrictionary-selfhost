#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
/startup/docker-entrypoint.sh neo4j &

echo "Waiting for neo4j to start..."
sleep 10

# Start the helper process
./create-indexes.sh

# now we bring the primary process back into the foreground
# and leave it there
fg %1
