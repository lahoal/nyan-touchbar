// Pruebas de comportamiento del plugin, sin BTT: un delegado falso, teclas de media falsas y un archivo de descartes
// temporal (nunca el real). Correr con: zsh pruebas/correr.sh
import Cocoa

final class Del: NSObject, BTTTouchBarPluginDelegate {
    var vars: [String: Any] = ["nyan_forzar": "normal"]
    func executeAssignedBTTActions(_ sender: Any) {}
    func update(with string: String, sender: Any) {}
    func setVariable(_ name: String, value: Any) { vars[name] = value }
    func getVariable(_ name: String) -> Any? { vars[name] }
}

var fallas = 0, total = 0
func check(_ ok: Bool, _ msg: String) { total += 1; if !ok { fallas += 1; print("FALLA", msg) } }
func esperar(_ s: Double) { RunLoop.main.run(until: Date().addingTimeInterval(s)) }
func fecha(_ s: String) -> Date { let f = DateFormatter(); f.dateFormat = "yyyy-MM-dd HH:mm"; return f.date(from: s)! }

let tmp = FileManager.default.temporaryDirectory.appendingPathComponent("nyan-pruebas-\(getpid())")
try? FileManager.default.createDirectory(at: tmp, withIntermediateDirectories: true)
defer { try? FileManager.default.removeItem(at: tmp) }

func nuevo() -> (NyanCat, Del) {
    let n = NyanCat(), d = Del()
    n.delegate = d
    n.rutaDescartes = tmp.appendingPathComponent("descartados.json")
    _ = n.touchBarViewController()
    return (n, d)
}
let (n, d) = nuevo()
var teclas: [Int] = []
n.tecla = { teclas.append($0) }
func forzar(_ s: String) -> [String] { d.vars["nyan_forzar"] = s; n.vuelta = 0; n.actualizarEstado(); return n.capasGato }

// --- Moods y prioridades
check(forzar("terminal,musica,juegos,video,noche,chat") == ["base_matrix", "gorro_noche", "lentes_hacker", "control", "zzz", "notas"], "combinación múltiple")
check(forzar("halloween,diseno,microfono") == ["base", "audifonos"], "audífonos gana en la cabeza")
check(forzar("halloween,diseno") == ["base", "sombrero_bruja"], "fecha especial gana a la boina")
check(forzar("inactivo,chat,videollamada,video,manana") == ["base", "dormido", "corbata", "palomitas", "zzz"], "inactivo")
check(n.estadosDeCalendario(fecha("2026-12-25 08:00")) == ["navidad", "manana"], "navidad en la mañana")
check(n.estadosDeCalendario(fecha("2026-09-18 03:00")) == ["fiestas_patrias", "noche"], "18 de septiembre de madrugada")
check(n.ocurrencia("ano_nuevo", fecha("2027-01-01 10:00")) == n.ocurrencia("ano_nuevo", fecha("2026-12-31 10:00")), "año nuevo es una sola ocurrencia")

// --- Panel y esquemas
_ = forzar("normal"); check(n.activas.suffix(2) == ["cielo_base", "panel_apagado_base"], "sin reproductor: panel apagado")
_ = forzar("reproductor"); check(n.activas.last == "panel_play_base", "en pausa: ▶")
_ = forzar("terminal,musica"); check(n.activas.suffix(2) == ["cielo_matrix", "panel_pausa_matrix"], "terminal con música: verde y ⏸")
_ = forzar("bateria_baja,reproductor"); check(n.activas.last == "panel_play_destenida", "batería baja: desteñido")

// --- Animación con Core Animation
let base = n.capas["base"]!, contenido = base.contents as AnyObject
check(n.animadas.count >= 20 && n.animadas.contains(base) && n.animadas.contains(n.capas["cielo_base"]!), "capas con movimiento animadas")
check(!n.animadas.contains(n.capas["panel_play_base"]!) && !n.animadas.contains(n.capas["panel_apagado_matrix"]!), "capas quietas sin animación")
if let a = base.animation(forKey: "cuadros") as? CAKeyframeAnimation {
    check(a.calculationMode == .discrete && a.beginTime == 1 && a.repeatCount == .infinity && abs(a.duration - 12 * 0.09) < 1e-9, "animación por pasos de 90 ms")
} else { check(false, "base sin animación") }
_ = forzar("cpu"); check(abs((base.animation(forKey: "cuadros")?.duration ?? 0) - 12 * 0.045) < 1e-9, "CPU alta: el doble de rápido")
_ = forzar("inactivo"); check(abs((base.animation(forKey: "cuadros")?.duration ?? 0) - 12 * 0.3) < 1e-9, "inactivo: cámara lenta")
_ = forzar("normal")
for _ in 0..<5 { n.actualizarEstado() }
check(base.contents as AnyObject === contenido, "la imagen de la capa no se reemplaza")
check(n.capas.allSatisfy { nombre, capa in capa.isHidden != (n.activas.contains(nombre) || n.transitorios[nombre] != nil) }, "solo se ven las capas activas y las transitorias")

