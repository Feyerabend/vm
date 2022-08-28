
CC		= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES		= enkel.o error.o scan.o symbol.o vmenkel.o runvm.o
TARGET		= enkel runvm

all: $(TARGET)

enkel: enkel.o scan.o symbol.o error.o
	$(CC) $(CFLAGS) -o enkel enkel.o scan.o symbol.o error.o $(LDFLAGS)

runvm: runvm.o vmenkel.o
	$(CC) $(CFLAGS) -o runvm runvm.o vmenkel.o $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~

