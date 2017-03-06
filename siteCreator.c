#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *removeSpaces(char * str);

void printToFile(char *tok, char *filename);

void parseLine(char *buffer, char *filename);

void addLink(char *tok, char *filename);

void addText(char *tok, char *filename);

void addHeading(char *tok, char *filename);

void addLine(char *tok, char *filename);

void addImage(char *tok, char *filename);

void addButton(char *tok, char * filename);

void addInput(char *tok, char *filename);

void addRadioButton(char *tok, char *filename);

void addExe(char *tok, char *filename);

int main(int argc, char **argv) {
    if(argc != 2) {
        printf("Include Filename\n");
        return(-1);
    }
    char *filename = malloc(strlen(argv[1]) + 1);
    char *outFileName = malloc(strlen(argv[1]) + 1);
    strcpy(filename, argv[1]);
    strcpy(outFileName, argv[1]);
    char *ptr = strstr(outFileName, "wpml");
    strcpy(ptr, "html");
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
                    addHeading(removeSpaces(tok), filename);
                    break;
                case 't':
                    addText(removeSpaces(tok), filename);
                    break;
                case 'd':
                    addLine(removeSpaces(tok), filename);
                    break;
                case 'l':
                    addLink(removeSpaces(tok), filename);
                    break;
                case 'p':
                    addImage(removeSpaces(tok), filename);
                    break;
                case 'e':
                    addExe(removeSpaces(tok), filename);  /*FIXME*/
                    break;
                case 'b':
                    addButton(removeSpaces(tok), filename);
                    break;
                case 'i':
                    addInput(removeSpaces(tok), filename);
                    break;
                case 'r':
                    addRadioButton(removeSpaces(tok), filename);
                    break;
                default:
                    printToFile(tok, filename);
                    break;
            }
        } else {
            printToFile(tok, filename);
        }
        tok = strtok(NULL, ")");
    }
}

void addExe(char *tok, char *filename) {
    FILE *fp = fopen(filename, "a");
    char * nameptr = strstr(tok, "exe=");
    nameptr += 5;
    char exeName[100];
    int i = 0;
    while(nameptr[i] != '"') {
        exeName[i] = nameptr[i];
        ++i;
    }
    FILE *tempfp;
    if((tempfp = fopen(exeName, "r")) == NULL) {
        char temp[99];
        strcpy(temp, "./bin/");
        strcat(temp, exeName);
        if((tempfp = fopen(temp, "r")) == NULL) {
            fprintf(fp,"<?php\n\texec(\"%s\");\n?>\n", exeName);    //FIXME
        } else {
            fclose(tempfp);
            fprintf(fp,"<?php\n\texec(\"%s\");\n?>\n", exeName);
        }
    } else {
        fclose(tempfp);
        fprintf(fp,"<?php\n\texec(\"%s\");\n?>\n", exeName);
    }
    fclose(fp);
}

void addRadioButton(char *tok, char *filename) {
    char *action = strstr(tok, "action=");
    char *nameptr, *valueptr;
    int i = 0 , j = 0;
    FILE *fp = fopen(filename, "a");
    fprintf(fp, "<form action=\"");
    action += 8;
    while(action[i] != '"') {
        fprintf(fp, "%c", action[i]);
        ++i;
    }
    fprintf(fp, "\" method=\"post\">\n");

    nameptr = strstr(tok, "name=");
    nameptr += 6;
    while((valueptr = strstr(tok, "value=")) != NULL) {
        valueptr += 7;
        fprintf(fp, "\t");
        fprintf(fp, "<input type=\"radio\" name=\"");
        i = 0;
        while(nameptr[i] != '"') {
            fprintf(fp, "%c", nameptr[i]);
            ++i;
        }
        fprintf(fp, "\" value=\"");
        i = 0;
        while(valueptr[i] != '"') {
            fprintf(fp, "%c", valueptr[i]);
            ++i;
        }
        if(j == 0) {
            fprintf(fp, "\" checked>");
        } else {
            fprintf(fp, "\">");
        }
        i = 0;
        while(valueptr[i] != '"') {
            fprintf(fp, "%c", valueptr[i]);
            ++i;
        }
        fprintf(fp, "<br>\n");
        tok = valueptr;
        j = 1;
    }
    fprintf(fp, "\t<input type=\"submit\" value=\"submit\">\n</form>\n");
    fclose(fp);
}

