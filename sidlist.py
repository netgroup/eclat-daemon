"""
sidlist

implements a list of IPv6 addresses

my_sidlist = Sidlist()

my_sidlist.add('ff00::1')
my_sidlist.add('ff00::2')

print(my_sidlist.len())
print(my_sidlist.get())
print(my_sidlist.to_hex())

my_sidlist.set(['cafe::1','cafe::2','cafe::2'])



"""

import math
import ipaddress
from hex_types import to_hex

class Sidlist:
  def __init__(self):
    self.list = []
  def __call__(self):
    return self.get()

  def set(self,data):
    """
    take a list as input

    each element of the list can be an ipaddress.IPv6Address
    or a string representation of an IPv6 address
    """
    if type(data) != type([]):
      raise TypeError("List is needed")
    else:
      self.list = []
      for i in data:
        self.add(i)

  def add(self, ipv6_addr):
    """
    add an IPv6 address to a Sidlist

    the IPv6 address can be an ipaddress.IPv6Address
    or a string representation of an IPv6 address
    """
    if type(ipv6_addr) == type(ipaddress.IPv6Address('::1')):
      self.list.append(ipv6_addr)
    else:
      self.list.append(ipaddress.IPv6Address(ipv6_addr))

  def get(self):
    """
    return the Sidlist as a list of ipaddress.IPv6Address
    """
    return self.list

  def len(self):
    """
    return the length of the Sidlist
    """
    return len(self.list)


  def to_hex(self):
    """
    return the Sidlist as an array of hex in network order
    """
    tmp = []
    for i in self.list:
      tmp.extend(to_hex(i))
    return tmp


