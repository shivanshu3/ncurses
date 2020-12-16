add_compile_definitions(_DEFAULT_SOURCE)
add_compile_definitions(_XOPEN_SOURCE=600)
add_compile_definitions(NDEBUG)

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/include)

### Generated C source files

set(CODES_C ${CMAKE_CURRENT_BINARY_DIR}/codes.c)
add_custom_command(
    OUTPUT ${CODES_C}
    COMMAND awk -f ./tinfo/MKcodes.awk bigstrings=1 ../include/Caps ../include/Caps-ncurses > ${CODES_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

set(COMP_CAPTAB_C ${CMAKE_CURRENT_BINARY_DIR}/comp_captab.c)
add_custom_command(
    OUTPUT ${COMP_CAPTAB_C}
    COMMAND sh -e ./tinfo/MKcaptab.sh awk 1 ./tinfo/MKcaptab.awk ../include/Caps ../include/Caps-ncurses > ${COMP_CAPTAB_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

set(COMP_USERDEFS_C ${CMAKE_CURRENT_BINARY_DIR}/comp_userdefs.c)
add_custom_command(
    OUTPUT ${COMP_USERDEFS_C}
    COMMAND sh -e ./tinfo/MKuserdefs.sh awk 1 ../include/Caps ../include/Caps-ncurses > ${COMP_USERDEFS_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

set(EXPANDED_C ${CMAKE_CURRENT_BINARY_DIR}/expanded.c)
add_custom_command(
    OUTPUT ${EXPANDED_C}
    COMMAND sh -e ./tty/MKexpanded.sh > ${EXPANDED_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

set(FALLBACK_C ${CMAKE_CURRENT_BINARY_DIR}/fallback.c)
add_custom_command(
    OUTPUT ${FALLBACK_C}
    COMMAND sh -e ./tinfo/MKfallback.sh /usr/share/terminfo ../misc/terminfo.src tic infocmp > ${FALLBACK_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

### Misc tools

add_executable(make_keys
    ./tinfo/make_keys.c
)

### Generated H files

set(NCURSES_DEF_H ${CMAKE_CURRENT_BINARY_DIR}/ncurses_def.h)
add_custom_command(
    OUTPUT ${NCURSES_DEF_H}
    COMMAND sh ./MKncurses_def.sh ./ncurses_defs > ${NCURSES_DEF_H}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/include
)

set(HASHSIZE_H ${CMAKE_CURRENT_BINARY_DIR}/hashsize.h)
add_custom_command(
    OUTPUT ${HASHSIZE_H}
    COMMAND sh ./MKhashsize.sh ./Caps ./Caps-ncurses > ${HASHSIZE_H}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/include
)

add_custom_target(
    GEN_HEADERS DEPENDS
    ${NCURSES_DEF_H}
    ${HASHSIZE_H}
)

add_library(ncurses STATIC
    # ${CODES_C}
    # ${COMP_CAPTAB_C}
    # ${COMP_USERDEFS_C}
    # ${EXPANDED_C}
    # ${FALLBACK_C}
    base/define_key.c
    base/key_defined.c
    base/keybound.c
    base/keyok.c
    base/legacy_coding.c
    base/lib_addch.c
    base/lib_addstr.c
    base/lib_beep.c
    base/lib_bkgd.c
    base/lib_box.c
    base/lib_chgat.c
    base/lib_clear.c
    base/lib_clearok.c
    base/lib_clrbot.c
    base/lib_clreol.c
    base/lib_color.c
    base/lib_colorset.c
    base/lib_delch.c
    base/lib_delwin.c
    base/lib_dft_fgbg.c
    base/lib_echo.c
    base/lib_endwin.c
    base/lib_erase.c
    base/lib_flash.c
    base/lib_freeall.c
    base/lib_getch.c
    base/lib_getstr.c
    base/lib_hline.c
    base/lib_immedok.c
    base/lib_inchstr.c
    base/lib_initscr.c
    base/lib_insch.c
    base/lib_insdel.c
    base/lib_insnstr.c
    base/lib_instr.c
    base/lib_isendwin.c
    base/lib_leaveok.c
    base/lib_mouse.c
    base/lib_move.c
    base/lib_mvwin.c
    base/lib_newterm.c
    base/lib_newwin.c
    base/lib_nl.c
    base/lib_overlay.c
    base/lib_pad.c
    base/lib_printw.c
    base/lib_redrawln.c
    base/lib_refresh.c
    base/lib_restart.c
    base/lib_scanw.c
    base/lib_screen.c
    base/lib_scroll.c
    base/lib_scrollok.c
    base/lib_scrreg.c
    base/lib_set_term.c
    base/lib_slk.c
    base/lib_slkatr_set.c
    base/lib_slkatrof.c
    base/lib_slkatron.c
    base/lib_slkatrset.c
    base/lib_slkattr.c
    base/lib_slkclear.c
    base/lib_slkcolor.c
    base/lib_slkinit.c
    base/lib_slklab.c
    base/lib_slkrefr.c
    base/lib_slkset.c
    base/lib_slktouch.c
    base/lib_touch.c
    base/lib_ungetch.c
    base/lib_vline.c
    base/lib_wattroff.c
    base/lib_wattron.c
    base/lib_winch.c
    base/lib_window.c
    base/nc_panel.c
    base/new_pair.c
    base/resizeterm.c
    base/safe_sprintf.c
    base/tries.c
    base/use_window.c
    base/version.c
    base/vsscanf.c
    base/wresize.c
    # lib_gen.c
    # lib_keyname.c
    # names.c
    tinfo/access.c
    tinfo/add_tries.c
    tinfo/alloc_entry.c
    tinfo/alloc_ttype.c
    tinfo/captoinfo.c
    tinfo/comp_error.c
    tinfo/comp_expand.c
    tinfo/comp_hash.c
    tinfo/comp_parse.c
    tinfo/comp_scan.c
    tinfo/db_iterator.c
    tinfo/doalloc.c
    tinfo/entries.c
    tinfo/free_ttype.c
    tinfo/getenv_num.c
    tinfo/hashed_db.c
    tinfo/home_terminfo.c
    tinfo/init_keytry.c
    tinfo/lib_acs.c
    tinfo/lib_baudrate.c
    tinfo/lib_cur_term.c
    tinfo/lib_data.c
    tinfo/lib_has_cap.c
    tinfo/lib_kernel.c
    tinfo/lib_longname.c
    tinfo/lib_napms.c
    tinfo/lib_options.c
    tinfo/lib_print.c
    tinfo/lib_raw.c
    tinfo/lib_setup.c
    tinfo/lib_termcap.c
    tinfo/lib_termname.c
    tinfo/lib_tgoto.c
    tinfo/lib_ti.c
    tinfo/lib_tparm.c
    tinfo/lib_tputs.c
    tinfo/lib_ttyflags.c
    tinfo/name_match.c
    tinfo/obsolete.c
    tinfo/parse_entry.c
    tinfo/read_entry.c
    tinfo/read_termcap.c
    tinfo/strings.c
    tinfo/trim_sgr0.c
    tinfo/use_screen.c
    tinfo/write_entry.c
    trace/lib_trace.c
    trace/varargs.c
    trace/visbuf.c
    tty/hardscroll.c
    tty/hashmap.c
    tty/lib_mvcur.c
    tty/lib_tstp.c
    tty/lib_twait.c
    tty/lib_vidattr.c
    tty/tty_update.c
    # unctrl.c
)

add_dependencies(ncurses GEN_HEADERS)

