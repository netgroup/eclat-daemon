"""
hex_types.to_hex(data)
convert data into a list of strings with the hex representation of data
to be used inside a BPF map as key or value

data can be:
- a list
- an object that supports a to_hex() method
- an int (converted to 8 bytes little-endian)
- an ipaddress.IPv6Address (converted in big-endian)

"""

import math
import ipaddress

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
  def toHex(self):
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

class u128(uGeneric):
  def __init__(self, data):
    super().__init__(128, data) 

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

class s128(sGeneric):
  def __init__(self, data):
    super().__init__(128, data) 

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
  elif type(data) == type(ipaddress.IPv6Address('::1')):
    hex_list = to_hex(u128(int(data)))
    hex_list.reverse()
  elif type(data) == type(0):
    hex_list = to_hex(u64(data))
  else:
    hex_list = data.toHex()
  return hex_list

"""
converts a list of 16 integers 0-255 (big-endian) to an integer (128 bit equivalent)
"""
def ipv6_int128_from_int8(input_list):
    ipv6_int128 = 0
    i = 15
    for int8 in input_list:
        ipv6_int128 = ipv6_int128 | (int8 << (i*8))
        i = i - 1
    #print (ipv6_int128)
    return ipv6_int128
