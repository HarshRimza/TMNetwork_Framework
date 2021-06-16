import socket
import sys
import threading
from network_server.config import Configuration
from network_common.wrappers import Request,Response,Wrapper
from data_layer.hr import DataLayerException

class RequestProcessor(threading.Thread):
 def __init__(self,socket,requestHandler):
  self.socket=socket
  self.requestHandler=requestHandler
  threading.Thread.__init__(self)
 def run(self):
  dataBytes=NetworkServer.getDataBytes(self.socket,1024)
  request_json_string_length=int(dataBytes.decode("utf-8").strip())
  dataBytes=NetworkServer.getDataBytes(self.socket,request_json_string_length)
  request_json_string=dataBytes
  request=Request.fromJSON(request_json_string)  
  response=self.requestHandler(request)
  if response is None: response=Response("False",error=DataLayerException("Invalid manager or action"))
  response_json_string=response.toJSON()
  response_json_string_length=len(response_json_string)
  self.socket.sendall(bytes(str(response_json_string_length).ljust(1024),"utf-8"))
  self.socket.sendall(bytes(response_json_string,"utf-8"));
  self.socket.close()


class NetworkServer:
 def __init__(self,requestHandler):
  self.requestHandler=requestHandler
  self.server_configuration=Configuration()
  self.server_configuration._obj._validate_values()
  if self.server_configuration._obj.has_exceptions:
   for exception in self.server_configuration._obj.exceptions.values():
    print(exception[1])
   sys.exit() # needs to be converted to code that raises exception

 def getDataBytes(socket,toReceive):
  dataBytes=b''
  dataBytesLength=0 
  while dataBytesLength<toReceive:
   by=socket.recv(toReceive-dataBytesLength)
   dataBytes+=by
   dataBytesLength+=len(by)
  return dataBytes

 def start(self):
  server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  server_socket.bind(("localhost",self.server_configuration._obj.port))
  server_socket.listen()
  while True:
   print(f"Server is listening on port {self.server_configuration._obj.port}")
   client_socket,socket_name=server_socket.accept()
   dataBytes=NetworkServer.getDataBytes(client_socket,1024)
   decisionLength=int(dataBytes.decode("utf-8").strip()) 
   dataBytes=NetworkServer.getDataBytes(client_socket,decisionLength)
   clientOrNot=dataBytes.decode("utf-8").strip()
   if clientOrNot=="stop server":break
   RequestProcessor(client_socket,self.requestHandler).start()
   print("New thread has been created in memory.")
  server_socket.close()

