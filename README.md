# Python Packet Sniffer and Parser for Lineage 2 Revolution RX Packets

Still a lot to be done. Putting this in a repo in case others want to lend a hand.

## Requirements

- Python3
- put this in a python virtualenv if you are not lazy
- if you want to work on adding KaiTai structs you will need the compiler. More info at kaitai.io.

## Installation & Usage

1. Build this with `python3 setup.py build install` or however you like to build python projects. I havnt actually tested the setup.py file but I assume it works. Will get to it later if it doesnt, there are not many dependencies to pip3 install if the setup.py is no good.

2. Simply run `python3 l2rsniff.py` to get going. On start you will see the sniffer start up and spit out what it can make sense of.
	- tool listens to all interfaces (TODO make it configurable via cli param)
	- tool is hardcoded to the Windawood03 server IP (TODO allow this to be a cli param as well)
	- tool is coded to kill the process once it gets data (debug / development; easily taken out)

3. Once tool is running open your emulator of choice and start L2R. Currently only parser is for Guild Member List data.
	- navigate to you clan page and click on your clan, then on the members tab.
	- go back to the terminal this tool is running in and you will see data

### TODOS

	Most ToDos are in the l2rsniff.py file but here are some QoL points.
	
	- add usercallback feature via function decorator on the main_pkt_handler so a user can define what to do with parsed data
	- provide functions for pumping data to csv? or anything else really
	- implement threading (high priority)
	- add more parser definitions
	- flesh out the terminal parameters for easier use.
	- better logging of tracebacks during try/except


### Resources


	- L2R clannies I dont want to say who
	- this repo: https://github.com/AngryHank - kinda.
