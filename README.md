# neovim-fsi


A Neovim plugin that provides integration with F# Interactive via the 
Neovim terminal emulator. Specifically, it provides the following commands

* open new fsi session in split window (`:FsiOpen`),
* send buffer to fsi  (`:FsiSendBuffer`),
* send visual selection to fsi  (`:FsiSendSelection`),
* send line to fsi (`:FsiSendLine`).


## Prerequisites

* Neovim with Python3 support and the `pynvim` package 
installed (`pip3 install pynvim`);
* F# Interactive (fsi.exe or fsharpi)

## Install

Using [vim-plug](https://github.com/junegunn/vim-plug):

```
Plug 'buntec/neovim-fsi', { 'do': ':UpdateRemotePlugins' }
```


## Settings

You can override the default window height (12):

```
let g:neovim_fsi_window_height = 15
```
