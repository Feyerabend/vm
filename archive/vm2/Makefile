
CC		= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES	= fibonacci.o vm2.o
TARGET		= fib

all: $(TARGET)

$(TARGET): $(OBJFILES)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJFILES) $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~
