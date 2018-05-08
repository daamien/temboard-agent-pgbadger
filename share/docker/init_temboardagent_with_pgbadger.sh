

# Install plugin from source
pip install -e /usr/local/src/temboard-agent/

# activate the config
cp /usr/local/src/temboard-agent/share/pgbadger.conf /etc/temboard-agent/temboard-agent.conf.d/

# fetch pgBadger from the PGDG repo
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
apt-get update && apt-get install -y lsb-release wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt-get update && apt-get install pgbadger -y

# reload temboard-agent
temboard-agent
