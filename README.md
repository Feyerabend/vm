# Virtual Machines

Virtual machines samples[^1]. A collection of virtual machines to teach or understand some
ideas and inner workings of virtual machines. They are solely intended for show of principles,
and not for uses in any other way.

[^1]: My best inspiration for the code of simple machines *here* comes from Bartosz Sypytowski:
https://bartoszsypytkowski.com/simple-virtual-machine/ from whom I derived basically the main
code, even though some bugs were corrected and many more additions has been made.

My interest in virtual machines started long time ago, first with *USCD Pascal* on the *Apple II*
sometime around 1980 or 1981 ...

__NOTE: The term "virtual machine" can often be replaced by "emulator", "interpreter" etc. and
perhaps should not be restricted or qualified too much. The idea of an abstraction that separates
the underlying mechanics from the levels above is what should be observed, not a deepend confusion
of concepts which already are ambigious and not very well definied anyway.__

The term "virtual machine" and also "interpreter" has been used for such diverse fields as from the
Apollo Guidance Computer[^2], code from Busicom interpreted[^3] to run on Intel 4004,
and Steve Wozniack routines in SWEET16[^4].

[^2]: This does not verify the reference, but gives general info on AGC,
https://en.wikipedia.org/wiki/Apollo_Guidance_Computer 
[^3]: Neither this verify reference to VM, but general info on Intel 4004,
https://en.wikipedia.org/wiki/Intel_4004
[^4]: SWEET16, https://en.wikipedia.org/wiki/SWEET16 but also in Byte no 11, 1977:
https://archive.org/details/BYTE_Vol_02-11_1977-11_Sweet_16/page/n151/mode/2up

## *From virtual machines to compilers*

### 1. vm1

We start off with a simple virtual stack machine. To not be confused too much, it has been simplified
in many ways. There is no error checking, no warnings, you have to compile the machine if you only
slightly change the program, etc. The idea is to grasp what happends inside the virtual machine
and use code as the main instructive part.

### 2. vm2

### 3. vm3

### 4. chip8

We have alook at an early virtual machine used for games starting in the late 70'ties: CHIP-8. 

### 5. cmp1

### 6. cmp2

### 7. cmp3

