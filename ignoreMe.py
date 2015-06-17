#  
#   Hello World client in Python  
#   Connects REQ socket to tcp://localhost:5555  
#   Sends "Hello" to server, expects "World" back  
#  
import zmq  
import socket
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)
context = zmq.Context()  
  
#  Socket to talk to server  
print "Connecting to hello world server..."  
socket = context.socket(zmq.REQ)  

s = "tcp://" + myaddr + ":5555"
print s
socket.connect (s)  
  
#  Do 10 requests, waiting each time for a response  
for request in range (1,10):  
    print "Sending request ", request,"..."  
    socket.send ("Hello")  
      
    #  Get the reply.  
    message = socket.recv()  
    print "Received reply ", request, "[", message, "]"  