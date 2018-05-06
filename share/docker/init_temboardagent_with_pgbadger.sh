
pip install -e /usr/local/src/temboard-agent/

cp /usr/local/src/temboard-agent/share/pgbadger.conf /etc/temboard-agent/temboard-agent.conf.d/

apt-get update && apt-get install pgbadger -y

temboard-agent
