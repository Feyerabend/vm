# Virtual Machines


## logging

*This section is intended to highlight that the principles of
application and system development should not be compartmentalized.
Tools like loggers, commonly used in systems, can also be highly
beneficial in other applications. For example, integrating a logger
into an editor can be very useful.*

As previously stated, logging is a tool with many aspects and uses.
Here, we demonstrate this by using a *line editor*. A line editor was
once very common in the past. It was easy to implement and versatile,
making it effective for editing text files. As long as the files
weren’t too large, it wasn’t too difficult to use. We will not delve
into the specifics of line editors, as that is not our aim here.
Instead, we want to illustrate how logging can benefit even editors.
In this case, you can have the *entire history of edits* saved. From
the saved file, you can, in principle, work backwards in steps, undo
or redo edits. The log would contain enough information to restore
the session and continue from where you left off, even if you just
quit the editor. Todays computer may be fast enough to not corrupt
saving the log, so in principal it should work ok. That is just
one idea that could be implemented even in editors of today.

### run

```shell
> python3 ed.py -i trad.txt
```

![Line editor](../assets/images/ed.png)

### line editor

We start off with a very simple line editor 'ed.py'. It can load text
files, view them, insert a line, delete a line, edit a line, save the
file. The bare necessities.

In short `load_file` loads the content of the file into `self.lines`,
while `save_file` saves the current lines to the current file. The
`view` displays the content of the file with line numbers. The
functions take a more closer approach `edit` replaces a specific line
with new content, `insert` inserts new content at a specific line, and
`delete` deletes a specific line. Next `run` is the main loop to handle
user commands "view, edit, insert, delete, load, save, exit".

### run

```shell
> python3 ed2.py -i trad.txt
```

![Line editor](../assets/images/ed2.png)

### line editor with logger

The second editor 'ed2.py' includes a built-in *logger*, which distinguishes it
from 'ed.py'. Despite this improvement, the functionality remains largely
similar to the previous version. There are always room for improvement,
but cut off with regards to pegagogical values.[^flawed] The 'log.txt'
is hardcoded for every text that runs through the editor. Logs are usually
custom-built and may vary in format.

[^flawed]: The logs are significantly flawed and redundant. The log file
can grow immensely in proportion to the files they track. For example,
a saved file is fully represented in the log file both when it is
loaded and saved.

### view log

```shell
> cat log.txt
```

```log
2024-07-27 09:47:12 | LOAD | NAME = trad.txt
2024-07-27 09:47:12 | LOAD | 0 = “True happiness is to enjoy the present,
2024-07-27 09:47:12 | LOAD | 1 = without anxious dependence upon the future,
2024-07-27 09:47:12 | LOAD | 2 = not to amuse ourselves with either hopes or fears
2024-07-27 09:47:12 | LOAD | 3 = but to rest satisfied with what we have,
2024-07-27 09:47:12 | LOAD | 4 = which is sufficient, for he that is so wants nothing.
2024-07-27 09:47:12 | LOAD | 5 = The greatest blessings of mankind are within us
2024-07-27 09:47:12 | LOAD | 6 = and within our reach. A wise man is content with his lot,
2024-07-27 09:47:12 | LOAD | 7 = whatever it may be, without wishing for what he has not.”
2024-07-27 09:48:31 | INSERT | 8 = Seneca, 'On Discursiveness in Reading'
2024-07-27 09:48:39 | SAVE | NAME = trad.txt
2024-07-27 09:48:39 | SAVE | 0 = “True happiness is to enjoy the present,
2024-07-27 09:48:39 | SAVE | 1 = without anxious dependence upon the future,
2024-07-27 09:48:39 | SAVE | 2 = not to amuse ourselves with either hopes or fears
2024-07-27 09:48:39 | SAVE | 3 = but to rest satisfied with what we have,
2024-07-27 09:48:39 | SAVE | 4 = which is sufficient, for he that is so wants nothing.
2024-07-27 09:48:39 | SAVE | 5 = The greatest blessings of mankind are within us
2024-07-27 09:48:39 | SAVE | 6 = and within our reach. A wise man is content with his lot,
2024-07-27 09:48:39 | SAVE | 7 = whatever it may be, without wishing for what he has not.”
2024-07-27 09:48:39 | SAVE | 8 = Seneca, 'On Discursiveness in Reading'
```


### A log viewer

Long logs can be challenging to navigate. A dedicated viewer `viewlog.html`
with filtering or sorting options can make this process easier. While text
files may not present many obstacles, programming languages or machine code
often benefit significantly from such specialized tools.

![Log viewer](../assets/images/viewlog.png)


### A playback viewer

In this case with a line editor that have a *recording log*, a *playback
viewer* `playlog.html` will illustrate how a textfile gets created. As can
be understood from this, versioning, alternate copies, and other reconizable
properties from e.g. versioning software could in principle also be added.

![Log viewer](../assets/images/playlog.png)

Thus logging is often a system tool, but it capture ideas that can be use
in many other ways.



## Assembling & disassembling

Taking an assembler from previous, we can turn it into something which
analyses our "machine code", a disassembler. It reverses the process,
takes the integers and turn them into easier to understandable mnemonics,
the "assembly language".


### Disassembler: disasm.py

```code
38,13,0,28,0,12,0,27,1,5,11,16,27,1,30,
0,24,12,0,27,1,31,28,3,12,3,29,0,2,0,12,
0,14,0,18,30,0,24,24,27,10,29,0,2,0,14,
0,22,8
```

```assembly
L0:
	LDARG 0     # 013 000
	ST 0        # 028 000
	LD 0        # 012 000
	SET 1       # 027 001
	EQ          # 005
	JPZ :L16    # 011 016
	SET 1       # 027 001
	STORE 0     # 030 000
	RET         # 024
L16:
	LD 0        # 012 000
	SET 1       # 027 001
	SUB         # 031
	ST 3        # 028 003
	LD 3        # 012 003
	STARG 0     # 029 000
	CALL :L0    # 002 000
	LD 0        # 012 000
	LOAD 0      # 014 000
	MUL         # 018
	STORE 0     # 030 000
	RET         # 024
	RET         # 024
START:
	SET 10		# 027 010
	STARG 0		# 029 000
	CALL :L0	# 002 000
	LOAD 0		# 014 000
	PRINT		# 022
	HALT		# 008
```