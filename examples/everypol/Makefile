GK=graphkit --debug -c config.json

all: tmp/data.json tmp/anc_members.json

tmp/anc_members.json: tmp/term-26.nq
	$(GK) query -i tmp/term-26.nq -f anc_query.json -o tmp/anc_members.json

tmp/data.json: tmp/term-26.nq
	$(GK) dump-json -i tmp/term-26.nq -t persons -t organizations -o tmp/data.json

tmp/term-26.nq:
	$(GK) load-csv -x urn:everypol:southafrica -m mapping.json -o tmp/term-26.nq term-26.csv

clean:
	rm -rf tmp
