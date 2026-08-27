# Makefile
# This Makefile compiles the vulnerable C code into a shared library.

all: libvulnerable.so

libvulnerable.so: vulnerable.o
	gcc -shared -o libvulnerable.so vulnerable.o

vulnerable.o: vulnerable.c
	gcc -c vulnerable.c

clean:
	rm -f libvulnerable.so vulnerable.o