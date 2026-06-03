#!/bin/bash

create_index()
{
	echo "CREATE INDEX ON :$1($2);"
	until cypher-shell -u "neo4j" -p "" "CREATE INDEX IF NOT EXISTS FOR (n:$1) ON (n.$2);"
	do
	  echo "create index on ($1) failed, sleeping"
	  sleep 10
	done
	echo "create index on ($1) complete"
}

create_index "VAlpha" "gene"
create_index "VAlpha" "allele"
create_index "JAlpha" "gene"
create_index "JAlpha" "allele"
create_index "Cdr3Alpha" "id"
create_index "VBeta" "gene"
create_index "VBeta" "allele"
create_index "JBeta" "gene"
create_index "JBeta" "allele"
create_index "Cdr3Beta" "id"
create_index "Clone" "cdr3a_nt"
create_index "Clone" "cdr3b_nt"
create_index "Repertoire" "id"
create_index "Individual" "id"
create_index "Study" "id"
create_index "Database" "id"
create_index "MhcA" "gene"
create_index "MhcA" "allele_1"
create_index "MhcA" "allele_2"
create_index "MhcA" "class"
create_index "MhcB" "gene"
create_index "MhcB" "allele_1"
create_index "MhcB" "allele_2"
create_index "MhcB" "class"
create_index "Epitope" "id"
create_index "Species" "id"
