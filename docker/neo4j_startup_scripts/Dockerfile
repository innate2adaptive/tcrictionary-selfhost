# Dockerfile to index neo4j DB on startup
FROM neo4j:latest

COPY --chmod=755 create-indexes.sh create-indexes.sh
COPY --chmod=755 wrapper.sh wrapper.sh

ENTRYPOINT ["./wrapper.sh"]
