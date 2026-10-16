# RETURN without GOSUB is not a compile error. BASIC cannot know,
# since a GOTO might have jumped here from inside a subroutine. The
# machine knows at run time.
PRINT "before"
RETURN
