#include "siteCreator.h"

void parseLine(char *buffer);

int main(int argc, char **argv) {
    if(argc != 2) {
        printf("Include Filename\n");
        return(-1);
    }
    char *filename = malloc(strlen(argv[1]) + 1);
    strcpy(filename, argv[1]);
    char *buffer = malloc(sizeof(char) * 1000);
    FILE *fp = fopen(filename, "r");
    if(fp == NULL) {
        printf("Invalid File\n");
        return(-1);
    }

    while(fgets(buffer, 999,fp)) {
        buffer[strlen(buffer) - 1] = '\0';
        parseLine(buffer);
    }
    fclose(fp);

    free(buffer);
    free(filename);
    return(0);
}

void parseLine(char *buffer) {
    char *tok = strtok(buffer, ")");
    while(tok != NULL) {
        if(tok[0] == '.' && tok[2] == '(') {
            switch(tok[1]) {
                case 'h':
                    break;
                case 't':
                    break;
                case 'd':
                    break;
                case 'l':
                    break;
                case 'p':
                    break;
                case 'e':
                    break;
                case 'b':
                    break;
                case 'i':
                    break;
                case 'r':
                    break;
                default:

            }
        }
        tok = strtok(NULL, ")");
    }
}
