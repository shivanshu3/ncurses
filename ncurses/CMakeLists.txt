add_compile_definitions(_DEFAULT_SOURCE)
add_compile_definitions(_XOPEN_SOURCE=600)
add_compile_definitions(NDEBUG)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 14)

if(MSVC)
    add_compile_options(/WX)
else()
    add_compile_options(-Werror)
endif()

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/include)

if (MSVC)
    set(PREPROCESSOR_CMD "cl /E")
else()
    set(PREPROCESSOR_CMD "gcc -E")
endif()

if (MSVC)
    set(EXE_EXT ".exe")
else()
    set(EXE_EXT "")
endif()

set(PREPROCESSOR_ARGS "-DHAVE_CONFIG_H -I${CMAKE_CURRENT_BINARY_DIR} -I${CMAKE_CURRENT_SOURCE_DIR} -I${CMAKE_SOURCE_DIR}/include -D_DEFAULT_SOURCE -D_XOPEN_SOURCE=600 -DNDEBUG")

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
    COMMAND sh -e ${CMAKE_CURRENT_SOURCE_DIR}/tinfo/MKcaptab.sh awk 1 ${CMAKE_CURRENT_SOURCE_DIR}/tinfo/MKcaptab.awk ${CMAKE_SOURCE_DIR}/include/Caps ${CMAKE_SOURCE_DIR}/include/Caps-ncurses > ${COMP_CAPTAB_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    DEPENDS ${MAKE_HASH_PATH}
)

