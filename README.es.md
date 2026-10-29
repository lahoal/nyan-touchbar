# Nyan Cat para la Touch Bar

*[Read in English](README.md)*

Un Nyan Cat animado para la Touch Bar de la MacBook Pro, hecho como plugin de [BetterTouchTool](https://folivora.ai). Cambia de accesorios según lo que estés haciendo.

![El Nyan Cat pasando por sus variantes en una Touch Bar real](previews/touchbar-real.gif)

*Grabado en una Touch Bar real. Así se ve la barra completa (el nombre del evento del calendario se reemplazó por privacidad):*

![Touch Bar completa con el gato a la izquierda](previews/touchbar-real.png)

Novedades de cada versión: [CHANGELOG.md](CHANGELOG.md) (en inglés).

## Variantes

| | Estado | Cómo se detecta |
|---|---|---|
| ![](previews/music.gif) | **Música sonando**: notas que suben | Variable de BTT `BTTCurrentlyPlaying` |
| ![](previews/terminal.gif) | **Terminal, editor o herramienta de desarrollo al frente**: arcoíris matrix y lentes de hacker | `apps.json` → `terminal` (58 apps: terminales, editores, IDE, clientes Git y de API, bases de datos) |
| ![](previews/design.gif) | **App de diseño al frente**: boina de pintor | `apps.json` → `diseno` (Figma, Sketch, Adobe, Affinity, Blender, Final Cut, DaVinci…), o una pestaña de Penpot, Figma o Canva |
| ![](previews/writing.gif) | **App de escritura u oficina al frente**: lápiz en la oreja | `apps.json` → `escritura` (Notas, Pages, Word, Obsidian, Notion, Bear…), o una pestaña de Google Docs |
| ![](previews/chat.gif) | **App de chat al frente**: globo de diálogo escribiendo | `apps.json` → `chat` (Slack, Discord, WhatsApp, Telegram, Signal, Mensajes, Teams…) |
| ![](previews/games.gif) | **Juego o launcher al frente**: control | `apps.json` → `juegos` (Steam, Epic, Battle.net, launchers de Minecraft, emuladores…) |
| ![](previews/video.gif) | **Viendo video**: palomitas | `apps.json` → `video` (TV, IINA, VLC, Infuse…), o una pestaña de YouTube, Netflix o Twitch |
| ![](previews/video-call.gif) | **Cámara en uso**: corbata | Cualquier cámara, incluidas las virtuales, en uso por cualquier app (CoreMediaIO) |
| ![](previews/microphone.gif) | **Micrófono en uso**: audífonos | La entrada de audio predeterminada está en uso por cualquier app (CoreAudio), así que también cuentan las llamadas desde el navegador |
| ![](previews/low-battery.gif) | **Batería ≤ 20 %**: arcoíris desteñido, ojos cansados | IOKit |
| ![](previews/charging.gif) | **Cargando**: rayo en la tostada | IOKit |
| ![](previews/late-night.gif) | **De 0:00 a 6:00**: gorro de dormir, ojos cerrados, zzz | Reloj |
| ![](previews/high-cpu.gif) | **CPU sobre 70 % por 3 s**: gotas de sudor y animación al doble de velocidad | `host_statistics` |
| ![](previews/hot.gif) | **Mac caliente**: el glaseado se derrite | `ProcessInfo.thermalState` grave o crítico |
| ![](previews/idle.gif) | **5 min sin teclado ni mouse**: se duerme y anda en cámara lenta | `CGEventSource` |
| ![](previews/offline.gif) | **Sin red**: signo de pregunta que parpadea | `NWPathMonitor` |
| ![](previews/morning.gif) | **De 7:00 a 10:00**: café humeante | Reloj |
| ![](previews/halloween.gif) | **Fechas especiales**: sombrero de bruja (31 oct), gorro navideño (24 y 25 dic), gorro de fiesta y confeti (31 dic y 1 ene), chupalla (18 y 19 sep) | Calendario |

Los accesorios se combinan: con música y la terminal al frente, el gato sale con lentes de hacker **y** notas.

![](previews/terminal-music.gif)

Cuando dos accesorios ocupan el mismo lugar, una prioridad fija decide (tabla `zonas` en `NyanCat.swift.in`):

- Cabeza: audífonos > fecha especial > boina > lápiz > gorro de dormir
- Ojos: lentes > dormido (noche o inactivo) > cansado
- Frente a la cara: control > palomitas > café
- Arriba a la izquierda: zzz > globo

## Ocultar un mood con triple toque

Toca al gato 3 veces seguidas para ocultar los moods decorativos que estén a la vista: café, palomitas, globo de chat y fechas especiales. No vuelven hasta su próxima ocurrencia: el café, mañana a las 7; una fecha especial, el próximo año; las palomitas y el globo, la próxima vez que abras una app de video o de chat. El descarte se guarda en `~/Library/Application Support/NyanCat/descartados.json`, así que lo comparten todos los widgets del gato (uno por grupo de BTT) y sobrevive a un reinicio de BTT. Otro triple toque, sin nada que ocultar, los devuelve. Los moods que informan algo (batería, CPU, red, micrófono, cámara) no se ocultan.

![](previews/dismiss.gif)

Cada toque hace vibrar suave el trackpad y el triple toque, fuerte, con unas chispas. La Touch Bar no tiene motor de vibración, así que se usa el del trackpad mediante una API privada de macOS (la misma que usa [HapticKey](https://github.com/niw/HapticKey)); si una versión de macOS la cambia, el gato sigue funcionando sin vibrar.

## Qué apps activan cada mood

Las listas están en `apps.json`, ordenadas por mood y armadas a partir de las apps más instaladas con Homebrew en el último año. Para cambiarlas, copia el archivo a `~/Library/Application Support/NyanCat/apps.json` y edítalo: el plugin lo relee al guardarlo, sin reiniciar BTT. Si ese archivo no existe, se usa la copia embebida en el plugin.

- `apps`: bundle ID exacto, o un prefijo terminado en `*` (`com.jetbrains.*`). Para saber el de una app: `osascript -e 'id of app "Nombre"'`.
- `navegadores` y `titulos`: con un navegador al frente, se busca cada palabra en el título de la ventana activa (sin distinguir mayúsculas). Así cuenta una pestaña de Penpot o de YouTube. Usa el permiso de Accesibilidad de BTT.

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

Estados: `musica`, `terminal`, `diseno`, `escritura`, `chat`, `juegos`, `video`, `microfono`, `videollamada`, `bateria_baja`, `cargando`, `noche`, `manana`, `inactivo`, `cpu`, `caliente`, `sin_red`, `halloween`, `navidad`, `ano_nuevo`, `fiestas_patrias`. Cualquier otro valor (por ejemplo `normal`) muestra el gato sin accesorios.

## Modificar

Los sprites se dibujan con código en `generar.py` (Python 3 + Pillow). Cada sprite usa una grilla de 46×20 px, escala ×3 y 12 cuadros por capa. El script embebe las tiras PNG en `NyanCat.swift` a partir de la plantilla `NyanCat.swift.in`. Edita la plantilla o el generador, nunca `NyanCat.swift` directamente:

```bash
python3 generar.py
```

Las reglas de combinación están en `NyanCat.swift.in` (`zonas`); las listas de apps, en `apps.json`, que `generar.py` valida y embebe.

## Consumo

Un timer de 90 ms cambia cuadros ya decodificados en capas de Core Animation, y el estado se revisa una vez por segundo. Con el gato andando, BetterTouchTool quedó en torno a 1–2 % de CPU en una MacBook Pro M1.

## Créditos

Nyan Cat es un personaje creado por Chris Torres (2011). Esto es un homenaje de fans, sin fines comerciales y con pixel art propio. El código se publica bajo licencia MIT.
