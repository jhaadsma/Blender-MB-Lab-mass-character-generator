# This class creates a unique ID to distuingish character models from each other easily

import uuid

def uId():
  id = uuid.uuid4().hex
  return id
    
