# Virtual Machines

## Background

This BASIC *basal/0* takes it inspiration from
[Tiny BASIC](https://en.wikipedia.org/wiki/Tiny_BASIC).
But Tiny BASIC has a very interesting history of its own.


One interesting controversy was between
[Bill Gates](https://en.wikipedia.org/wiki/Bill_Gates) of
computer fame, and
what Gates understood as piracy of
[Micro-Softs'](https://en.wikipedia.org/wiki/Microsoft)
BASIC by hobbyists in the early days of microcomputing.
This might have been a point in history where events highlighted
larger changes in the software industry. On one hand software
started to be more of a product of its own, protected by the
manufacturer/seller by copyright or even patent, but also often
by some intentional obfuscation with the code. On the other hand
the source code wasn’t a separate issue so much when software
was tied to the machines they were made for, when it was the
same company that sold them both. Later when machines themselves
were copied and compatible with the competitors, software became
more of a protected commodity. On another hand again, people
learned from just even reading the source code of others. The
source code itself could improve when there were more people
involved, it could be extended. This was also what some in the
business understood, when they wanted feedback from customers
altering things in the delivered code. Thus, improved software.

In the early days of microcomputing, hobbyists made their own
computers to a large extent themselves. There could be e.g.
schematic for circuits published in a magazine, but then you
had to buy components, solder, etch boards, etc. to manufacture
the computer. A small industry of computer kits emerged, some
even prefabricated to the degree you could buy the kit and plug
in an old teletype for keyboard, and maybe some perforated paper
tape for storage of programs and data, or at a cassette tape.

But programs were hard to get when you finally had the machine.
These machines were so small there really was no market for "applications".
You could make programs yourself, but then you need access to some 
programming language, if you didn't have a lot of time to write
assembly/machine code by hand which often was the case.
As hobbyists, a need for sharing, buying and selling (inexpensive)
software arised, so computer clubs[^homebrew] were one of the forums,
where it could happend. In a generous atmosphere giving and
taking could be done without (much or any) money in between,
not always, but sometimes. Magazines and books had listings
of code that could be entered manually through a keyboard
(or switches) to run on the computer. But also as software has the
characteristic of being copied without losing quality (as in the
case of music and cassette tapes e.g.), software could easily be
distributed without the consent of the author or authors.
This could understandably be understood as some kind of piracy
or robbery from the author. In this case the intention from the
author (programmer) was that software was only to be sold, not
given away. But due to different reasons copies of originally sold
software were distributed among enthusiasts. There reason could be
that it was too expensive to buy, if you could not afford it. It
could be that you only wanted to explore software you didn’t really
needed for a long time, or had no further use for. It could also be
because you didn’t want to pay, when you could get it for free
(or “free” as some would claim).

[^homebrew]: One famous club was the Homebrew Computer Club,
which had members such as
[Steve Wozniak](https://en.wikipedia.org/wiki/Steve_Wozniak) and
[Steve Jobs](https://en.wikipedia.org/wiki/Steve_Jobs),
https://en.wikipedia.org/wiki/Homebrew_Computer_Club


## Altair BASIC

So in this climate reactions from the manufacturers side came to light.
Bill Gates wrote an open letter to those who stole and copied, without
permission, code from his company. He,
[Paul Allen](https://en.wikipedia.org/wiki/Paul_Allen) and
lesser known [Monte Davidoff](https://en.wikipedia.org/wiki/Monte_Davidoff)
had developed
[Altair BASIC](https://en.wikipedia.org/wiki/Altair_BASIC).
He got welcomed feedback from hundreds of people using his BASIC.
But now suddenly he found out something interesting,
but irritating. He formulated his complaint like this in February 3, 1976:[^letter]

> Two surprising things are apparent, however. 1)
> Most of these "users" never bought BASIC (less than 10% of all
> Altair owners have bought BASIC), and 2) The amount of royalties
> we have received from sales to hobbyists makes the time spent
> of Altair BASIC worth less than $2 an hour.

[^letter]: https://en.wikipedia.org/wiki/File:Bill_Gates_Letter_to_Hobbyists_ocr.pdf

He wondered if this was fair, stealing software but paying for hardware?

> As the majority of hobbyists must be aware, most of you steal
> your software.

Bill Gates lamented.


## Tiny BASIC

Well the aftermath is much in echo still today, as you can imagine.
Nearly the same arguments for and against. Reactions reverberated.
But there was something else that happend: the start of software
that *wasn't protected* in the same way in __Tiny BASIC__. Actually
Tiny BASIC was published as a specification already in September 1975,
almost half a year before Gates' letter was published.
[Li-Chen Wang](https://en.wikipedia.org/wiki/Li-Chen_Wang),
who was behind Palo Alto Tiny BASIC, described the core contrasting
idea in the preamble of implementation:

> TINY BASIC FOR INTEL 8080 VERSION 2.0
> BY LI-CHEN WANG MODIFIED AND TRANSLATED
> TO INTEL MNEMONICS BY ROGER RAUSKOLB
> 10 OCTOBER, 1976 @COPYLEFT ALL WRONGS
> RESERVED

Li-Chen Wang pinpointed the ideas in the "COPYLEFT"-slogan:
"ALL WRONGS RESERVED". The later addition by Roger Rauskolb
also reflects the attitude of the upcomming community of adding
contributers names together with what was to become the "license".

This was in stark contrast to the followers of Gates and company.

### Note

*These historical events, small but important enough,
are however not really referenced in later recapitulations
of background for the
[free software movement](https://en.wikipedia.org/wiki/Free_software_movement),
as they might have been.[^rms]*

*Today when software is created, there are more than one way to
go about doing it. Even Microsoft, owning GitHub, acknowledge
the strong community of developers involved in the evolution of software,
openly publishing code. Code under the once demoted ideas of giving out
software free under the ruling of something similar to, or at least not
far from, COPYLEFT.*

[^rms]: Also compare
[Stallmans](https://en.wikipedia.org/wiki/Richard_Stallman)
experience, who formally started the GNU project in 1983,
https://www.gnu.org/gnu/rms-lisp.html.


## Tiny internals

& vm (or abstract machine) Tiny BASIC

On IL
https://troypress.com/the-tiny-basic-interpretive-language-il-and-onions/

More verbatim implementation of IL:
http://www.ittybittycomputers.com/IttyBitty/TinyBasic/TinyBasic.c

Python impl
https://github.com/kevinthecheung/tiny-basic


## Microsoft BASIC

After Altair BASIC, Gates and Allen clearly focused their
interests to build a company for the rising market of
BASIC interpreters. The plethora of newly designed
microcomputers popping up all the time needed a software base,
a system, where BASIC suited perfectly. There were other attempts
such as word processors without a start in a system for
BASIC, but they were relegated to a much smaller market.
Microsoft actually begun working on a APL-language which
was very popular at the time, but scrapped it in the end.

Microsoft BASIC came to dominate the microsystems of the time,
and was (almost) the de facto standard eventually. As an example
of spread, Steve Wozniack wrote an
[Integer BASIC](https://en.wikipedia.org/wiki/Integer_BASIC) for
his Apple II, but it was later replaced with a new version of BASIC
from Microsoft, as Woz din't have the time to complete his floating
point version and Jobs were impatient.

At the start Gates and Allen used an assembler
[MACRO-10](https://en.wikipedia.org/wiki/MACRO-10) on 
a minicomputer PDP-10 to produce codes for especially
the [MOS 6502](https://en.wikipedia.org/wiki/MOS_Technology_6502)
processor. As every computer architecture was a bit different,
adjustments to each variant had to be assembled separately.
There is an article detailing on how Microsoft BASIC works
and even source code from 1978: https://www.pagetable.com/?p=774.
Also some code can be found at: https://github.com/mist64/msbasic.
As timed progressed certain companies got the source code from
Microsoft directly, and adopted it to specific computers themselves.

To avoid problems with the mentioned piracy, a hidden message
from the programmers/ the company (read: Gates and Microsoft)
was embedded in code. This message could be called and showed
up on screen, establishing from where the code originated,
if there were any doubt.
Also read about the protection by Bill Gates on e.g.
Commodore 64:
https://www.c64-wiki.com/wiki/Microsoft#Easter_Egg_.28Microsoft.21.29.
