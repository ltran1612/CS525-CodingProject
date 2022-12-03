# CS525-CodingProject

## Description
The goal of this project is to implement 3 modes of block cipher learned in class, namely CBC, OFB, and CRT. Then, we need to compare their performance. 

## How to run
### Install pycryptodome

    pip install pycryptodome

### Run the program
Step 0.1: Get into the folder python (Assuming that you are inside the root of the git repository).
    
    cd python

Step 0.2: Update test.txt with the message that you want to test. The message must be in the utf-8 encoding. 

Step 1: Run the receiver.py on a terminal session.

    python3 receiver.py

Step 2: Run the sender.py on a separate terminal session

    python3 sender.py

## Structure of the code
The codes for the experiment is in the python/ folder

### CBC
cbc.py
This contains a class with functions for CBC block ciphers.

### OFB
ofb.py
This contains a class with functions for OFB block ciphers. 
However, the functions in this class cannot run on multiprocess in Python. The decrypt function that can run on multiprocess is in receiver.py

### CTR
ctr.py
This contains a class with functions for CTR block ciphers. 
However, the functions in this class cannot run on multiprocess in Python. The decrypt function that can run on multiprocess is in receiver.py

## The behaviour of the program.
The test message must be in the file test_message.txt
The start time will be in sender.csv
The end time will be in receiver.csv
