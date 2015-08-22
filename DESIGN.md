Notes on the design of the library collection around graphkit.


## Next Steps

* More complex processing graphs
* Implement mapping steps

## Pipeline

config:
    store:
        type: iomemory

steps:
    - step: csv-read
      source: http://...

    - step: json-map
      mapping:
        ...

    - step: rdf-load
      context: foo

    - step: rdf-dedupe

    - step: rdf-compact

    - step: mql-query
      context: ...

steps:
  read:
    step: csv-read


## Pipe stages

$ graphpipe mygraph.yaml

* ``readcsv``: None -> dict
* ``readtable``: None -> dict
* ``map``: dict -> dict
* ``load``: dict -> uri
* ``dedupe``: uri -> uri
* ``sparql``: uri -> dict
* ``mql``: uri -> dict
* ``dump``: uri -> None
* ``unmap``: dict -> dict
* ``writecsv``: dict -> None


## Stardog + rdflib:

https://lawlesst.github.io/notebook/rdflib-stardog.html
https://gist.github.com/lawlesst/9996cf3050c019a8d5ee


## Goto locations

http://json-schema.org/latest/json-schema-validation.html
https://github.com/json-schema/json-schema
https://github.com/Julian/jsonschema/blob/master/jsonschema/validators.py