set(COMP_USERDEFS_C ${CMAKE_CURRENT_BINARY_DIR}/comp_userdefs.c)
add_custom_command(
    OUTPUT ${COMP_USERDEFS_C}
    COMMAND sh -e ${CMAKE_CURRENT_SOURCE_DIR}/tinfo/MKuserdefs.sh awk 1 ${CMAKE_SOURCE_DIR}/include/Caps ${CMAKE_SOURCE_DIR}/include/Caps-ncurses > ${COMP_USERDEFS_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    DEPENDS ${MAKE_HASH_PATH}
)

set(EXPANDED_C ${CMAKE_CURRENT_BINARY_DIR}/expanded.c)
add_custom_command(
    OUTPUT ${EXPANDED_C}
    COMMAND sh -e ${CMAKE_CURRENT_SOURCE_DIR}/tty/MKexpanded.sh "${PREPROCESSOR_CMD}" ${PREPROCESSOR_ARGS} > ${EXPANDED_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

set(FALLBACK_C ${CMAKE_CURRENT_BINARY_DIR}/fallback.c)
add_custom_command(
    OUTPUT ${FALLBACK_C}
    COMMAND sh -e ./tinfo/MKfallback.sh /usr/share/terminfo ../misc/terminfo.src tic infocmp > ${FALLBACK_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

set(NAMES_C ${CMAKE_CURRENT_BINARY_DIR}/names.c)
add_custom_command(
    OUTPUT ${NAMES_C}
    COMMAND awk -f ./tinfo/MKnames.awk bigstrings=1 ../include/Caps ../include/Caps-ncurses > ${NAMES_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
add_custom_target(NAMES_C_TARGET DEPENDS ${NAMES_C})

set(UNCTRL_C ${CMAKE_CURRENT_BINARY_DIR}/unctrl.c)
add_custom_command(
    OUTPUT ${UNCTRL_C}
    COMMAND echo | awk -f ./base/MKunctrl.awk bigstrings=1 > ${UNCTRL_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

set(CURSES_H ${CMAKE_CURRENT_BINARY_DIR}/curses.h)

set(LIB_GEN_C ${CMAKE_CURRENT_BINARY_DIR}/lib_gen.c)
add_custom_command(
    OUTPUT ${LIB_GEN_C}
    COMMAND sh -e ./base/MKlib_gen.sh "${PREPROCESSOR_CMD} ${PREPROCESSOR_ARGS}" "awk" generated < ${CURSES_H} > ${LIB_GEN_C}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${CURSES_H}
)

### Misc tools

set(MAKE_KEYS_PATH ${CMAKE_CURRENT_BINARY_DIR}/make_keys${EXE_EXT})
add_executable(make_keys
    ./tinfo/make_keys.c
)
set_target_properties(make_keys
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_BINARY_DIR}
)
add_dependencies(make_keys
    NAMES_C_TARGET
    NCURSES_DEF_H_TARGET
    HASHSIZE_H_TARGET
    CURSES_H_TARGET
)

set(MAKE_HASH_PATH ${CMAKE_CURRENT_BINARY_DIR}/make_hash${EXE_EXT})
add_executable(make_hash
    ./tinfo/make_hash.c
)
set_target_properties(make_hash
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_BINARY_DIR}
)
add_dependencies(make_hash
    NCURSES_DEF_H_TARGET
    HASHSIZE_H_TARGET
)

### Misc generated files

set(KEYS_LIST ${CMAKE_CURRENT_BINARY_DIR}/keys.list)
add_custom_command(
    OUTPUT ${KEYS_LIST}
    COMMAND sh ./tinfo/MKkeys_list.sh ../include/Caps ../include/Caps-ncurses | sort > ${KEYS_LIST}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

### Generated H files

set(NCURSES_DEF_H ${CMAKE_CURRENT_BINARY_DIR}/ncurses_def.h)
add_custom_command(
    OUTPUT ${NCURSES_DEF_H}
    COMMAND sh ./MKncurses_def.sh ./ncurses_defs > ${NCURSES_DEF_H}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/include
)
add_custom_target(NCURSES_DEF_H_TARGET DEPENDS ${NCURSES_DEF_H})

set(HASHSIZE_H ${CMAKE_CURRENT_BINARY_DIR}/hashsize.h)
add_custom_command(
    OUTPUT ${HASHSIZE_H}
    COMMAND sh ./MKhashsize.sh ./Caps ./Caps-ncurses > ${HASHSIZE_H}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/include
)
add_custom_target(HASHSIZE_H_TARGET DEPENDS ${HASHSIZE_H})

set(INIT_KEYTRY_H ${CMAKE_CURRENT_BINARY_DIR}/init_keytry.h)
add_custom_command(
    OUTPUT ${INIT_KEYTRY_H}
    COMMAND ${MAKE_KEYS_PATH} ${KEYS_LIST} > ${INIT_KEYTRY_H}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/include
    DEPENDS ${MAKE_KEYS_PATH} ${KEYS_LIST}
)
add_custom_target(INIT_KEYTRY_H_TARGET DEPENDS ${INIT_KEYTRY_H})
add_dependencies(INIT_KEYTRY_H_TARGET make_keys)

set(PARAMETRIZED_H ${CMAKE_CURRENT_BINARY_DIR}/parametrized.h)
add_custom_command(
    OUTPUT ${PARAMETRIZED_H}
    COMMAND sh ./MKparametrized.sh ./Caps ./Caps-ncurses > ${PARAMETRIZED_H}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/include
)

add_custom_command(
    OUTPUT ${CURSES_H}
    COMMAND cat curses.head > ${CURSES_H}
    COMMAND sh ./MKkey_defs.sh ./Caps ./Caps-ncurses >> ${CURSES_H}
    COMMAND sh -c 'if test \"chtype\" = \"cchar_t\" \; then cat ./curses.wide >> ${CURSES_H} \; fi'
    COMMAND cat ./curses.tail >> ${CURSES_H}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/include
)
add_custom_target(CURSES_H_TARGET DEPENDS ${CURSES_H})

# Represents all generated headers
add_custom_target(
    GEN_HEADERS DEPENDS
    ${NCURSES_DEF_H}
    ${HASHSIZE_H}
    ${INIT_KEYTRY_H}
    ${PARAMETRIZED_H}
)
add_dependencies(GEN_HEADERS INIT_KEYTRY_H_TARGET)

add_library(ncurses STATIC
    ${CODES_C}
    ${COMP_CAPTAB_C}
    ${COMP_USERDEFS_C}
    ${EXPANDED_C}
    ${FALLBACK_C}
    ${NAMES_C}
    ${UNCTRL_C}
    ${LIB_GEN_C}
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
    # lib_keyname.c
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
)

add_dependencies(ncurses GEN_HEADERS)

