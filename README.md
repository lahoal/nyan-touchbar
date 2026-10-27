# Nyan Cat for the Touch Bar

*[Leer en español](README.es.md)*

An animated Nyan Cat for the MacBook Pro Touch Bar, built as a [BetterTouchTool](https://folivora.ai) plugin. It puts on different accessories depending on what you're doing.

![Nyan Cat cycling through its variants on a real Touch Bar](previews/touchbar-real.gif)

*Recorded on a real Touch Bar. The full bar looks like this (the calendar event name was replaced for privacy):*

![Full Touch Bar with the cat on the left](previews/touchbar-real.png)

## Variants

| | State | How it's detected |
|---|---|---|
| ![](previews/music.gif) | **Music playing**: floating notes | BTT variable `BTTCurrentlyPlaying` |
| ![](previews/terminal.gif) | **Terminal or code editor in front**: matrix rainbow and hacker shades | Frontmost app: Terminal, iTerm2, Warp, Ghostty, kitty, Alacritty, VS Code, Cursor, Xcode, Zed, Sublime Text, PyCharm, Claude |
| ![](previews/design.gif) | **Design app in front**: painter's beret | Figma, Sketch, Photoshop, Illustrator, Pixelmator Pro, Affinity |
| ![](previews/microphone.gif) | **Microphone in use**: headset | Default input device running in any app (CoreAudio), so browser calls count too |
| ![](previews/low-battery.gif) | **Battery ≤ 20 %**: faded rainbow, tired eyes | IOKit power sources |
| ![](previews/charging.gif) | **Charging**: lightning bolt on the pop-tart | IOKit power sources |
| ![](previews/late-night.gif) | **Midnight to 6 AM**: nightcap, closed eyes, zzz | Clock |
| ![](previews/high-cpu.gif) | **CPU above 70 % for 3 s**: sweat drops, double-speed animation | `host_statistics` |

Accessories stack: music with a terminal in front gives you hacker shades **and** notes.

![](previews/terminal-music.gif)

When two accessories want the same spot, a fixed priority decides. On the head, the order is headset > beret > nightcap. On the eyes, it is shades > closed > tired.

## Install

You need BetterTouchTool with Swift plugin support and the Command Line Developer Tools (`xcode-select --install`). Tested on BTT 6.784 and 6.958, macOS 15.7, MacBook Pro M1 (2020).

1. Download `NyanCat.swift` from the [latest release](../../releases/latest), or grab it from this repo.
2. Copy it to `~/Library/Application Support/BetterTouchTool/Plugins/`. BTT compiles it on its own and asks you to confirm.
3. In BTT → Touch Bar, add a **Plugin** widget and pick **Nyan Cat**. Put it at the top of the list and set its placement to the left.
4. If your preset uses conditional activation groups (for example a "Music Playing" group), add the widget to those groups too.
5. When you update the plugin, restart BTT. Hot reload does not replace widgets that already exist.

## Try the variants

Force one or more states with a BTT variable (comma-separated):

```bash
osascript -e 'tell application "BetterTouchTool" to set_string_variable "nyan_forzar" to "musica,terminal"'
```

Set it back to empty to return to automatic detection:

```bash
osascript -e 'tell application "BetterTouchTool" to set_string_variable "nyan_forzar" to ""'
```

State names (in Spanish, as in the code): `musica`, `terminal`, `diseno`, `microfono`, `bateria_baja`, `cargando`, `noche`, `cpu`. Any other value (`normal`, for example) shows the plain cat.

## Hacking on it

The sprites are drawn in code by `generar.py` (Python 3 + Pillow). Each sprite sits on a 46×20 px grid, scaled ×3, with 12 frames per layer. The script embeds the PNG strips into `NyanCat.swift`, using `NyanCat.swift.in` as the template. Edit the template or the generator, never `NyanCat.swift` itself:

```bash
python3 generar.py
```

The app lists and the stacking rules live in `NyanCat.swift.in` (`apps` and `capasPara`). The comments in the code are in Spanish.

## Performance

A 90 ms timer swaps pre-decoded frames on Core Animation layers, and the state is re-checked once per second. With the cat running, BetterTouchTool sat at about 1–2 % CPU on an M1 MacBook Pro.

## Credits

Nyan Cat is a character created by Chris Torres (2011). This is a non-commercial fan tribute with original pixel art. The code is released under the MIT license.
