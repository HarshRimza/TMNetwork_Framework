import json

# this file contains three classes Wrapper,Request,Response

class Wrapper:
 def __init__(self,value):
  self.value=value
  self.class_name=type(value).__name__
 def toJSON(self):
  return json.dumps(self.__dict__)
 def fromJSON(json_string):
  new_dict=json.loads(json_string)
  value=new_dict["value"]
  class_name=new_dict["class_name"]
  return eval(f"{class_name}({value})")

class Request:
 def __init__(self,manager,action,request_object=None):
  self.manager=manager
  self.action=action
  if request_object!=None: self.json_string=request_object.toJSON()
  else : self.json_string="{}"
 def toJSON(self):
  return json.dumps(self.__dict__)
 def fromJSON(json_string): 
  new_dict=json.loads(json_string)
  r=Request(new_dict["manager"],new_dict["action"],None)
  r.json_string=new_dict["json_string"]
  return r

class Response:
 def __init__(self,success,error=None,result_object=None):
  self.success=success
  if error!=None : self.error_json_string=error.toJSON()
  else : self.error_json_string="{}"
  if result_object!=None : 
   self.result_json_string=result_object.toJSON()
  else : 
   self.result_json_string="{}"
 def toJSON(self):
  json_string=json.dumps(self.__dict__)
  return json_string
 def fromJSON(json_string): 
  new_dict=json.loads(json_string)
  r=Response(new_dict["success"])
  r.error_json_string=new_dict["error_json_string"]
  r.result_json_string=new_dict["result_json_string"]
  return r
 