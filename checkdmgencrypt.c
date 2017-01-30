#define _CRT_SECURE_NO_DEPRECATE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {

    if(argc != 2) {
        printf("checkdmgencrypted [input file]");
        exit(-1);
    }

    FILE *original;
    unsigned char buffer;

    original = fopen((const char *)argv[1], "rb");
    if (original == NULL) {
        printf("File could not be found");
        exit(-2);
    }

    unsigned char header[9];

    for (int i = 0; i < 8; i++){
        fread(&buffer, 1, 1, original);
        header[i] = buffer;
    }
    header[8] = '\0';

    //header: 89001.0
    if (strcmp(header, "encrcdsa") == 0) {
        printf("DMG file %s is encrypted\r\n", argv[1]);
    } else {
        printf("DMG file %s is not encrypted\r\n", argv[1]);
    }

    fclose(original);

}