import asyncio
import math
from random import randint

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
        self.settings = None

    def _update_settings_from_options(self):
        self.settings = {
            "speed": 100,
            "angle": 20.0,
            "period": 10,
            "emoji": "💩",
        }
        for config_option in self.settings:
            if self.nvim.vars.get(f"{self._prefix}{config_option}"):
                if config_option == "emoji":
                    self.settings[config_option] = self.nvim.vars[
                        f"{self._prefix}{config_option}"
                    ]
                else:
                    self.settings[config_option] = float(
                        self.nvim.vars[f"{self._prefix}{config_option}"]
                    )

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
        speed, angle = (
            self.settings["speed"],
            self.settings["angle"],
        )
        time_step = 0.1
        horizontal_velocity = speed * math.cos(math.radians(angle))
        vertical_velocity = speed * math.sin(math.radians(angle))

        for time_elapsed in range(120):
            await asyncio.sleep(0.002)
            current_x = direction * (horizontal_velocity * (time_elapsed * time_step))
            current_y = (
                0
                - vertical_velocity * (time_elapsed * time_step)
                + (0.5 * (9.8) * (time_elapsed * time_step) ** 2)
            )

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

    def eject(self):
        """
        Creates a new buffer, sets its content, and opens a floating window
        displaying the buffer. An async task is added for right and left
        objects.
        """
        for direction in (-1, 1):
            # Create a new buffer
            buffer = self.nvim.api.create_buf(False, True)
            self.nvim.api.buf_set_lines(buffer, 0, 1, True, [self.settings["emoji"]])
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
        if self.settings is None:
            self._update_settings_from_options()

        use_period = False
        if len(args):
            use_period = args[0] == "use_period"
        should_eject = randint(0, self.settings["period"]) == 0
        if not use_period or should_eject:
            self.eject()
