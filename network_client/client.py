from network_client.config import Configuration
from network_common.wrappers import Request,Response
import socket
import sys
 
class NetworkClient:
 def __init__(self):
  self.server_configuration=Configuration()
  self.server_configuration._obj._validate_values()
  if self.server_configuration._obj.has_exceptions:
   for exception in self.server_configuration._obj.exceptions.values():
    print(exception[1])
   sys.exit() # needs to be converted to code that raises exception
 def send(self,request):
  client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  client_socket.connect((self.server_configuration.host,self.server_configuration.port))
  request_data=request.toJSON()

  client_socket.sendall(bytes("12".ljust(1024),"utf-8"))
  client_socket.sendall(bytes("it is client","utf-8"))
  client_socket.sendall(bytes(str(len(request_data)).ljust(1024),"utf-8"))
  client_socket.sendall(bytes(request_data,"utf-8"))

  to_receive=1024
  data_bytes=b''
  data_bytes_length=0
  while data_bytes_length<to_receive:
   dbytes=client_socket.recv(to_receive-data_bytes_length)
   data_bytes+=dbytes
   data_bytes_length+=len(dbytes)
  response_data_length=int(data_bytes.decode("utf-8").strip())
  to_receive=response_data_length
  data_bytes=b''
  data_bytes_length=0
  while data_bytes_length<to_receive:
   dbytes=client_socket.recv(to_receive-data_bytes_length)
   data_bytes+=dbytes
   data_bytes_length+=len(dbytes)
  response_data=data_bytes.decode("utf-8")
  client_socket.shutdown(socket.SHUT_RDWR)    #read as well as write, we want all operation to be closed
  client_socket.close()
  response=Response.fromJSON(response_data)
  return response
