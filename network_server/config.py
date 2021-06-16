import sys
import os
from xml.etree import ElementTree
from common.hr import ValidationException

class Configuration:
 _obj=None
 def __new__(class_ref):
  if Configuration._obj!=None: return Configuration._obj
  if os.path.isfile("server.xml")==False:
   print("Configuration file server.xml is missing, refer documentation")
   sys.exit()
  try:
   with open("server.xml") as serverConfigurationFile:
    xmlTree=ElementTree.parse(serverConfigurationFile)
  except ElementTree.ParseError as parseError: 
   print("contents of server.xml are malformed, refer documentation")
   sys.exit()
  rootNode=xmlTree.getroot()
  Configuration._obj=super(Configuration,class_ref).__new__(class_ref)
  Configuration._obj.port=None
  port=None
  for node in rootNode: 
   if node.tag=="port":port=node.text
  Configuration._obj.has_exceptions=False
  Configuration._obj.exceptions=dict()
  if port!=None:
   try:
    Configuration._obj.port=int(port)
   except Exception as exception:
    print(f"port in server.xml is of type {type(port)}, it should be of type {type(10)}")
    sys.exit()
  return Configuration._obj
 def _validate_values(self):
  if Configuration._obj.port==None:
   Configuration._obj.exceptions["port"]=('V',"port entry is missing in configuration file, server.xml, refer documentation")
  elif isinstance(Configuration._obj.port,int)==False:
   Configuration._obj.exceptions["port"]=('T',f"port of type {type(Configuration._obj.port)}, it should be of type {type(10)}")
  elif Configuration._obj.port<0 or Configuration._obj.port>49151:
   Configuration._obj.exceptions["port"]=('V',f"port number is {Configuration._obj.port}, whereas it should be >=0 and <=49151")
  if len(Configuration._obj.exceptions)>0: Configuration._obj.has_exceptions=True
