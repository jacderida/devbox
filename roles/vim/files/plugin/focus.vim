func! Focus(command, vim_command)
    let oldw = winnr()
    silent exe 'wincmd ' . a:vim_command
    let neww = winnr()
    if oldw == neww
        silent exe '!i3-msg focus ' . a:command
    endif
endfunc
