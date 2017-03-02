#include "siteCreator.h"

int main(int argc, char **argv) {
    char * filename;
    if(argc != 2) {
        printf("Default file: <config> being used\n");
        filename = malloc(sizeof(char) * 7);
        strcpy(filename, "config");
    } else {
        printf("Input file: <%s> being used\n", argv[1]);
        filename = malloc(strlen(argv[1]) + 1);
        strcpy(filename, argv[1]);
    }

    printf("%s\n", filename);
    return(0);
}
