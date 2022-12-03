# CS525-CodingProject

## Description
The goal of this project is to implement 3 modes of block cipher learned in class, namely CBC, OFB, and CRT. Then, we need to compare their performance. 

## How to run
### Install pycryptodome

    pip install pycryptodome

### Run the program
Step 0.1: Get into the folder python (Assuming that you are inside the root of the git repository).
    
    cd python

Step 0.2: Update test_message.txt with the message that you want to test. The message must be in the utf-8 encoding. 

Step 1: Run the receiver.py on a terminal session.

    python3 receiver.py

Step 2: Run the sender.py on a separate terminal session

    python3 sender.py
  
Step 3: Enter the required input and the program will run

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

The test message must be in the file test_message.txt . 

The start time will be in sender.csv .

The end time will be in receiver.csv .

### Steps
At the start, after the user has entered the input. The sender will send the following information to the receiver:
+ Block size.
+ IV.
+ Key.
+ Algorithm used (AES).
+ Cipher mode (CBC, OFB, or CTR).
+ The number of cipher blocks.
+ The path to the message (which is test_message.txt).

Then, the sender will wait for the receiver to send back a message saying that the receiver has finished setting up and is ready to receive the cipher blocks. 
Once the sender receive the message, the sender will use perf_counter() to get the start timestamp and start sending the cipher blocks and the receiver will start decrypting the cipher blocks.
Once the receiver has finished decrypting to get the plaintext blocks, it will use perf_counter() again to get the end timestamp and output it to receiver.csv . 
One the sender has sent everything, the sender will write the start timestamp to sender.csv .
It will also read the original message using the message path and compare to see if the decrypted message is the same as the original message.


