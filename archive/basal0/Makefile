
CC		= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES	= vmenkel.o runvm.o
TARGET		= runvm

all: $(TARGET)

runvm: runvm.o vmenkel.o
	$(CC) $(CFLAGS) -o runvm runvm.o vmenkel.o $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~
