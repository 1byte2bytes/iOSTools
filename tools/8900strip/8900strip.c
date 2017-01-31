#define _CRT_SECURE_NO_DEPRECATE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {

    if(argc != 3) {
        printf("8900strip [input file] [output file]");
        exit(-1);
    }

    FILE *original;
    FILE *stripped;
    unsigned char buffer;
    long original_len;
    char* original_filename = (char*)argv[1];

    original = fopen((const char *)argv[1], "rb");
    if (original == NULL) {
        printf("Original file could not be found");
        exit(-2);
    }
    fseek(original, 0, SEEK_END);
    original_len = ftell(original);
    rewind(original);

    unsigned char header[8];

    for (int i = 0; i < 7; i++){
        fread(&buffer, 1, 1, original);
        header[i] = buffer;
    }
    header[7] = '\0';

    //header: 89001.0
    if (strcmp(header, "89001.0") == 0) {
        printf("Stripping file %s\r\n", argv[1]);
    } else {
        printf("No 8900 header found.\r\n");
        exit(-3);
    }

    stripped = fopen((const char *)argv[2], "wb");

    fseek(original, 2048, SEEK_SET);
    fseek(stripped, 0, SEEK_SET);

    for (int i = 0; i < original_len-2048; ++i){
        fread(&buffer, 1, 1, original);
        fwrite(&buffer, 1, 1, stripped);
    }

    fclose(original);
    fclose(stripped);

}