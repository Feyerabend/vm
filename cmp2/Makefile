
CC			= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES	= par1.o scan.o
TARGET		= par

all: $(TARGET)

par1: par1.o scan.o
	$(CC) $(CFLAGS) -o par1 par1.o scan.o $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~
