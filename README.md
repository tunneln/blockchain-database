# Blockchain Database
An extremely barebones implementation of a blockchain database network made for
practice and learning purposes.

A detailed overview of Blockchain Databases can be foundin my short paper [here](https://www.cs.utexas.edu/~noel/Blockchain.pdf) or simply found in the repo

###What it can do:
	* The blockchain is interfaced to via the netowrk
	* The blockchains are self-verifiable
	* Two blockchain instances can be connected to act as a "peer-to-peer" netowrk
	* The ledger can be pickled into a json so that it can be stored or
		broadcasted over the network
	* A redis store acts as a buffer for peers to read the updated blockchain
	* The code is heavily modular, so it can also function as an API

###What it can't do:
	* None of the passthrough or nodes' identities are encrypted
	* Data is easily read in the form of json docs
	* No real peer-2-peer networking with broadcasting is implemented
	* This database is not Byzantine Fault Tolerant as it does not implement a
		consensus algorithm, so block forks could occur.

A proof-of-work algorithm is also not implemented for appending new blocks due to the
	nature of this implentation

###How to play with it:
run `$./run.sh`

You can now run the outputted url in a browser
Actions are invoked via POST and GET requests (by url extensions or using curl)
see code for descriptions of each request and it's corresponding action

Acknowledgement: Nothing in the 'static' folder was made by me

###REQUIRED LIBRARIES:
* requests
* click
* Flask (or gunicorn, see run.sh)
* redis

To resolve all dependency issues:

`$ pip install requests click Flask redis`

If you don't have pip:

```
$ wget https://bootstrap.pypa.io/get-pip.py

$ python2.7 get-pip.py
```


