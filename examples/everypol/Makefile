GK=graphkit --debug -c config.json

all: tmp/sa.json tmp/anc_members.json

tmp/anc_members.json: tmp/sa.nq
	$(GK) query -i tmp/sa.nq -f anc_query.json -o tmp/anc_members.json

tmp/sa.json: tmp/sa.nq
	$(GK) dump-json -i tmp/sa.nq -t persons -t organizations -o tmp/data.json

tmp/sa.nq: tmp/sa.csv
	$(GK) load-csv -x urn:everypol:sa -m mapping.json -o tmp/sa.nq tmp/sa.csv

tmp/sa.csv:
	curl -o tmp/sa.csv https://cdn.rawgit.com/everypolitician/everypolitician-data/00f0221/data/South_Africa/Assembly/term-26.csv

clean:
	rm -rf tmp
