CC		= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES	= bin.o factorial.o prime.o vm3.o
TARGET		= bin factorial prime

all: $(TARGET)

factorial: factorial.o vm3.o
	$(CC) $(CFLAGS) -o factorial factorial.o vm3.o $(LDFLAGS)

bin: bin.o vm3.o
	$(CC) $(CFLAGS) -o bin bin.o vm3.o $(LDFLAGS)

prime: prime.o vm3.o
	$(CC) $(CFLAGS) -o prime prime.o vm3.o $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~