// --- Gestos del botón (sin teclas reales)
_ = forzar("musica"); esperar(1.2)  // deja terminar la ráfaga del cambio de mood
n.tocado(100, 3); check(teclas == [16] && n.transitorios["toque_a_play_base"] == 8, "toque: play/pausa")
check(n.capas["toque_a_play_base"]!.isHidden == false && n.capas["toque_a_play_base"]!.animation(forKey: "unaVez") != nil, "animación del toque visible")
n.tocado(80, 25); check(teclas.last == 17 && n.gatoCapa.speed == 2 && n.paso == 2, "deslizar a la derecha: siguiente y el gato corre")
esperar(0.9)
check(n.transitorios.isEmpty && n.gatoCapa.speed == 1 && n.capas["desliza_siguiente_base"]!.isHidden, "al terminar se esconde y vuelve la velocidad")
n.tocado(120, -25); check(teclas.last == 18 && n.gatoCapa.speed == -1, "deslizar a la izquierda: anterior y rebobina")
esperar(0.9)
let antes = teclas.count
n.toques = []; n.tocado(30, 2); check(teclas.count == antes && n.toques.count == 1, "tocar el gato no manda tecla")
n.tocado(30, 40); check(teclas.count == antes, "deslizar sobre el gato no hace nada")
_ = forzar("normal"); n.tocado(100, 0); check(teclas.count == antes && n.toques.count == 2, "sin reproductor el botón cuenta como gato")

// --- Triple toque y descartes compartidos entre instancias
n.toques = []; n.transitorios = [:]
_ = forzar("manana,musica,halloween")
n.tocarGato(); n.tocarGato(); check(n.activas.contains("cafe"), "dos toques no descartan")
n.tocarGato(); check(!n.activas.contains("cafe") && !n.activas.contains("sombrero_bruja") && n.transitorios["destello"] == 12, "el tercero oculta con chispas")
let (n2, d2) = nuevo(); d2.vars["nyan_forzar"] = "manana"; n2.vuelta = 0; n2.actualizarEstado()
check(!n2.activas.contains("cafe"), "otra instancia también lo oculta")
_ = forzar("musica"); _ = forzar("manana"); check(!n.activas.contains("cafe"), "forzar estados no lo trae de vuelta")
n.tocarGato(); n.tocarGato(); n.tocarGato(); check(forzar("manana").contains("cafe"), "otro triple toque lo devuelve")

// --- Ráfaga al cambiar de mood
esperar(1.2); _ = forzar("normal"); _ = forzar("juegos")
check(n.transitorios["rafaga"] == 12 && !n.capas["rafaga"]!.isHidden, "cambio de mood: ráfaga")
_ = forzar("juegos"); esperar(1.2); check(n.transitorios["rafaga"] == nil && n.capas["rafaga"]!.isHidden, "la ráfaga termina sola")

// --- Lecturas espaciadas
d.vars["nyan_forzar"] = "chat"; n.vuelta = 1; n.actualizarEstado()
check(!n.capasGato.contains("globo"), "la variable de prueba no se relee en cada vuelta")
n.vuelta = 5; n.actualizarEstado(); check(n.capasGato.contains("globo"), "se relee cada 5 vueltas")
n.frente = ("com.valvesoftware.steam", 0); d.vars["nyan_forzar"] = ""; n.vuelta = 0; n.actualizarEstado()
check(n.estado.contains("juegos"), "la app al frente llega por aviso y se usa sin preguntar")
n.bateriaActual = (10, false); n.actualizarEstado(); check(n.estado.contains("bateria_baja"), "la batería llega por aviso")
d.vars["nyan_forzar"] = "normal"; n.vuelta = 0; n.actualizarEstado()

// --- Pausa de instancias que no se ven
check(n.timerEstado == nil, "fuera de pantalla no revisa estados")
let ventana = NSWindow(contentRect: NSRect(x: -3000, y: -3000, width: 200, height: 40), styleMask: .borderless, backing: .buffered, defer: true)
ventana.contentView?.addSubview(n.viewController.view)
check(n.timerEstado != nil, "en pantalla revisa cada segundo")
n.pantallaDormida = true; n.revisarPausa(); check(n.timerEstado == nil, "pantalla dormida: se detiene")
n.pantallaDormida = false; n.revisarPausa(); check(n.timerEstado != nil, "al despertar vuelve")
n.viewController.view.removeFromSuperview(); check(n.timerEstado == nil, "al salir de pantalla se detiene")

print(fallas == 0 ? "ok: \(total) pruebas" : "\(fallas) de \(total) pruebas fallaron")
exit(fallas == 0 ? 0 : 1)
