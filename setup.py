from setuptools import setup
    
setup(
    name= "pgbadger",
    version="0.1.0",
    entry_points={
        'temboardagent.plugins' : [
            'pgbadger = pgbadger:pgbadgerPlugin'
        ],
    },
)
