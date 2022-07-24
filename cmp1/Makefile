
CC			= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES	= cmp1.o
TARGET		= cmp

all: $(TARGET)

cmp1: cmp1.o
	$(CC) $(CFLAGS) -o cmp1 cmp1.o $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~

