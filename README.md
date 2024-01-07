# 💩 poop.nvim
A neovim plugin to help embrace the code smell.

![Peek 2024-01-02 20-46](https://github.com/ddl004/poop.nvim/assets/18647028/236436d8-971e-4880-bb3c-15de9e1c6827)

## Features
- Call `:Eject` to eject from the current cursor position!
    - Takes two arguments, `left` and `right`. e.g. `:Eject 💩 💀`
- Option for customizing the projectile ejected and animation properties.
- Optional configuration provided to eject emojis randomly while in insert mode.

## Installation
- This is a remote plugin written in Python, so you will need `pynvim` to install this plugin. See the installation instructions here: [pynvim](https://github.com/neovim/pynvim?tab=readme-ov-file#install).

Install this plugin using your plugin manager. With [vim-plug](https://github.com/junegunn/vim-plug), add:
```
Plug 'ddl004/poop.nvim'
```
and call `:PlugInstall` followed by `:UpdateRemotePlugins`.

### Optional - Tested on Neovim >= v0.10

In your `init.lua` file, add the following to periodically eject when in insert mode.
If you are using [lazy.nvim](https://github.com/folke/lazy.nvim), you can add this to the `config()` function for this plugin. 

You can edit the local variables `emojis` and `period` to modify the emojis ejected and the frequency of the ejection respectively.
```lua
local emojis = {'💩', '💀', '👻'}  -- edit these to include the emojis you want ejected
local period = 10 -- edit this to change the frequency of ejection

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

On previous versions of Neovim, you may run into issues with telescope or other plugins that also include floating windows.
You can use this modified configuration to exclude certain filetypes (e.g. `TelescopePrompt`).
```lua
local emojis = {'💩', '💀', '👻'}  -- edit these to include the emojis you want ejected
local period = 10 -- edit this to change the frequency of ejection
local excluded_fts = {"TelescopePrompt"}

local function is_fts_excluded(buf_ft, excluded_fts)
    for _, ft in ipairs(excluded_fts) do
        if buf_ft == ft then
            return true
        end
    end
    return false
end

vim.on_key(
    function(key)
        if
            vim.api.nvim_get_mode().mode ~= "i" or
                is_fts_excluded(vim.api.nvim_get_option_value("filetype", {}), excluded_fts)
         then
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
These options are used by the `:Eject` command.

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
