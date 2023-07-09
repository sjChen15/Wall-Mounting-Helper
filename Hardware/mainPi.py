#main program to run on Raspberry Pi
import TCPClient
#test TCP
TCP_IP = '10.0.0.47'
TCP_PORT = 12345 
client = TCPClient.ClientSocket(TCP_IP, TCP_PORT)