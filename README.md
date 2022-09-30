# CS525-CodingProject

## Description
The goal of this project is to implement 3 modes of block cipher learned in class, namely CBC, OFB, and CRT. Then, we need to compare their performance. 

## Language and Libraries

## Test Plan
### Description of the test program
The idea for the test program would be to have a sender process and a receiver process.

The sender will send a certain amount of messages to the receiver with each of the block cipher mode.

When the sender starts, we will save a timestamp, when the receiver ends, we will save another timestamp. This will allow us to calculate the total amount of time taken to transmit the same message for each cipher block mode. 

#### Why process instead of threads?
This is because depending on the operating systems and programming languages, threads may not be run parallely but only concurrently on multi-cores systems since they belong to the same process and share the same resources. 

While processes have a higher chance of being run in different cores since they are meant to be separated. 

#### The benefits of running on local machines
The benefit of running such system in a local machine is to reduce the effect of transmission delay due to propagation delay and packet loss. 

#### The transport protocol to use 
We will use UDP as the transport layer protocol to eliminate the variable delays from the transport layer protocol like TCP. 

### Encryption/Decryption Algorithm

### Measurement Method
### The size of the message to send

