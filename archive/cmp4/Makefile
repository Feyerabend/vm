
CC		= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES	= cmp4.o scan.o error.o vm4.o runvm.o
TARGET		= cmp4 runvm

all: $(TARGET)

cmp4: cmp4.o scan.o error.o
	$(CC) $(CFLAGS) -o cmp4 cmp4.o scan.o error.o $(LDFLAGS)

runvm: runvm.o vm4.o
	$(CC) $(CFLAGS) -o runvm runvm.o vm4.o $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~
