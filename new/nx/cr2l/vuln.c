#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[]) {
 char buf[256];
 /* Temporarily drop privileges */
 seteuid(getuid());
 strcpy(buf,argv[1]);
 printf("%s",buf);
 fflush(stdout);
 return 0;
}
