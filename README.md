# graphkit

[![Build Status](https://travis-ci.org/pudo/graphkit.svg?branch=master)](https://travis-ci.org/pudo/graphkit)

Handle the processing and conversion of data based on [JSON
schema](http://json-schema.org/) specifications. This includes the ability to
traverse an object graph together with the associated schema, and to map flat
data structures into a JSON object graph based on a mapping.

## README as it should be

GraphKit is a pipeline processing tool for graph-based data extraction,
transformation and analysis. The tool's graph model is based on annotated
[JSON schema](http://json-schema.org/) definitions.

A typical pipeline might extract data from a set of CSV files or database
tables, translate them to JSON using a given schema, combine them into an
RDF graph, perform de-duplication and data integration, and eventually run
a set of queries on the resulting graph.

## Stages

The following stages / operations should be supported in the graph processing
pipeline:

* ``csv:read``: Generate an iterator from a CSV file.
* ``readtable``: Generate an iterator from a SQL database table.
* ``json:map``: Apply a JSON schema mapping to the data coming from a source.
* ``rdf:load``: Import the data from a JSON stream into a triple store.
* ``rdf:dedupe``: Apply sameAs mappings based on some external mapping file.
* ``rdf:sparql``: Run a SPARQL query.
* ``mql:query``: Run an MQL query.
* ``rdf:dump``: Export RDF data to a file.
* ``json:unmap``: Apply a JSON schema mapping to convert objects to a flat table.
* ``csv:write``: Export data to a CSV file.

## JSON Schema Mapping

To link flat data structures to nested object graphs matching JSON schema
definitions, a mapping language is supported to define how the columns of
a source table are meant to be applied to the fields of a JSON schema.

See [here](https://github.com/pudo/graphkit/blob/master/tests/fixtures/everypol/mapping.json)
for an example.

The format allows mapping nested structures, including arrays. It also supports
the application of very basic data transformation steps, such as generating a
URL slug or hashing a column value.

## Tests

The test suite will usually be executed in it's own ``virtualenv`` and perform a
coverage check as well as the tests. To execute on a system with ``virtualenv``
and ``make`` installed, type:

```bash
$ make test
```
