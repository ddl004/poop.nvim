import asyncio
import math

import pynvim


@pynvim.plugin
class Plugin:
    def __init__(self, nvim: pynvim.api.nvim.Nvim):
        self._prefix = "eject_"
        self.nvim = nvim
        self.init_config = {
            "relative": "cursor",
            "row": 0,
            "col": 0,
            "height": 1,
            "width": 2,
            "style": "minimal",
        }
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.settings = {}

    def _update_settings_from_options(self):
        self.settings = {
            "speed": 100.0,
            "angle": 20.0,
            "frames": 120,
            "delay": 0.002,
            "emoji": "💩",
        }
        for config_option in self.settings:
            if self.nvim.vars.get(f"{self._prefix}{config_option}"):
                current = self.settings[config_option]
                self.settings[config_option] = type(current)(
                    self.nvim.vars[f"{self._prefix}{config_option}"]
                )

        speed = self.settings["speed"]
        angle = self.settings["angle"]
        self.settings["x_velocity"] = speed * math.cos(math.radians(angle))
        self.settings["y_velocity"] = speed * math.sin(math.radians(angle))

    async def animate(self, window: pynvim.api.window.Window, direction: int):
        """
        Animates the specified Neovim window.

        Args:
        - window: The Neovim window to be animated.
        - direction: The direction of animation. Use 1 for rightward and -1 for leftward.

        The animation is a simple projectile motion that updates the window's position over time.
        The window closes when the animation is completed

        Note:
        - The animation uses settings from self.settings, including speed, and angle.
        """
        for time_elapsed in range(self.settings["frames"]):
            await asyncio.sleep(self.settings["delay"])
            step = time_elapsed * 0.1
            current_x = direction * (self.settings["x_velocity"] * step)
            current_y = 0 - self.settings["y_velocity"] * step + (0.5 * 9.8 * (step**2))

            # Update the window position
            config = {
                **self.init_config,
                "relative": "cursor",
                "row": current_y / 100,
                "col": current_x / 100,
            }
            self.nvim.async_call(self.nvim.api.win_set_config, window, config)

        # Close the window when done
        self.nvim.async_call(self.nvim.api.win_close, window, True)

    def eject(self, left, right):
        """
        Creates a new buffer, sets its content, and opens a floating window
        displaying the buffer. An async task is added for right and left
        objects.
        """
        for direction, emoji in ((-1, left), (1, right)):
            # Create a new buffer
            buffer = self.nvim.api.create_buf(False, True)
            self.nvim.api.buf_set_lines(buffer, 0, 1, True, [emoji])
            # Create a floating window
            window = self.nvim.api.open_win(buffer, False, self.init_config)
            self.nvim.api.set_option_value("winhl", "Normal:Poop", {"win": window})

            self.loop.create_task(self.animate(window, direction))

    @pynvim.command("Eject", nargs="*", sync=False)
    def eject_handler(self, args):
        """
        :Eject in command mode

        Simulate ejection by moving a 1x1 floating window.
        """
        if self.settings == {}:
            self._update_settings_from_options()

        if len(args) == 1:
            left = right = args[0]
        elif len(args) == 2:
            left = args[0]
            right = args[1]
        else:
            left = right = self.settings["emoji"]

        self.eject(left, right)
