CC=gcc
CFLAGS = -ansi -Wall -g

all: libstream post addauthor creator

post: post.cc libstream.a
	$(CC) $(CFLAGS) converter.c -o c
	./c post.cc
	rm c
	$(CC) $(CFLAGS) post.c -o post.o -c
	$(CC) $(CFLAGS) post.o -o post -L. -lstream
	rm post.c
	mkdir messages

addauthor: addauthor.c libstream.a
	$(CC) $(CFLAGS) addauthor.c -o addauthor.o -c
	$(CC) $(CFLAGS) addauthor.o -o addauthor -L. -lstream
	rm *.o

libstream: stream.c stream.h
	$(CC) -c stream.c -o stream.o
	ar cr libstream.a stream.o
	rm *.o

creator: siteCreator.c
	$(CC) $(CFLAGS) siteCreator.c -o sc
