GK=graphkit --debug -c config.yaml

all: tmp/data.json

tmp/data.json: tmp/term-26.nq
	$(GK) to-json -i tmp/term-26.nq -o tmp/data.json

tmp/term-26.nq:
	$(GK) load-csv -x urn:everypol:southafrica -m mapping.json -o tmp/term-26.nq term-26.csv

clean:
	rm -rf tmp/term-26.nq
	rm -rf tmp/data.json