void addInput(char *tok, char *filename) {
    char *action = strstr(tok, "action=");
    char  *textptr, *nameptr, *valueptr;
    int i = 0;
    FILE *fp = fopen(filename, "a");
    fprintf(fp, "<form action=\"");
    action += 8;
    while(action[i] != '"') {
        fprintf(fp, "%c", action[i]);
        ++i;
    }
    fprintf(fp, "\" method=\"post\">\n");
    while((textptr = strstr(tok, "text=")) != NULL) {
        textptr += 6;
        nameptr = strstr(textptr, "name=");
        valueptr = strstr(textptr, "value=");
        fprintf(fp, "\t");
        while(textptr[0] != '"') {
            fprintf(fp, "%c", textptr[0]);
            ++textptr;
        }
        fprintf(fp, "<input type=\"text\" name=\"");
        nameptr += 6;
        while(nameptr[0] != '"') {
            fprintf(fp, "%c", nameptr[0]);
            ++nameptr;
        }
        fprintf(fp, "\" value=\"");
        valueptr += 7;
        while(valueptr[0] != '"') {
            fprintf(fp, "%c", valueptr[0]);
            ++valueptr;
        }
        fprintf(fp, "\">\n");

        tok = textptr;
    }
    fprintf(fp, "\t<input type=\"submit\" value=\"submit\"\n</form>\n");
    fclose(fp);
}

void addButton(char *tok, char * filename) {
    FILE *fp = fopen(filename, "a");
    char *namePtr = strstr(tok, "name="), *linkPtr = strstr(tok, "link=");
    if(namePtr == NULL || linkPtr == NULL) return;
    namePtr +=6;
    linkPtr +=6;
    fprintf(fp, "<form action=\"");
    int i = 0;
    while(linkPtr[i] != '"') {
        fprintf(fp, "%c", linkPtr[i]);
        ++i;
    }
    fprintf(fp, "\">\n\t<input type=\"submit\" value=\"");
    i =0;
    while(namePtr[i] != '"') {
        fprintf(fp, "%c", namePtr[i]);
        ++i;
    }
    fprintf(fp, "\"/>\n</form>\n");
    fclose(fp);
}

void addImage(char *tok, char *filename) {
    FILE *fp = fopen(filename, "a");
    char *sizePtr = strstr(tok, "size="), *imagePtr = strstr(tok, "image=");
    fprintf(fp, "<img src=");
    imagePtr += 6;
    if(sizePtr != NULL) {
        int i = 0;
        while(imagePtr[i] != ',') {
            fprintf(fp, "%c", imagePtr[i]);
            ++i;
        }
        sizePtr += 5;
        char *sizeTok = strtok(sizePtr, "x");
        fprintf(fp, " width=\"%s\"", sizeTok);
        sizeTok = strtok(NULL, ")");
        fprintf(fp, " height =\"%s\"", sizeTok);
    } else {
        fprintf(fp, "%s width=\"100\" height = \"100\"", imagePtr);
    }
    fprintf(fp, ">\n");
    fclose(fp);
}

void addLine(char *tok, char *filename) {
    FILE *fp = fopen(filename, "a");
    fprintf(fp, "<hr>\n");
    fclose(fp);
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
        if(infp == NULL) {
            fprintf(fp, "Invalid File");
        } else {
            while((c = fgetc(infp)) != EOF) {
                fprintf(fp, "%c", c);
            }
            fclose(infp);
        }
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

void printToFile(char *tok, char *filename) {
    FILE* fp = fopen(filename, "a");
    fprintf(fp, "%s", tok);
    fclose(fp);
}
char *removeSpaces(char * str) {
    int i;
    for(i = 0; i < strlen(str); ++i) {
        if(str[i] == '"') {
            ++i;
            while(str[i] != '"') {
                ++i;
            }
            ++i;
        }
        if(str[i] == ' ') {
            int j;
            for(j = i; j < strlen(str) - 1; ++j) {
                str[j] = str[j+1];
            }
            str[strlen(str) - 1] = '\0';
            --i;
        }
    }
    return str;
}
