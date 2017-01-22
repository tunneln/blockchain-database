#!/bin/bash

python2.7 peer.py --name Blumberg --port 9000 --peer-address http://127.0.0.1:9001 &
python2.7 peer.py --name Noel --port 9001 --peer-address http://127.0.0.1:9000 &

python2.7 client.py --name Blumberg --port 9050 --peer-address http://127.0.0.1:9000 &
python2.7 client.py --name Noel --port 9051 --peer-address http://127.0.0.1:9001 &

echo "Press Ctrl+X to push processes to the background"


### THIS IS THE ALTERNATIVE VERSION USING GUNICORN INSTEAD OF FLASK ###
		### ALLOWING THE BLOCKCHAIN TO RUN ON A FULL NETWORK ###
#gunicorn -w 4 -b 0.0.0.0:8000 'peer:start("Blumberg", "http://127.0.0.1:8001")' &
#gunicorn -w 4 -b 0.0.0.0:8001 'peer:start("Noel", "http://127.0.0.1:8000")' &
#gunicorn -w 4 -b 0.0.0.0:8080 'planner:start("Blumberg", "http://127.0.0.1:8000")' &
#gunicorn -w 4 -b 0.0.0.0:8081 'planner:start("Noel", "http://127.0.0.1:8001")'
