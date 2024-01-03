# 💩 poop.nvim
A neovim plugin to help embrace the code smell.

![Peek 2024-01-02 20-46](https://github.com/ddl004/poop.nvim/assets/18647028/236436d8-971e-4880-bb3c-15de9e1c6827)

## Features
- Call `:Eject` to eject from the current cursor position!
- By adding the `on_key` call in your config file, the poop will be ejected randomly on every key press in insert mode, with frequency inversely proportional to the value of `eject_period`.
- Option for customizing the projectile ejected.

## Installation
- This is a remote plugin written in Python, so you will need `pynvim` to install this plugin. See the installation instructions here: [pynvim](https://github.com/neovim/pynvim?tab=readme-ov-file#install).

Install this plugin using your plugin manager. With [vim-plug](https://github.com/junegunn/vim-plug), add:
```
Plug 'ddl004/poop.nvim'
```
and call `:PlugInstall` followed by `:UpdateRemotePlugins`.

### Optional - Tested on Neovim >= v0.10

In your `init.lua` file, add the following to periodically eject when in insert mode:
```lua
vim.on_key(function(key)
    if vim.api.nvim_get_mode().mode ~= 'i' then return end
    vim.schedule_wrap(function()
        vim.cmd.Eject("use_period")
    end)() 
end, nil)
```

If you are using `init.vim` instead:
```vim
lua << EOF
vim.on_key(function(key)
    if vim.api.nvim_get_mode().mode ~= 'i' then return end
    vim.schedule_wrap(function()
        vim.cmd.Eject("use_period")
    end)() 
end, nil)
EOF
```

## Configuration
### Options
| Option         | Description                                                                                  | Default |
|----------------|----------------------------------------------------------------------------------------------|---------|
| `eject_emoji`  | The emoji that is ejected.                                                                   | 💩      |
| `eject_speed`  | Increase/decrease to change the speed of the projectile being ejected.                       | 100     |
| `eject_angle`  | Angle at which the projectile is ejected.                                                    | 20      |
| `eject_period` | Increase to lower the frequency of ejection, or lower to increase the frequency of ejection. | 10      |

You can set it these in your `init.lua` as follows:
```lua
vim.g.eject_emoji = '💩'
```
or in `init.vim`:
```vim
let g:eject_emoji = '💩'
```

## License
This project is licensed under the MIT License.

## Related
This project was inspired by [duck.nvim](https://github.com/tamton-aquib/duck.nvim)
