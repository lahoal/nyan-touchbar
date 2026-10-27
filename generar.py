"""Genera los sprites del Nyan Cat (pixel art propio) y arma NyanCat.swift con ellos embebidos.

Grilla de 46x20 px, escala 3 -> 138x60 px (69x30 pt en la Touch Bar).
Cada capa es una tira de 12 cuadros. Las bases son opacas; los accesorios, transparentes.
Uso: python3 generar.py   (escribe NyanCat.swift, sprites/ y vistas/)
"""
import base64, io, os
from PIL import Image, ImageDraw

W, H, S, N = 46, 20, 3, 12
NAVY, BLK, WHT, YEL = (0, 51, 102), (0, 0, 0), (255, 255, 255), (255, 230, 0)
RAIN = [(255, 0, 0), (255, 153, 0), (255, 255, 0), (51, 255, 0), (0, 153, 255), (102, 51, 255)]
MATRIX = [(0, 255, 65), (0, 170, 45), (0, 255, 65), (0, 170, 45), (0, 255, 65), (0, 170, 45)]
FADED = [tuple((c + 140) // 2 for c in col) for col in RAIN]
CRUST, PINK, SPR, GREY, CHEEK = (255, 204, 153), (255, 153, 255), (255, 51, 153), (153, 153, 153), (255, 153, 153)
BOB = [0, 0, 1, 1, 1, 0]
STARS = [(5, 1), (30, 0), (18, 18), (44, 17), (10, 17), (24, 1), (40, 3)]
HERE = os.path.dirname(os.path.abspath(__file__))


def pose(i):
    """Desplazamientos del cuadro i: cuerpo (b), cabeza (hb) y x de la cabeza (hx)."""
    k = i % 6
    return BOB[k], BOB[(k + 1) % 6], 23 + (1 if k in (2, 3) else 0)


def lienzo(fondo=None):
    im = Image.new("RGBA", (W, H), fondo + (255,) if fondo else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    return im, (lambda x0, y0, x1, y1, c: d.rectangle([x0, y0, x1, y1], fill=c))


def base(i, rainbow=RAIN, fondo=NAVY, estrella=WHT, tramos=5):
    im, r = lienzo(fondo)
    k = i % 6
    b, hb, hx = pose(i)
    for sx, sy in STARS:
        x = (sx - k * 3) % W
        if k % 2:
            r(x - 1, sy, x + 1, sy, estrella); r(x, sy - 1, x, sy + 1, estrella)
        else:
            r(x, sy, x, sy, estrella)
    for seg in range(tramos):  # arcoíris ondulado
        off = (seg + k) % 2
        x0 = 14 - (seg + 1) * 3
        for n, c in enumerate(rainbow):
            r(x0, 4 + n * 2 + off + b, x0 + 2, 5 + n * 2 + off + b, c)
    for n, c in enumerate(rainbow):
        r(14, 4 + n * 2 + b, 15, 5 + n * 2 + b, c)
    tail = 10 + (k % 2)
    r(10, tail + b, 13, tail + 1 + b, BLK); r(11, tail + b, 13, tail + b, GREY)
    lx = k % 2
    for px in (15, 18, 25, 28):
        r(px - lx, 15 + b, px + 1 - lx, 17 + b, BLK); r(px - lx, 15 + b, px - lx, 16 + b, GREY)
    r(13, 2 + b, 30, 16 + b, BLK); r(14, 3 + b, 29, 15 + b, CRUST); r(16, 4 + b, 27, 14 + b, PINK)
    for sx, sy in [(18, 5), (22, 6), (25, 5), (17, 9), (20, 11), (24, 9), (26, 12), (19, 13), (23, 13)]:
        r(sx, sy + b, sx, sy + b, SPR)
    r(hx, 7 + hb, hx + 12, 16 + hb, BLK); r(hx + 1, 8 + hb, hx + 11, 15 + hb, GREY)
    for ex in (hx + 1, hx + 9):
        r(ex, 5 + hb, ex + 2, 7 + hb, BLK); r(ex + 1, 6 + hb, ex + 1, 8 + hb, GREY)
    for ex in (hx + 3, hx + 8):
        r(ex, 10 + hb, ex + 1, 11 + hb, BLK); r(ex, 10 + hb, ex, 10 + hb, WHT)
    r(hx + 2, 12 + hb, hx + 2, 12 + hb, CHEEK); r(hx + 10, 12 + hb, hx + 10, 12 + hb, CHEEK)
    r(hx + 4, 13 + hb, hx + 8, 13 + hb, BLK); r(hx + 6, 12 + hb, hx + 6, 12 + hb, BLK)
    return im


NOTA = ["..X.", "..XX", "..X.X", "..X.", "XXX.", "XXX."]  # corchea: cabeza abajo, plica y bandera


def notas(i):
    im, r = lienzo()
    for x, fase, col in ((38, 0, WHT), (42, 6, YEL)):
        y = 13 - ((i + fase) % N)  # suben 1 px por cuadro y vuelven a empezar
        for dy, fila in enumerate(NOTA):
            for dx, ch in enumerate(fila):
                if ch == "X" and 0 <= y + dy < H:
                    r(x + dx - 1, y + dy, x + dx - 1, y + dy, col)
    return im


def lentes_hacker(i):
    im, r = lienzo()
    _, hb, hx = pose(i)
    y = 9 + hb
    r(hx + 1, y + 1, hx + 11, y + 1, BLK)  # patillas y puente
    r(hx + 2, y, hx + 5, y + 2, (15, 15, 15)); r(hx + 7, y, hx + 10, y + 2, (15, 15, 15))
    g = (i // 2) % 4  # brillo verde que recorre los lentes
    r(hx + 2 + g, y, hx + 2 + g, y, (0, 255, 65)); r(hx + 7 + g, y, hx + 7 + g, y, (0, 255, 65))
    return im


def audifonos(i):
    im, r = lienzo()
    _, hb, hx = pose(i)
    BAND, CUP, RED = (60, 60, 60), (30, 30, 30), (255, 60, 60)
    r(hx + 1, 4 + hb, hx + 11, 4 + hb, BAND)
    r(hx, 5 + hb, hx, 8 + hb, BAND); r(hx + 12, 5 + hb, hx + 12, 8 + hb, BAND)
    r(hx - 1, 9 + hb, hx + 1, 12 + hb, CUP); r(hx + 11, 9 + hb, hx + 13, 12 + hb, CUP)
    for n in range(3):  # brazo del micrófono hacia la boca
        r(hx + 11 - n, 13 + hb + (n > 0), hx + 11 - n, 13 + hb + (n > 0), BAND)
    r(hx + 8, 14 + hb, hx + 8, 14 + hb, RED if (i // 3) % 2 else (150, 30, 30))
    return im


def boina(i):
    im, r = lienzo()
    _, hb, hx = pose(i)
    ROJA, OSCURA = (200, 30, 60), (120, 10, 35)
    r(hx + 3, 4 + hb, hx + 12, 6 + hb, ROJA); r(hx + 2, 6 + hb, hx + 11, 7 + hb, OSCURA)
    r(hx + 5, 3 + hb, hx + 10, 3 + hb, ROJA); r(hx + 8, 2 + hb, hx + 8, 2 + hb, OSCURA)
    return im


def gorro_noche(i):
    im, r = lienzo()
    _, hb, hx = pose(i)
    AZUL = (40, 80, 200)
    filas = [(1, 11), (2, 10), (4, 10), (6, 11), (8, 12), (10, 13)]  # cono que se dobla hacia atrás
    for n, (a, z) in enumerate(filas):
        r(hx + a, 6 - n + hb, hx + z, 6 - n + hb, WHT if n % 2 == 0 else AZUL)
    r(hx + 14, 0, hx + 15, 1, WHT)  # pompón
    return im


def ojos(i, modo):
    """modo 'dormido' (ojos cerrados) o 'cansado' (párpados a media asta)."""
    im, r = lienzo()
    _, hb, hx = pose(i)
    for ex in (hx + 3, hx + 8):
        r(ex, 10 + hb, ex + 1, 11 + hb, GREY)
        if modo == "dormido":
            r(ex, 11 + hb, ex + 1, 11 + hb, BLK)
        else:
            r(ex, 11 + hb, ex + 1, 11 + hb, BLK); r(ex - 1, 9 + hb, ex + 2, 9 + hb, (110, 110, 110))
    return im


def zzz(i):
    im, r = lienzo()
    for n, (x, y) in enumerate(((1, 0), (6, 0), (11, 0))):
        if n <= i // 4:  # aparecen de a una
            r(x, y, x + 3, y, WHT); r(x + 2, y + 1, x + 2, y + 1, WHT)
            r(x + 1, y + 2, x + 1, y + 2, WHT); r(x, y + 3, x + 3, y + 3, WHT)
    return im


def rayo(i):
    im, r = lienzo()
    b = pose(i)[0]
    if (i // 3) % 2 == 0:
        return im  # parpadea
    for dy, fila in enumerate(["..XX", ".XX.", "XXXX", ".XX.", "XX..", "X..."]):
        for dx, ch in enumerate(fila):
            if ch == "X":
                r(20 + dx, 6 + dy + b, 20 + dx, 6 + dy + b, YEL)
    return im


def sudor(i):
    im, r = lienzo()
    _, hb, hx = pose(i)
    GOTA = (150, 220, 255)
    for x, fase in ((hx - 2, 0), (hx + 13, 3)):
        y = 5 + ((i + fase) % 6) + hb  # gota con forma de lágrima que cae
        r(x + 1, y, x + 1, y, GOTA); r(x, y + 1, x + 1, y + 2, GOTA)
    return im


CAPAS = {
    "base": lambda i: base(i),
    "base_matrix": lambda i: base(i, MATRIX, (0, 12, 0), (0, 200, 50)),
    "base_destenida": lambda i: base(i, FADED, (20, 35, 60), (150, 150, 150), tramos=3),
    "notas": notas, "lentes_hacker": lentes_hacker, "audifonos": audifonos, "boina": boina,
    "gorro_noche": gorro_noche, "dormido": lambda i: ojos(i, "dormido"),
    "cansado": lambda i: ojos(i, "cansado"), "zzz": zzz, "rayo": rayo, "sudor": sudor,
}


def tira(fn):
    out = Image.new("RGBA", (W * S * N, H * S), (0, 0, 0, 0))
    for i in range(N):
        out.paste(fn(i).resize((W * S, H * S), Image.NEAREST), (i * W * S, 0))
    return out


def png(im):
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True); return buf.getvalue()


def compuesto(nombres, i):
    im = CAPAS[nombres[0]](i).copy()
    for n in nombres[1:]:
        im.alpha_composite(CAPAS[n](i))
    return im.resize((W * S, H * S), Image.NEAREST)


VISTAS = {  # lo que el plugin muestra en cada estado (ver NyanCat.swift)
    "normal": ["base"], "musica": ["base", "notas"], "terminal": ["base_matrix", "lentes_hacker"],
    "diseno": ["base", "boina"], "microfono": ["base", "audifonos"],
    "bateria-baja": ["base_destenida", "cansado"], "cargando": ["base", "rayo"],
    "noche": ["base", "gorro_noche", "dormido", "zzz"], "cpu-alta": ["base", "sudor"],
    "combo-musica-terminal": ["base_matrix", "lentes_hacker", "notas"],
}

if __name__ == "__main__":
    tiras = {n: tira(fn) for n, fn in CAPAS.items()}
    for n, t in tiras.items():
        assert t.size == (W * S * N, H * S), n
    # vistas para el README: GIF por estado y una lámina con todos
    lam = Image.new("RGBA", (W * S * 2 + 30, (H * S + 30) * ((len(VISTAS) + 1) // 2)), (24, 24, 24, 255))
    d = ImageDraw.Draw(lam)
    for k, (nombre, capas) in enumerate(VISTAS.items()):
        fr = [compuesto(capas, i).convert("RGB") for i in range(N)]
        fr[0].save(os.path.join(HERE, "vistas", nombre + ".gif"), save_all=True, append_images=fr[1:], duration=90, loop=0)
        x, y = (k % 2) * (W * S + 30), (k // 2) * (H * S + 30)
        lam.paste(fr[3], (x, y)); d.text((x, y + H * S + 4), nombre, fill=(230, 230, 230))
    lam.save(os.path.join(HERE, "vistas", "todas.png"))
    # NyanCat.swift = plantilla + sprites embebidos
    datos = ",\n".join(f'    "{n}": "{base64.b64encode(png(t)).decode()}"' for n, t in tiras.items())
    plantilla = open(os.path.join(HERE, "NyanCat.swift.in")).read()
    assert "/*SPRITES*/" in plantilla
    open(os.path.join(HERE, "NyanCat.swift"), "w").write(plantilla.replace("/*SPRITES*/", datos))
    print("ok:", len(tiras), "capas,", len(VISTAS), "vistas")
