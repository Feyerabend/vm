
CC		= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES	= par2.o cmp3.o scan.o
TARGET		= par2 cmp3

all: $(TARGET)

par2: par2.o scan.o
	$(CC) $(CFLAGS) -o par2 par2.o scan.o $(LDFLAGS)

cmp3: cmp3.o scan.o
	$(CC) $(CFLAGS) -o cmp3 cmp3.o scan.o $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~
