
CC		= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES	= adder.o
TARGET		= adder

all: $(TARGET)

adder: adder.o
	$(CC) $(CFLAGS) -o adder adder.o $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~
