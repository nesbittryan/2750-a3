#include "siteCreator.h"

int main(int argc, char **argv) {
    char * filename;
    if(argc != 2) {
        printf("Include Filename\n");
        return(-1);
    }
    filename = malloc(strlen(argv[1]) + 1);
    strcpy(filename, argv[1]);
    printf("%s\n", filename);
    return(0);
}
