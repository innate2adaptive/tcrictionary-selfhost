FROM neo4j:latest

# Disable auth
ENV NEO4J_AUTH=none

# Import data
COPY data/ /import
RUN neo4j-admin database import full --nodes /import/nd* --relationships /import/rl* --overwrite-destination=true

# Index data
COPY --chmod=755 docker/neo4j_startup_scripts/create-indexes.sh create-indexes.sh
RUN set -m && \
    /startup/docker-entrypoint.sh neo4j & \
    bg_pid=$! && \
    sleep 10 && \
    ./create-indexes.sh && \
    kill $bg_pid
