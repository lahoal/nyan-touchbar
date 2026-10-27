# Nyan Cat para la Touch Bar

*[Read in English](README.md)*

Un Nyan Cat animado para la Touch Bar de la MacBook Pro, hecho como plugin de [BetterTouchTool](https://folivora.ai). Cambia de accesorios según lo que estés haciendo.

![El Nyan Cat pasando por sus variantes en una Touch Bar real](previews/touchbar-real.gif)

*Grabado en una Touch Bar real. Así se ve la barra completa (el nombre del evento del calendario se reemplazó por privacidad):*

![Touch Bar completa con el gato a la izquierda](previews/touchbar-real.png)

## Variantes

| | Estado | Cómo se detecta |
|---|---|---|
| ![](previews/music.gif) | **Música sonando**: notas que suben | Variable de BTT `BTTCurrentlyPlaying` |
| ![](previews/terminal.gif) | **Terminal o editor al frente**: arcoíris matrix y lentes de hacker | App al frente: Terminal, iTerm2, Warp, Ghostty, kitty, Alacritty, VS Code, Cursor, Xcode, Zed, Sublime Text, PyCharm, Claude |
| ![](previews/design.gif) | **App de diseño al frente**: boina de pintor | Figma, Sketch, Photoshop, Illustrator, Pixelmator Pro, Affinity |
| ![](previews/microphone.gif) | **Micrófono en uso**: audífonos | La entrada de audio predeterminada está en uso por cualquier app (CoreAudio), así que también cuentan las llamadas desde el navegador |
| ![](previews/low-battery.gif) | **Batería ≤ 20 %**: arcoíris desteñido, ojos cansados | IOKit |
| ![](previews/charging.gif) | **Cargando**: rayo en la tostada | IOKit |
| ![](previews/late-night.gif) | **De 0:00 a 6:00**: gorro de dormir, ojos cerrados, zzz | Reloj |
| ![](previews/high-cpu.gif) | **CPU sobre 70 % por 3 s**: gotas de sudor y animación al doble de velocidad | `host_statistics` |

Los accesorios se combinan: con música y la terminal al frente, el gato sale con lentes de hacker **y** notas.

![](previews/terminal-music.gif)

Cuando dos accesorios ocupan el mismo lugar, una prioridad fija decide. En la cabeza el orden es audífonos > boina > gorro; en los ojos, lentes > dormido > cansado.

## Instalación

Necesitas BetterTouchTool con soporte para plugins en Swift y las Command Line Developer Tools (`xcode-select --install`). Probado en BTT 6.784 y 6.958, macOS 15.7, MacBook Pro M1 (2020).

1. Descarga `NyanCat.swift` desde el [último release](../../releases/latest), o tómalo de este repo.
2. Cópialo en `~/Library/Application Support/BetterTouchTool/Plugins/`. BTT lo compila solo y te pide confirmación.
3. En BTT → Touch Bar, agrega un widget **Plugin** y elige **Nyan Cat**. Déjalo arriba de todo, con ubicación a la izquierda.
4. Si tu preset usa grupos de activación condicional (por ejemplo uno de "Music Playing"), agrega el widget también en esos grupos.
5. Cuando actualices el plugin, reinicia BTT: la recarga en caliente no reemplaza los widgets que ya existen.

## Probar las variantes

Para forzar uno o más estados, usa una variable de BTT (separados por coma):

```bash
osascript -e 'tell application "BetterTouchTool" to set_string_variable "nyan_forzar" to "musica,terminal"'
```

Para volver a la detección automática, déjala vacía:

```bash
osascript -e 'tell application "BetterTouchTool" to set_string_variable "nyan_forzar" to ""'
```

Estados: `musica`, `terminal`, `diseno`, `microfono`, `bateria_baja`, `cargando`, `noche`, `cpu`. Cualquier otro valor (por ejemplo `normal`) muestra el gato sin accesorios.

## Modificar

Los sprites se dibujan con código en `generar.py` (Python 3 + Pillow). Cada sprite usa una grilla de 46×20 px, escala ×3 y 12 cuadros por capa. El script embebe las tiras PNG en `NyanCat.swift` a partir de la plantilla `NyanCat.swift.in`. Edita la plantilla o el generador, nunca `NyanCat.swift` directamente:

```bash
python3 generar.py
```

Las listas de apps y las reglas de combinación están en `NyanCat.swift.in` (`apps` y `capasPara`).

## Consumo

Un timer de 90 ms cambia cuadros ya decodificados en capas de Core Animation, y el estado se revisa una vez por segundo. Con el gato andando, BetterTouchTool quedó en torno a 1–2 % de CPU en una MacBook Pro M1.

## Créditos

Nyan Cat es un personaje creado por Chris Torres (2011). Esto es un homenaje de fans, sin fines comerciales y con pixel art propio. El código se publica bajo licencia MIT.
