
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
