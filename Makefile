
DEST=_api_responses

WGET_BIN?=wget
WGET_OPT=-q --no-check-certificate --header="Content-Type:application/json"
WGET=$(WGET_BIN) $(WGET_OPT)
WGET_TOKEN=$(WGET) -O $@ --header="X-Session: $(TOKEN)"

API_URL?=https://127.0.0.1:2345
API_LOGIN=$(API_URL)/login
API_PROFILE=$(API_URL)/profile
API_DISCOVER=$(API_URL)/discover
API_PGBADGER_VERSION=$(API_URL)/pgbadger/version

TOKEN_FILE=$(DEST)/token.json
JSON_AUTH={"username": "alice","password": "alice"}

TOKEN=$(shell cat $(TOKEN_FILE) | jq --raw-output .session)



api_discover: $(DEST)/discover.json
api_profile: $(DEST)/profile.json
api_pgbadger_version: $(DEST)/pgbadger_version.json

$(DEST)/discover.json: $(TOKEN_FILE)
	$(WGET_TOKEN) $(API_DISCOVER) -
	cat $@

$(DEST)/profile.son: $(TOKEN_FILE) 
	$(WGET_TOKEN) $(API_PROFILE)
	cat $@


$(DEST)/pgbadger_version.json: $(TOKEN_FILE)
	$(WGET_TOKEN) $(API_PGBADGER_VERSION)
	cat $@
	
api_login: $(TOKEN_FILE)

$(TOKEN_FILE):
	-mkdir $(DEST)
	$(WGET) --post-data '$(JSON_AUTH)' $(API_LOGIN) -O $(TOKEN_FILE)
	TOKEN=$(shell cat $(TOKEN_FILE) | jq --raw-output .session)



#
# Unit test
# 

pytest_prepare: src/pgBadger src/pgBadger-3.3 src/pgBadger-9.0  _tmp/reports _tmp/log/postgresql.log

src/pgBadger:
	git clone --branch 'master' https://github.com/dalibo/pgbadger.git src/pgBadger

src/pgBadger-3.3:
	git clone --branch 'v3.3' https://github.com/dalibo/pgbadger.git src/pgBadger-3.3

src/pgBadger-9.0:
	git clone --branch 'v9.0' https://github.com/dalibo/pgbadger.git src/pgBadger-9.0

_tmp/reports:
	mkdir -p $@ 

_tmp/log/postgresql.log:
	mkdir -p _tmp/log
	bunzip2 -d src/pgBadger/t/fixtures/light.postgres.log.bz2 -c > $@

pytest: pytest_prepare
	python -m pytest --cov=pgbadger tests/unit/ --cov-report term --cov-report html:_cov_html                                           

local_ci:
	gitlab-runner exec docker install_pgbadger
	gitlab-runner exec docker unit-2.7
