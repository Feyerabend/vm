![Sample of matrix printer output](../assets/images/matrixprint.png)

# Background

## Xerox Parc

In the early 1970s, Xerox Corporation embarked on an ambitious
project to create a research center that would push the
boundaries of technology far beyond their core copier business.
This vision led to the establishment of the
*Palo Alto Research Center*, commonly known as *PARC*[^parc],
in 1970.

One of PARC's most notable early achievements was the development
of the *Alto* computer in 1973. It featured a graphical user 
interface (GUI), which was a revolutionary concept at the time,
allowing users to interact with the computer using *windows*,
*icons*, and *menus*, and navigate with a *mouse*. Although
the Alto was never sold commercially, it profoundly influenced
the design of future personal computers (e.g. the future Macintosh
and Windows operating systems).

Parallel to the development of the Alto, PARC invented *Ethernet*,
a networking technology that allowed multiple computers to
communicate over a shared coaxial cable. This innovation,
developed in 1973, laid the groundwork for local area networks
(LANs), which became the backbone of modern computer networking.

Alan Kay, another visionary at PARC, led the development of
*Smalltalk*, an object-oriented programming language. Beginning
in the early 1970s, Smalltalk introduced (with other languages)
a new way of thinking about software design by using objects
to represent both data and behavior.

In the realm of text editing, Charles Simonyi at PARC developed
the Bravo text editor, which was one of the first applications
to use the *WYSIWYG* (What You See Is What You Get) principle.
This meant that what users saw on their screen was exactly how
the document would appear when printed. Bravo, developed in the
mid-1970s, set the standard for modern word processors and paved
the way for software like the ubiquitous Microsoft Word.

[^parc]: https://en.wikipedia.org/wiki/Palo_Alto_Research_Center


### Laser printers

While PARC was pioneering these revolutionary computing technologies,
Gary Starkweather was working on adapting laser technology for
printing. Transferring from Xerox's Rochester facility to PARC
in 1971, Starkweather began developing what would become the
laser printer. By 1972, he had created a working prototype, and
this breakthrough led to the commercialization of laser printing
technology. In 1977, Xerox released the 9700 Electronic Printing
System, capable of printing at a remarkable speed of 120 pages
per minute with the resolution of 300 dpi. This innovation
transformed the printing industry, making high-speed, high-quality
printing *accessible* for office automation and desktop
publishing.[^printer]

[^printer]: https://www.historyofinformation.com/detail.php?entryid=1112

### Software for printing: InterPress[^interpress]

While employed at PARC, John Warnock and Charles Geschke worked
on a project called *Interpress*. It was designed to precisely
describe the layout and contents of printed pages, making it a
precursor to *PostScript*. Interpress aimed to facilitate
high-quality printing by providing a detailed and
*device-independent specification of documents*.
Xerox did not fully capitalize on its potential, or maybe
didn't saw larger markets where it could be used.

[^interpress]: https://en.wikipedia.org/wiki/Interpress.
On both Postscript and InterPress:
https://www.tech-insider.org/unix/research/1985/0301.html

![Print from LaTeX through PS](../assets/images/ps.png)

## Adobe Systems, PostScript and DTP

In 1982, Warnock and Geschke, two researchers from PARC,
left Xerox to found Adobe Systems. Recognizing the need for
such a technology, they decided to develop a new, more versatile
page description language, which they named *PostScript*[^ps].

[^ps]: https://en.wikipedia.org/wiki/PostScript

PostScript was designed to be beside device-independent it could
describe text, images, and graphics on any printer or display
device. It used much many of the same concepts of contemporary
stack-based programming languages.

The introduction of PostScript in 1984 revolutionized the printing
and publishing industries. It allowed for the creation of complex,
high-quality documents with precise layouts that could be printed
exactly as they appeared on the screen.

Prior to its development, printers required pre-defined typographic
fonts, or in the case of cheap matrix printers: what was built in.
PostScript enabled users to define text as graphic objects,
described mathematically with straight and curved lines.
Adobe introduced Type 1 fonts for PostScript. These fonts were
scalable, used Bézier curves to describe the shapes of characters,
allowing for high-quality scaling and rendering at any size and
resolution. But Abode also kept a secret: the details of the
implementation of type setting, especially with small size fonts,
was (and still is) *not* public. Types are mostly copyrighted and
owned by type foundries. Their use can be restricted and often
involves certain costs. (However, an early exception here was Donald
E. Knuths 'Metafont' in TeX[^tex].)

