#include <stdio.h>
#include <string.h>

/* Eventhough shell() function isnt invoked directly, its needed here since 'system@PLT' and 'exit@PLT' stub code should be present in executable to successfully exploit it. */
void shell() {
 system("/bin/sh");
 exit(0);
}

int main(int argc, char* argv[]) {
 int i=0;
 char buf[256];
 strcpy(buf,argv[1]);
 printf("%s\n",buf);
 return 0;
}
