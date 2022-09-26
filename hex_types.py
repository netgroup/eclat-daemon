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
    if data < 0:
      raise OverflowError
    elif data < 2**(self.size):
      #self.v = data % 2**self.size
      self.v = data
    else:
      raise OverflowError
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

class u256(uGeneric):
  def __init__(self, data):
    super().__init__(256, data) 

class u128(uGeneric):
  def __init__(self, data):
    super().__init__(128, data)

class u96(uGeneric):
  def __init__(self, data):
    super().__init__(96, data) 

class u64(uGeneric):
  def __init__(self, data):
    super().__init__(64, data) 

class u48(uGeneric):
  def __init__(self, data):
    super().__init__(48, data) 

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


"""
converts a srh header to an hex_list
"""
class srh_hdr:
  def __init__(self, nsegs):
    self.srhlen = 8 + 16 * nsegs
    self.nxthdr = u8(59)
    self.hdrlen = u8((self.srhlen >> 3) - 1)
    self.type = u8(4)
    self.segleft = u8(nsegs - 1)
    self.lastentry = u8(nsegs - 1)
    self.flags = u8(0)
    self.tag = u16(0)

  def set_nxthdr(self, data):
    self.nxthdr = u8(data)
  def get_nxthdr(self):
    return self.nxthdr
  def set_hdrlen(self, data):
    self.hdrlen = u8(data)
  def get_hdrlen(self):
    return self.hdrlen
  def set_segleft(self, data):
    self.segleft = u8(data)
  def get_segleft(self):
    return self.segleft
  def set_lastentry(self, data):
    self.lastentry = u8(data)
  def get_flags(self):
    return self.lastentry
  def set_flags(self, data):
    self.flags = u8(data)
  def get_flags(self):
    return self.flags
  def set_tag(self, data):
    self.tag = u16(data)
  def get_tag(self):
    return self.tag

  def to_hex(self):
    hex_list = []
    hex_list.append(self.nxthdr.toHex())
    hex_list.append(self.hdrlen.toHex())
    hex_list.append(self.type.toHex())
    hex_list.append(self.segleft.toHex())
    hex_list.append(self.lastentry.toHex())
    hex_list.append(self.flags.toHex())
    hex_list.append(self.tag.toHex())
    return hex_list
