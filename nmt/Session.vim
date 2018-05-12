let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/GraduationProject/nmt
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +198 nmt/nmt.py
badd +285 nmt/train.py
badd +448 nmt/model_helper.py
badd +571 nmt/model.py
badd +0 infer.sh
argglobal
silent! argdel *
$argadd nmt/nmt.py
edit nmt/model_helper.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe '1resize ' . ((&lines * 23 + 23) / 47)
exe 'vert 1resize ' . ((&columns * 79 + 79) / 159)
exe '2resize ' . ((&lines * 21 + 23) / 47)
exe 'vert 2resize ' . ((&columns * 79 + 79) / 159)
exe 'vert 3resize ' . ((&columns * 79 + 79) / 159)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 454 - ((14 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
454
normal! 09|
wincmd w
argglobal
if bufexists('infer.sh') | buffer infer.sh | else | edit infer.sh | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 4 - ((3 * winheight(0) + 10) / 21)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4
normal! 020|
wincmd w
argglobal
if bufexists('nmt/nmt.py') | buffer nmt/nmt.py | else | edit nmt/nmt.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 149 - ((9 * winheight(0) + 22) / 45)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
149
normal! 0
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 23 + 23) / 47)
exe 'vert 1resize ' . ((&columns * 79 + 79) / 159)
exe '2resize ' . ((&lines * 21 + 23) / 47)
exe 'vert 2resize ' . ((&columns * 79 + 79) / 159)
exe 'vert 3resize ' . ((&columns * 79 + 79) / 159)
tabnext 1
if exists('s:wipebuf') && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 winminheight=1 winminwidth=1 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
