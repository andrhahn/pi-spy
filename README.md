# pi-spy

Python motion detector for Raspberry Pi

Currently tested on RPI 3 Model B

Requires RPI camera module

[Client documentation](client/README.md)
[Server documentation](server/README.md)

### Getting Started

##### Setup
    sudo apt update
    
    sudo apt full-upgrade
    
    sudo pip install picamera
    
##### Run client
    cd client

    python detect_motion.py

##### Run server
    cd server

    python server.py
    
### License

[The MIT License](http://opensource.org/licenses/MIT)
