# 💩 poop.nvim
A neovim plugin to help embrace the code smell.

![Peek 2024-01-02 20-46](https://github.com/ddl004/poop.nvim/assets/18647028/236436d8-971e-4880-bb3c-15de9e1c6827)

## Features
- Call `:Eject` to eject from the current cursor position!
- Option for customizing the projectile ejected.

## Installation
- This is a remote plugin written in Python, so you will need `pynvim` to install this plugin. See the installation instructions here: [pynvim](https://github.com/neovim/pynvim?tab=readme-ov-file#install).

Install this plugin using your plugin manager. With [vim-plug](https://github.com/junegunn/vim-plug), add:
```
Plug 'ddl004/poop.nvim'
```
and call `:PlugInstall` followed by `:UpdateRemotePlugins`.

### Optional - Tested on Neovim >= v0.10

In your `init.lua` file, add the following to periodically eject when in insert mode. This also gives you the option to eject different types of emojis.
```lua
local emojis = {'💩', '💀', '👻'}
local period = 10
vim.on_key(
    function(key)
        if vim.api.nvim_get_mode().mode ~= "i" then
            return
        end
        vim.schedule_wrap(
            function()
                local left = emojis[math.random(1, #emojis)]
                local right = emojis[math.random(1, #emojis)]
                local should_eject = math.random(1, period) == 1

                if should_eject then
                    vim.cmd.Eject(left, right)
                end
            end
        )()
    end,
    nil
)
```

## Configuration
### Options
| Option         | Description                                                            | Default |
|----------------|------------------------------------------------------------------------|---------|
| `eject_emoji`  | The default emoji that is ejected.                                     | 💩      |
| `eject_speed`  | Increase/decrease to change the speed of the projectile being ejected. | 100     |
| `eject_angle`  | Angle at which the projectile is ejected.                              | 20      |
| `eject_frames` | Number of frames in the animation.                                     | 120     |
| `eject_delay`  | Delay in seconds between each frame.                                   | 0.002   |


You can set these in your `init.lua` as follows:
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
