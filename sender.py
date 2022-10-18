# If we want to be parallel and not just concurrent, we need to use Pool 
import socket 

if __name__ == "__main__": 
	UDP_IP = "127.0.0.1"
	UDP_PORT = 8080
	MESSAGE = "Hello, World!" 
	print("UDP target IP: %s" % UDP_IP)
	print("UDP target port: %s" % UDP_PORT)
	print("message: %s" % MESSAGE) 
	content = bytes(MESSAGE, "utf-8")
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.sendto(content, (UDP_IP, UDP_PORT))