[^tex]: https://en.wikipedia.org/wiki/TeX and
https://en.wikipedia.org/wiki/Metafont.


### Apple & Adobe

The relationship between Xerox PARC's innovations and PostScript
became even more significant through Adobe's partnership with
[Apple](APPLE.md). In 1985, Apple launched the LaserWriter, the
first PostScript-based laser printer. The collaboration was
instrumental in the rise of desktop publishing (DTP).

But the LaserWriter was expensive, almost $7,000[^hist] USD at
the time. The investment could though be balanced against
much more expensive hire of labour, professional equipment
and the cost of time for a final product. The lower the cost
of the printer, the more attractive the alternative was.[^sidenote]

One more element was required for the DTP revolution to take off:
*PageMaker*.[^pagemaker] PageMaker, developed by Aldus
Corporation[^aldus] and released in 1985, was one of the
first desktop publishing software applications. It changed the
publishing industry by enabling users to create professional-quality
documents with flowing text, pictures and graphics integrated
on the same page. PageMaker's compatibility with Apple Macintosh
and its use of the PostScript page description language were
pivotal in making desktop publishing accessible to a wider audience.
Naturally, IBM, Microsoft, and other companies wanted to be
part of this change as well, and soon there were versions of
LaserWriters, PageMaker, and Windows on top of a PC that
were more or less competitive.

[^sidenote]: When I was a student, sometime in the 1980s,
the option of writing an essay and obtaining a laser-printed
version wasn’t exactly feasible. A cheap electronic typewriter
was the norm back then. However, as the 1990s approached and
I could get a printout on a laser printer, a LaserWriter II
using a Macintosh Plus, I discovered that when the printout
went wrong, some strange characters were generated on the
paper: this was actually PostScript. Remarkable! I actually
understood something about this .. But far from owning a
printer, at least I could borrow it for a few hours.

[^hist]: https://rgbcmyk.com.ar/en/history-of-postscript/
[^pagemaker]: https://en.wikipedia.org/wiki/Adobe_PageMaker
https://web.archive.org/web/20070709042131/http://www.makingpages.org/pagemaker/history/
[^aldus]: https://en.wikipedia.org/wiki/Aldus_Corporation


### Consequences

Thus the combination of Macintosh, laser printers and applications
such as PageMaker changed the scene of small scale publishing.

*"Democratization" of publishing*: These technologies lowered the
barriers to entry in the publishing industry. Small businesses,
magazines, and other publications could now produce high-quality
printed materials without the need for costly prepress services.

*Efficiency in prepress*: The combination of PageMaker and
PostScript-enabled laser printers streamlined the prepress
process. Designers could create, edit, and proof their layouts
on screen, printing them directly from their computers. This
eliminated the need for manual typesetting and paste-up
processes, which were labor-intensive and time-consuming.

*Cost reduction*: By enabling in-house production of professional
documents, businesses could significantly cut costs associated
with outsourcing prepress and printing tasks. This was especially
beneficial for small publishers and corporate marketing departments.

*Productivity*: The ability to see immediate results of
design changes on-screen and print high-quality proofs rapidly
increased productivity. Iterations could be completed much faster
than with traditional methods.

*Desktop Publishing (DTP)*: Much of the synergy between PageMaker,
PostScript, laser printers, and the Macintosh gave rise to
the desktop publishing industry.


## References

Brock, David C., "PostScript: A Digital Printing Press"
https://computerhistory.org/blog/postscript-a-digital-printing-press/

"Laser printing," Wikipedia: The Free Encyclopedia, Wikimedia Foundation.
Available at: https://en.wikipedia.org/wiki/Laser_printing (Accessed: 17 July 2024).

"LaserWriter," Wikipedia: The Free Encyclopedia, Wikimedia Foundation.
Available at: https://en.wikipedia.org/wiki/LaserWriter  (Accessed: 17 July 2024).

"PostScript," Wikipedia: The Free Encyclopedia, Wikimedia Foundation.
Available at: https://en.wikipedia.org/wiki/PostScript (Accessed: 17 July 2024).

Warnock, John, "Simple Ideas That Changed Printing and Publishing",
*Proceedings of the American Philosophical Society*, no. 156, 2012, pp. 363-378.

Reference manual 2nd ed:
https://www.os2site.com/sw/dev/openwatcom/docs/postscript_level_2_reference_manual.pdf

PostScript and Forth:
https://dl.acm.org/doi/pdf/10.1145/122077.122083

