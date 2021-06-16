import json
import sys
import os

#Configuration class is a singleton class

class Configuration:
 _obj=None
 def __new__(class_ref):
  if Configuration._obj!=None: return Configuration._obj
  if os.path.isfile("server.cfg")==False:
   print("Configuration file server.cfg is missing, refer documentation")
   sys.exit()
  try:
   with open("server.cfg") as json_file:
    new_dict=json.load(json_file)
  #issues file is opened but its contents are not in json form, therefore try
  except json.decoder.JSONDecodeError as e: 
   print("Contents of server.cfg are not of JSON Type, refer documentation")
   sys.exit()
  Configuration._obj=super(Configuration,class_ref).__new__(class_ref)
  Configuration._obj.host=None
  Configuration._obj.port=None
  Configuration._obj.has_exceptions=False
  Configuration._obj.exceptions=dict()
  if "host" in new_dict:
   Configuration._obj.host=new_dict["host"]
  if "port" in new_dict:
   Configuration._obj.port=new_dict["port"] 
  return Configuration._obj
 def _validate_values(self):
  if Configuration._obj.host==None:
   Configuration._obj.exceptions["host"]=('V',"host entry is missing in configuration file, server.cfg, refer documentation")
  elif isinstance(Configuration._obj.host,str)==False:
   Configuration._obj.exceptions["host"]=('T',f"host of type {type(Configuration._obj.host)}, it should be of type {type('a')}")
  if Configuration._obj.port==None:
   Configuration._obj.exceptions["port"]=('V',"port entry is missing in configuration file, server.cfg, refer documentation")
  elif isinstance(Configuration._obj.port,int)==False:
   Configuration._obj.exceptions["port"]=('T',f"port of type {type(Configuration._obj.port)}, it should be of type {type(10)}")
  elif Configuration._obj.port<0 or Configuration._obj.port>49151:
   Configuration._obj.exceptions["port"]=('V',f"port number is {Configuration._obj.port}, whereas it should be >=0 and <=49151")
  if len(Configuration._obj.exceptions)>0: Configuration._obj.has_exceptions=True


