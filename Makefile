CC=gcc
CFLAGS = -ansi -Wall -g

all: post addauthor creator

post: stream/post.cc libstream.a
	$(CC) $(CFLAGS) converter/converter.c -o converter/c
	./converter/c stream/post.cc
	rm converter/c
	$(CC) $(CFLAGS) stream/post.c -o stream/post.o -c
	$(CC) $(CFLAGS) stream/post.c -o stream/post -L. -lstream
	rm stream/post.c
	rm stream/*.o

addauthor: stream/addauthor.c libstream.a
	$(CC) $(CFLAGS) stream/addauthor.c -o stream/addauthor.o -c
	$(CC) $(CFLAGS) stream/addauthor.c -o stream/addauthor -L. -lstream
	rm stream/*.o

libstream.a: stream/stream.c stream/stream.h
	$(CC) -c stream/stream.c -o stream/stream.o
	ar cr libstream.a stream/stream.o
	rm stream/*.o

creator: siteCreator.c
	$(CC) $(CFLAGS) siteCreator.c -o sc
