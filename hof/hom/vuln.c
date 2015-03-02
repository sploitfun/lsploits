/* 
 House of Mind vulnerable program
 */
#include <stdio.h>
#include <stdlib.h>

int main (void) {
   char *ptr  = malloc(1024);        /* First allocated chunk */
   char *ptr2, *ptr3;                /* Second chunk  & Last but one chunk */
   int heap = (int)ptr & 0xFFF00000;
   _Bool found = 0;
   int i = 2;

   printf("ptr found at %p\n", ptr);  /* Print address of first chunk */
   
   for (i = 2; i < 1024; i++) {
     /* Prereq 1: Series of malloc calls until a chunk's address - when aligned to HEAP_MAX_SIZE results in 0x08100000 */
     /* 0x08100000 is the place where fake heap_info structure is found. */
     if (!found && (((int)(ptr2 = malloc(1024)) & 0xFFF00000) == \
                                           (heap + 0x100000))) {
          printf("good heap allignment found on malloc() %i (%p)\n", i, ptr2);
          found = 1;
          break;
       }

   }
        ptr3 = malloc(1024); /* Last but one chunk */
        malloc(1024); /* Request another chunk. Hence next chunk to ptr3 != top chunk */
        /* User Input. */
        fread (ptr, 1024 * 1024, 1, stdin); 

        free(ptr);   /* Free first chunk  */
        free(ptr2);  /* Prereq 2: Freeing a chunk whose size and its arena pointer is controlled by the attacker. */
	free(ptr3);  /* Shell code execution. */
        return(0);   /* Bye */
}
