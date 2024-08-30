#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct sc {
	int s;
	int c;
} sc;

// -------------------------------------------

// fwd decl
void printcarry(sc p0, sc p1, sc p2, sc p3, sc p4, sc p5, sc p6, sc p7);
void printsum(sc p0, sc p1, sc p2, sc p3, sc p4, sc p5, sc p6, sc p7, int i, int j);
void printbin(int i);
void printadder(int i, int j, int k);

// -------------------------------------------

// primitives
int not(int x) {
	return !x;
}
int and(int x, int y) {
	return x & y;
}
int or(int x, int y) {
	return x | y;
}
int xor(int x, int y) {
	return x ^ y;
}

// full adder
sc adder(int x, int y, int carry) {
	sc r;
	int s, c;

	c = or(and(xor(x, y), carry), and(x, y));	// c = (c & (x ^ y)) | (x & y)
	s = xor(xor(x, y), carry);			// s = ((x ^ y) ^ c)

	r.s = s;
	r.c = c;
	return r;
}

void add(int i, int j) {
	sc p0, p1, p2, p3, p4, p5, p6, p7;

	p0 = adder((i & 0x01) ? 1 : 0, (j & 0x01) ? 1 : 0, 0);
	p1 = adder((i & 0x02) ? 1 : 0, (j & 0x02) ? 1 : 0, p0.c);
	p2 = adder((i & 0x04) ? 1 : 0, (j & 0x04) ? 1 : 0, p1.c);
	p3 = adder((i & 0x08) ? 1 : 0, (j & 0x08) ? 1 : 0, p2.c);
	p4 = adder((i & 0x10) ? 1 : 0, (j & 0x10) ? 1 : 0, p3.c);
	p5 = adder((i & 0x20) ? 1 : 0, (j & 0x20) ? 1 : 0, p4.c);
	p6 = adder((i & 0x40) ? 1 : 0, (j & 0x40) ? 1 : 0, p5.c);
	p7 = adder((i & 0x80) ? 1 : 0, (j & 0x80) ? 1 : 0, p6.c);

	printcarry(p0, p1, p2, p3, p4, p5, p6, p7);
	printbin(i); printbin(j);
	printsum(p0, p1, p2, p3, p4, p5, p6, p7, i, j);
}


// -------------------------------------------

void printbin(int n) {
	int k;
 	for (int c = 7; c >= 0; c--) {
		k = n >> c;
		if (k & 1)
			printf("1");
		else
			printf("0");
	}
	printf(" <- %d", n);
	printf("\n");
}

void printcarry(sc p0, sc p1, sc p2, sc p3, sc p4, sc p5, sc p6, sc p7) {
	printf("\n\n%d%d%d%d%d%d%d0    (carry)",
			p6.c, p5.c, p4.c, p3.c, p2.c, p1.c, p0.c);
	printf("\n--------\n");
}

void printsum(sc p0, sc p1, sc p2, sc p3, sc p4, sc p5, sc p6, sc p7, int i, int j) {
	printf("========");
	printf("\n%d%d%d%d%d%d%d%d =  %d",
			p7.s, p6.s, p5.s, p4.s, p3.s, p2.s, p1.s, p0.s, (i+j));
	if (p7.c == 1)
		printf("  <-- Overflow! last carry = 1");
	printf("\n");
}

void printadder(int i, int j, int k) {
	sc p;
	p = adder(i, j, k);
	printf("adder(%d, %d) c=%d => s[%d] c=[%d]\n", i, j, k, p.s, p.c);
}

void test() {
	printf("\n\n> logic\n");
	printf("not(0)=%d\n", not(0));
	printf("not(1)=%d\n", not(1));

	printf("and(0, 0)=%d\n", and(0, 0));
	printf("and(0, 1)=%d\n", and(0, 1));
	printf("and(1, 0)=%d\n", and(1, 0));
	printf("and(1, 1)=%d\n", and(1, 1));

	printf("or(0, 0)=%d\n", or(0, 0));
	printf("or(0, 1)=%d\n", or(0, 1));
	printf("or(1, 0)=%d\n", or(1, 0));
	printf("or(1, 1)=%d\n", or(1, 1));

	printf("xor(0, 0)=%d\n", xor(0, 0));
	printf("xor(0, 1)=%d\n", xor(0, 1));
	printf("xor(1, 0)=%d\n", xor(1, 0));
	printf("xor(1, 1)=%d\n", xor(1, 1));

	printf("\n> adder\n");
	printadder(0, 0, 0);
	printadder(0, 1, 0);
	printadder(1, 0, 0);
	printadder(1, 1, 0);
	printadder(0, 0, 1);
	printadder(0, 1, 1);
	printadder(1, 0, 1);
	printadder(1, 1, 1);
}


// -------------------------------------------

int main() {
	add(1, 1);
	add(1, 2);
	add(23, 126);
	add(255, 1);
	test();
	return 0;
}
