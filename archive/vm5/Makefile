
CC		= gcc
CFLAGS		= -Wall
LDFLAGS		=
OBJFILES	= gc.o gc2.o vm5.o
TARGET		= gc gc2 vm5

all: $(TARGET)

gc: gc.o
	$(CC) $(CFLAGS) -o gc gc.o $(LDFLAGS)

gc2: gc2.o
	$(CC) $(CFLAGS) -o gc2 gc2.o $(LDFLAGS)

vm5: vm5.o
	$(CC) $(CFLAGS) -o vm5 vm5.o $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~

