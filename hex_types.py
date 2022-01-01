import math

class uGeneric:
  def __init__(self, size, data):
    self.size = size
    self.set(data)
  def __call__(self):
    return self.get()
  def set(self,data):
    self.v = data % 2**self.size
  def get(self):
    return self.v 
  def to_hex(self):
    tmp = self.v
    hex_list = []
    for i in range (0,math.ceil(self.size/8)):
        hex_list.append("{:02x}".format(tmp % 256))
        tmp = tmp >> 8
    return hex_list

class sGeneric(uGeneric):
  def __init__(self, size, data):
    super().__init__(size, data)
  def set(self,data):
    if data < - (2**(self.size-1)):
      raise OverflowError
    #elif data < 0:
    #  self.v = data
    elif data < 2**(self.size-1):
      self.v = data
    else:
      raise OverflowError

class u64(uGeneric):
  def __init__(self, data):
    super().__init__(64, data) 

class u32(uGeneric):
  def __init__(self, data):
    super().__init__(32, data) 

class u16(uGeneric):
  def __init__(self, data):
    super().__init__(16, data) 

class u8(uGeneric):
  def __init__(self, data):
    super().__init__(8, data) 

class s64(sGeneric):
  def __init__(self, data):
    super().__init__(64, data) 

class s32(sGeneric):
  def __init__(self, data):
    super().__init__(32, data) 

class s16(sGeneric):
  def __init__(self, data):
    super().__init__(16, data) 

class s8(sGeneric):
  def __init__(self, data):
    super().__init__(8, data) 

def to_hex (data):
  #print (type(data))
  hex_list = []
  if type(data) == type([]):
    for e in data:
      hex_list.extend(to_hex(e))
  elif type(data) == type(0):
    hex_list = to_hex(u64(data))
  else:
    hex_list = data.to_hex()
  return hex_list
