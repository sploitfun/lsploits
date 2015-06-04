//#echo 0 > /proc/sys/kernel/randomize_va_space
//$gcc -z execstack -fno-stack-protector -mpreferred-stack-boundary=2 -o vuln vuln.c
#include <stdio.h>
#include <string.h>

void foo(char* arg);
void bar(char* arg);

void foo(char* arg) {
	bar(arg);
}

void bar(char* arg) {
	char buf[256];
	strcpy(buf, arg);
}

int main(int argc, char *argv[]) {
	if(strlen(argv[1])>256) {
		printf("Buffer Overflow Attempt!!!\r\n");
		fflush(stdout);
		return 1;
	}
	foo(argv[1]);
	return 0;
}
