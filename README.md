# tcrictionary-selfhost

Run a self-hosted instance of TcRictionary using Neo4j and Docker.

## Why run TcRictionary locally?

A local deployment is useful for queries that:

1. Return large result sets that may exceed limits imposed by hosted services.
2. Require complex Cypher logic that is not supported by the web or Python
   interfaces.

For example, advanced analyses that condition on multiple elements of a query
chain are often easier to perform directly against a local Neo4j database.

## Requesting the Dataset

The TcRictionary dataset is not currently publicly available.

To request access, please contact:

**[m.cowley@ucl.ac.uk](mailto:m.cowley@ucl.ac.uk)**

Once access has been granted, place the provided dataset files into the
repository's `data/` directory.

## Prerequisites

Before starting, ensure that you have:

- Installed Docker and Docker Compose. See the
  [Docker documentation](https://docs.docker.com/compose/install/) for
  instructions.
- The TcRictionary dataset available in the `data/` directory

## Launching TcRictionary

The self-hosted deployment is managed entirely through a single Docker Compose
configuration.

From the repository root, run:

```bash
docker compose -f docker/tcrictionary.yml up
```

On first startup, the deployment will automatically:

1. Import the dataset into Neo4j.
2. Create all required database indexes.
3. Launch the Neo4j database.

No separate import step is required.

> **Note**
>
> This deployment also includes
> [Neo4j's APOC (Awesome Procedures on Cypher)](https://neo4j.com/docs/apoc/current/)
> library, which is installed and available by default. APOC procedures and
> functions can be used directly from Cypher queries without any additional
> configuration.

Depending on your hardware and dataset size, the initial import may take several
minutes. Subsequent startups will use the existing database and start much more
quickly.

## Updating the Dataset

The Neo4j database is stored in a Docker volume after the initial import. As a
result, simply replacing the files in `data/` will **not** cause the database to
be rebuilt.

Before updating the dataset, you must stop the deployment and remove the
existing database volume:

```bash
docker compose -f tcrictionary.yml down -v
```

The `-v` flag is important because it removes the persistent Neo4j volume.
Without it, Docker will reuse the existing database and ignore any changes made
to the dataset files.

Once the volume has been removed:

1. Replace the existing dataset files in the `data/` directory with the updated
   versions.
2. Restart TcRictionary:

```bash
docker compose -f tcrictionary.yml up
```

On startup, the database will detect that no existing Neo4j volume is present
and will perform a fresh import of the dataset, recreate all indexes, and launch
the database.

## Using Local TcRictionary

Once the database has started, you can access it in two ways.

### 1. Cypher Shell

Connect directly to the database using Neo4j's Cypher shell:

```bash
docker exec -it <database-container-id> cypher-shell -u neo4j -p ''
```

You can obtain the container ID by running:

```bash
docker ps
```

Queries are written in Cypher. For an introduction to the language, see the
official
[Neo4j Cypher documentation](https://neo4j.com/docs/cypher-manual/current/introduction/).

### 2. Neo4j Browser

Open:

```text
http://localhost:7474/browser/
```

You will be presented with a `:server connect` dialog.

Simply select **Connect** without modifying any fields.

You can then explore and query the database through Neo4j Browser's graphical
interface. See
[documentation for the Neo4j Browser](https://neo4j.com/docs/browser-manual/current/).

### 3. Neo4j Python Driver

TcRictionary can also be accessed programmatically using the Neo4j Python
Driver.

See the official
[Neo4j Python Driver documentation](https://neo4j.com/docs/api/python-driver/current/)
for detailed information.

This interface is recommended for integrating TcRictionary queries into analysis
pipelines, scripts, and larger Python applications.

Example usage is provided in the repository's `examples/` directory. These
examples demonstrate how to connect to the database and execute Cypher queries
from Python.

A typical connection looks like:

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "")
)

with driver.session() as session:
    result = session.run(
        "MATCH (n) RETURN count(n) AS count"
    )

    print(result.single()["count"])

driver.close()
```

For more advanced functionality, including transaction management, connection
pooling, and asynchronous queries, refer to the official Neo4j Python Driver
documentation.
