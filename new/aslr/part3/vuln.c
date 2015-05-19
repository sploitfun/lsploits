// vuln.c
// gcc -o vuln vuln.c -fno-stack-protector
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main (int argc, char **argv)
{
 char buf[256];
 int i;
 seteuid (getuid());
 if (argc < 2)
 {
  puts ("Need an argument\n");
  exit (1);
 }
 strcpy (buf, argv[1]);
 printf ("%s\nLen:%d\n", buf, (int)strlen(buf));
 return (0);
}
