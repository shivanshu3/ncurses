import sys
import tempfile
import os

if len(sys.argv) != 2:
    print('Bad usage.', file=sys.stderr)
    sys.exit(1)

ppCmd = sys.argv[1]

print(
"""
/* generated by MKexpanded.sh */
#define NEED_NCURSES_CH_T 1
#include <curses.priv.h>

#ifndef CUR
#define CUR SP_TERMTYPE
#endif

#if NCURSES_EXPANDED
""")
sys.stdout.flush()


ppSrcContents = \
"""
#include <ncurses_cfg.h>
#undef NCURSES_EXPANDED /* this probably is set in ncurses_cfg.h */
#include <curses.priv.h>
/* these are names we'd like to see */
#undef ALL_BUT_COLOR
#undef PAIR_NUMBER
#undef TRUE
#undef FALSE
/* this is a marker */
IGNORE
NCURSES_EXPORT(void)
_nc_toggle_attr_on (attr_t *S, attr_t at)
{
	toggle_attr_on(*S,at);
}

NCURSES_EXPORT(void)
_nc_toggle_attr_off (attr_t *S, attr_t at) 
{
	toggle_attr_off(*S,at);
}

NCURSES_EXPORT(int)
NCURSES_SP_NAME(_nc_DelCharCost) (NCURSES_SP_DCLx int count)
{
	return DelCharCost(SP_PARM, count);
}

NCURSES_EXPORT(int)
NCURSES_SP_NAME(_nc_InsCharCost) (NCURSES_SP_DCLx int count)
{
	return InsCharCost(SP_PARM, count);
}

NCURSES_EXPORT(void)
NCURSES_SP_NAME(_nc_UpdateAttrs) (NCURSES_SP_DCLx CARG_CH_T c)
{
	UpdateAttrs(SP_PARM, CHDEREF(c));
}

@if_NCURSES_SP_FUNCS
NCURSES_EXPORT(int)
_nc_DelCharCost (int count)
{
	return NCURSES_SP_NAME(_nc_DelCharCost) (CURRENT_SCREEN, count);
}

NCURSES_EXPORT(int)
_nc_InsCharCost (int count)
{
	return NCURSES_SP_NAME(_nc_InsCharCost)(CURRENT_SCREEN, count);
}

NCURSES_EXPORT(void)
_nc_UpdateAttrs (CARG_CH_T c)
{
	NCURSES_SP_NAME(_nc_UpdateAttrs)(CURRENT_SCREEN,c);
}
@endif
"""

ppSrcFile = tempfile.NamedTemporaryFile(mode='w+t', suffix='.c')
print(ppSrcContents, file=ppSrcFile)
ppSrcFile.flush()

ppOutFile = tempfile.NamedTemporaryFile(mode='w+t', suffix='.i')

exitResult = os.system(ppCmd + ' ' + ppSrcFile.name + ' > ' + ppOutFile.name)
exitCode = os.WEXITSTATUS(exitResult)

if exitCode != 0:
    sys.exit(exitCode)

sedScript = \
"""
sed -e '1,/^IGNORE$/d' -e 's/^@/#/' -e 's/^#[ 	]*if_/#if /' -e "s,$TMP,expanded.c,"
"""

exitResult = os.system('cat ' + ppOutFile.name + ' | ' + sedScript)
exitCode = os.WEXITSTATUS(exitResult)

if exitCode != 0:
    sys.exit(exitCode)

print(
"""
#else /* ! NCURSES_EXPANDED */
NCURSES_EXPORT(void) _nc_expanded (void) { }
#endif /* NCURSES_EXPANDED */
""")
sys.stdout.flush()

