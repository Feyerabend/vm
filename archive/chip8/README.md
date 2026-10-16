# Virtual machines

## chip8

Next a virtual machine (or interpreter) that has been widespread and used in many computers, even
calculators. It started its life running on a processor RCA1802[^1], and systems such as COSMAC VIP
from the late 70-ties. Joseph Weisbecker which both invented the physical processor[^2] and the
application of a virtual "processor" CHIP-8, also had a daughter Joyce which is considered as the
first female video game programmer/designer.

[^1]: https://en.wikipedia.org/wiki/RCA_1802.

[^2]: Even before the Intel 4004 (around 1970/1971) Joseph Weisbecker conceived and designed the
processor FRED with only discrete logic. Intel is considered to be the first commercial company
with a processor to the market. However both RCA and Intel didn't at first understand the importance
of this idea what was to become the microprocessor. As a side note the 4004 was first used in
Busicom calculators, but the japanese software was adapted through a mechanism close to "virtual machine".

## Chip8 by Dustin Ryan-Roepsch

There is a much larger story here, much to unpack, but we limit the focus to the virtual machine __*CHIP-8*__.
This implementation here by Dustin Roepsch (among the many thousands there are) of Chip 8 in C, only depends
on Ncurses: https://github.com/dustinroepsch/Chip8-curses. Ncurses is a library dating back into the
80-ties, starting as a "clone" of Curses.[^3] This implies that it can be run in a *terminal window* with
very, very simplified graphics, i.e. text, and also has a nice keyboard connection to C.

This version by Roepsch has the benefit of being rather simple to understand and also few dependencies,
i.e. easy to get up and running on many environments.

[^3]: See: https://en.wikipedia.org/wiki/Curses_(programming_library) and https://en.wikipedia.org/wiki/Ncurses.
Also have a look at ANSI escape codes: https://en.wikipedia.org/wiki/ANSI_escape_code.

To get going, after downloading, try:

```shell
> mkdir build
> cd build
> cmake ../
> make
```

If all went well, you will find in the `build/bin` the compiled binary of Chip8. Start up:

```shell
> ./Chip8 <rom_file>
```

Where you provide your binary sample of a Chip-8 file `<rom_file>`. You can find some at:
https://github.com/kripod/chip8-roms, or search the web.

