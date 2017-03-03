#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void parseLine(char *buffer, char *filename);

void addLink(char *tok, char *filename);

void addText(char *tok, char *filename);

void addHeading(char *tok, char *filename);

int main(int argc, char **argv) {
    if(argc != 2) {
        printf("Include Filename\n");
        return(-1);
    }
    char *filename = malloc(strlen(argv[1]) + 1);
    char *outFileName = malloc(strlen(filename) + 5);
    strcpy(filename, argv[1]);
    strcpy(outFileName, filename);
    strcat(outFileName, ".html");
    char *buffer = malloc(sizeof(char) * 1000);
    FILE *fp = fopen(filename, "r");
    if(fp == NULL) {
        printf("Invalid File\n");
        return(-1);
    }
    FILE *outfp = fopen(outFileName, "w");
    fprintf(outfp,"<html>\n");
    fclose(outfp);
    while(fgets(buffer, 999,fp)) {
        buffer[strlen(buffer) - 1] = '\0';
        parseLine(buffer, outFileName);
    }
    outfp = fopen(outFileName, "a");
    fprintf(outfp,"</html>\n");
    fclose(outfp);

    fclose(fp);

    free(buffer);
    free(filename);
    return(0);
}

void parseLine(char *buffer, char *filename) {
    char *tok = strtok(buffer, ")");
    while(tok != NULL) {
        if(tok[0] == '.' && tok[2] == '(') {
            switch(tok[1]) {
                case 'h':
                    addHeading(tok, filename);
                    break;
                case 't':
                    addText(tok, filename);
                    break;
                case 'd':
                    break;
                case 'l':
                    addLink(tok, filename);
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
                    break;

            }
        }
        tok = strtok(NULL, ")");
    }
}

void addText(char *tok, char *filename) {
    FILE *fp = fopen(filename, "a");
    char *textptr = strstr(tok, "text="), *filenameptr = strstr(tok, "file=");
    fprintf(fp, "<p>");
    if(filenameptr == NULL) {
        if(textptr == NULL) {
            fprintf(fp, "Default text");
        } else {
            textptr += 6;
            while(textptr[0] != '"') {
                fprintf(fp, "%c", textptr[0]);
                ++textptr;
            }
        }
    } else {
        filenameptr += 6;
        char inFileName[100], c;
        int i = 0;
        while(filenameptr[i] != '"') {
            inFileName[i] = filenameptr[i];
            ++i;
        }
        FILE *infp = fopen(inFileName, "r");
        while((c = fgetc(infp)) != EOF) {
            fprintf(fp, "%c", c);
        }
        fclose(infp);
    }
    fprintf(fp, "</p>");
    fclose(fp);
}

void addLink(char *tok, char *filename) {
    FILE *fp = fopen(filename, "a");
    char *linkptr = strstr(tok, "link="), *textptr = strstr(tok, "text=");
    linkptr += 6;
    fprintf(fp, "<a href=\"");
    while(linkptr[0] != '"') {
        fprintf(fp, "%c", linkptr[0]);
        ++linkptr;
    }
    fprintf(fp,"\">\n");
    if(textptr == NULL) {
        fprintf(fp,"link");
    } else {
        textptr += 6;
        while(textptr[0] != '"') {
            fprintf(fp, "%c", textptr[0]);
            ++textptr;
        }
    }
    fprintf(fp, "</a>\n");
    fclose(fp);
}

void addHeading(char *tok, char *filename) {
    FILE *fp = fopen(filename, "a");
    char *sizeptr = strstr(tok, "size="), *textptr = strstr(tok, "text=");
    if(sizeptr == NULL) {
        fprintf(fp, "<h3>\n");
        if(textptr == NULL) {
            fprintf(fp, "HEADING");
        } else {
            textptr += 6;
            while(textptr[0] != '"') {
                fprintf(fp, "%c", textptr[0]);
                ++textptr;
            }
        }
        fprintf(fp, "</h3>\n");
    } else {
        sizeptr += 5;
        fprintf(fp, "<h%c>\n", sizeptr[0]);
        if(textptr == NULL) {
            fprintf(fp, "HEADING");
        } else {
            textptr += 6;
            while(textptr[0] != '"') {
                fprintf(fp, "%c", textptr[0]);
                ++textptr;
            }
        }
        fprintf(fp, "</h%c>\n", sizeptr[0]);
    }
    fclose(fp);
}
