/* 
 Clarification - Consolidation of chunks can lead to its size being more than 128KB 
 and hence could stay in brk'd memory region.
*/
#include <stdio.h>
#include <stdlib.h>

int main() {
	char *a, *b, *c, *d, *e, *f;
	a = (char*) malloc((128*1024)-16);		//Max possible allocation throught brk
	b = (char*) malloc((130*1024)-8);		//Use the remaining top chunk
	c = (char*) malloc((128*1024)-16);		//Extend the top chunk
	d = (char*) malloc((130*1024)-8);		//Use the remaining top chunk
	e = (char*) malloc(100);			//This chunk restricts consolidation into top chunk
	free(a);					//Add chunk a into unsorted bin
	free(b);					//Add consolidated chunk (a+b) into unsorted bin
	free(c);					//Add consolidated chunk (a+b+c) into unsorted bin
	free(d);					//Add consolidated chunk (a+b+c+d) into unsorted bin
	f = (char*) malloc((1024*1024)-8);		//Put the above consolidated chunk into bin 126 (last largest bin) 
	return 0;
}
