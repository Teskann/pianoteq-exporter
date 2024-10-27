# Pianoteq Exporter

Retrieve what you just played in Pianoteq on your Android device.

## Installation

Download the script on the machine running Pianoteq:

```bash
git clone https://github.com/Teskann/pianoteq-exporter
mkdir ~/pianoteq-exports  # Create the folder where the exported wav are stored
```

### Dependencies

```bash
pip install requests
```

### Usage

To see how to use, run:
```commandline
python pianoteq-exporter.py --help
```

## Android Usage

Modify the following script according to your preferences and store it in `~` using [Termux](https://f-droid.org/packages/com.termux/).
```bash
#!/bin/bash

# Variables
REMOTE_USER="piano"
REMOTE_HOST="192.168.1.99"  # URL of your machine running Pianoteq
DESTINATION="/data/data/com/termux/files/home/storage/download/"  # Android Download folder
INDEX=${1:-1}

ssh ${REMOTE_USER}@${REMOTE_HOST} "bash -s" << EOF
    python3 "/home/piano/pianoteq-exporter/pianoteq-exporter.py" --ptq-path "/home/piano/pianoteq/Pianoteq 8" --index-of-midi-to-export ${INDEX}
EOF

# Copy exported wav file
scp ${REMOTE_USER}@${REMOTE_HOST}:/home/piano/pianoteq-exports/* ${DESTINATION}

# Clear exports folder
ssh ${REMOTE_USER}@${REMOTE_HOST} "bash -s" << EOF
    rm /home/piano/pianoteq-exports/*
EOF
```

Assuming you name this file `pianoteq-export.sh`, don't forget to add executable permissions:

```bash
chmod +x ~/pianoteq-export.sh
```

Then, run `~/pianoteq-export.sh`. Once done, you should see a new `.wav` file in the
`Downloads` folder of your Android Device.