#include "stream.h"

int main(int argc, char ** argv) {
    int i = 2, rFlag = 0;
    if(strcmp(argv[1], "remove") == 0) {
        rFlag = 1;
    }
    char * username = malloc(sizeof(char) * 100);
    char streams[100];
    strcpy(username, argv[i]);
    while(argv[i+2] != NULL) {
        strcat(username, " ");
        strcat(username, argv[i+1]);
        ++i;
    }
    ++i;
    strcpy(streams,argv[i]);
    int j;
    for(i = 0; i < strlen(streams); ++i) {
        if(streams[i] == ' ') {
            for(j = i; j < strlen(streams) - 1; ++j) {
                streams[j] = streams[j+1];
            }
            streams[strlen(streams)-1] = '\0';
        }
    }
    if(rFlag == 1) {
        removeUser(username, streams);
    } else {
        addUser(username, streams);
    }
    free(username);
    return(0);
}
