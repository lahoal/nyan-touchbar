# Changelog

## v1.1.0 — 2026-10-29

### New moods

| | Mood | Trigger |
|---|---|---|
| ![](previews/writing.gif) | Pencil behind the ear | A writing or office app in front (Notes, Pages, Word, Obsidian, Notion, Bear…) or a Google Docs tab |
| ![](previews/chat.gif) | Speech bubble, typing | A chat app in front (Slack, Discord, WhatsApp, Telegram, Signal, Messages, Teams…) |
| ![](previews/games.gif) | Gamepad | A game, launcher or emulator in front (Steam, Epic, Battle.net, Minecraft launchers, OpenEmu…) |
| ![](previews/video.gif) | Popcorn | A video player in front (TV, IINA, VLC, Infuse…) or a YouTube, Netflix or Twitch tab |
| ![](previews/video-call.gif) | Tie | Any camera in use, virtual ones included (CoreMediaIO) |
| ![](previews/idle.gif) | Falls asleep, slow motion | No keyboard or mouse input for 5 minutes |
| ![](previews/offline.gif) | Blinking question mark | No network connection |
| ![](previews/hot.gif) | Melting frosting | The Mac's thermal state is serious or critical |
| ![](previews/morning.gif) | Steaming coffee | 7 to 10 AM |
| ![](previews/halloween.gif) | Witch hat | October 31 |
| ![](previews/christmas.gif) | Santa hat | December 24–25 |
| ![](previews/new-year.gif) | Party hat and confetti | December 31 – January 1 |
| ![](previews/fiestas-patrias.gif) | Chilean *chupalla* | September 18–19 |

### Triple tap to hide a mood

- Tap the cat three times in a row (within 0.8 s) to hide the decorative moods on screen: coffee, popcorn, chat bubble and special days. The cat answers with a burst of sparkles.
- A hidden mood stays hidden until its next occurrence: coffee until tomorrow morning, a special day until next year, popcorn and the bubble until the next time you open a video or chat app.
- Another triple tap with nothing left to hide brings everything back.
- Moods that carry information (battery, charging, CPU, heat, network, microphone, camera) can't be hidden.
- Dismissals are saved to `~/Library/Application Support/NyanCat/descartados.json`. Every cat widget shares them (BTT creates one instance per Touch Bar group, e.g. Global and "Music Playing"), and they survive a BTT restart.

![](previews/dismiss.gif)

### Haptic feedback

- Each tap on the cat gives a light click on the trackpad, and the triple tap a strong one.
- The Touch Bar has no haptic engine, and the public macOS haptics API only fires while a finger rests on the trackpad. The plugin uses the trackpad actuator through the private MultitouchSupport framework instead, the same approach as [HapticKey](https://github.com/niw/HapticKey). If a macOS update changes that API, the cat keeps working without haptics.

### App lists moved to `apps.json`

- 194 apps across six moods (terminal 58, design 32, writing 37, chat 28, games 25, video 14), picked from the most installed Homebrew casks of the last 365 days, plus popular App Store apps.
- Entries are exact bundle IDs, or a prefix ending in `*` (`com.jetbrains.*`, `com.adobe.PremierePro*`).
- Browser tabs count too: when a browser is in front, the title of its active window is matched against keywords (Penpot, Figma, Canva, Google Docs, YouTube, Netflix, Twitch…). This uses BTT's existing Accessibility permission.
- To customize, copy `apps.json` to `~/Library/Application Support/NyanCat/apps.json`. The plugin reloads it on save, with no BTT restart. Without that file, the copy embedded in the plugin is used.
- `generar.py` validates the file (known moods, no duplicates, well-formed IDs) before embedding it.

### Changes

- Accessory stacking is now a table of zones (`zonas` in `NyanCat.swift.in`) instead of nested `if`s. Head: headset > special day > beret > pencil > nightcap. Eyes: shades > closed (night or idle) > tired. In front of the face: gamepad > popcorn > coffee. Top left: zzz > bubble.
- The state check runs on its own one-second timer, separate from the animation timer, so the animation can slow down (idle) or speed up (high CPU) without affecting detection.
- With everything running, BetterTouchTool still sits at about 2 % CPU on an M1 MacBook Pro.

### Upgrading from v1.0.0

1. Replace `~/Library/Application Support/BetterTouchTool/Plugins/NyanCat.swift` with the one from this release and confirm the compile prompt.
2. Restart BTT (hot reload doesn't replace widgets that already exist).
3. Optional: copy `apps.json` to `~/Library/Application Support/NyanCat/` if you want to edit the app lists.

## v1.0.0 — 2026-10-27

First release: animated Nyan Cat Touch Bar widget for BetterTouchTool, with 8 stackable variants (music, terminal/editor, design app, microphone, low battery, charging, late night, high CPU).
