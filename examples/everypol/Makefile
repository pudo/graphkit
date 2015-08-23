GK=graphkit --debug -c config.json

all: tmp/sa.json tmp/anc_members.json tmp/de.nq

clean:
	rm -rf tmp

# South Africa:
tmp/anc_members.json: tmp/sa.nq
	$(GK) query -i tmp/sa.nq -f anc_query.json -o tmp/anc_members.json

tmp/sa.json: tmp/sa.nq
	$(GK) dump-json -i tmp/sa.nq -t persons -t organizations -o tmp/sa.json

tmp/sa.nq: tmp/sa.csv
	$(GK) load-csv -x urn:everypol:sa -m mapping.json -o tmp/sa.nq tmp/sa.csv

tmp/sa.csv:
	curl -o tmp/sa.csv https://cdn.rawgit.com/everypolitician/everypolitician-data/00f0221/data/South_Africa/Assembly/term-26.csv


# Germany
tmp/de.nq: tmp/de-17.nq tmp/de-18.nq
	$(GK) merge -i tmp/de-17.nq -i tmp/de-18.nq -o tmp/de.nq

tmp/de-17.nq: tmp/de-17.csv
	$(GK) load-csv -x urn:everypol:de:17 -m mapping.json -o tmp/de-17.nq tmp/de-17.csv

tmp/de-18.nq: tmp/de-18.csv
	$(GK) load-csv -x urn:everypol:de:18 -m mapping.json -o tmp/de-18.nq tmp/de-18.csv

tmp/de-17.csv:
	curl -o tmp/de-17.csv https://cdn.rawgit.com/everypolitician/everypolitician-data/a915dbd/data/Germany/Bundestag/term-17.csv

tmp/de-18.csv:
	curl -o tmp/de-18.csv https://cdn.rawgit.com/everypolitician/everypolitician-data/a915dbd/data/Germany/Bundestag/term-18.csv
