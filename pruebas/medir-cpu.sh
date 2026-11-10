#!/bin/zsh
# Mide cuánta CPU usan BetterTouchTool y los procesos que dibujan la Touch Bar durante N segundos (60 por defecto).
# Uso: zsh pruebas/medir-cpu.sh etiqueta [segundos]   → agrega una línea a resultados.tsv, al lado de este script.
# CPU en % de un núcleo, a partir del tiempo de CPU acumulado (ps) al inicio y al final.
zmodload zsh/datetime
etiqueta=$1; seg=${2:-60}; aqui=${0:A:h}
pids=($(pgrep -x BetterTouchTool) $(pgrep -x TouchBarServer) $(pgrep -x WindowServer))
(( ${#pids} == 3 )) || { echo "falta un proceso: ${pids}"; exit 1; }
cpu() { for p in $pids; do ps -o time= -p $p | awk -F: '{printf "%s ", $1*60+$2}'; done; }
idlew() { top -l 1 -pid $pids[1] -stats pid,idlew | awk -v p=$pids[1] '$1==p {gsub(/\+/,"",$2); print $2}'; }
# Con la Touch Bar atenuada por inactividad, TouchBarServer gasta mucho menos: se la mantiene despierta para comparar.
caffeinate -u -t $((seg + 5)) &
sleep 2
c0=($(cpu)); w0=$(idlew); t0=$EPOCHREALTIME
sleep $seg
c1=($(cpu)); w1=$(idlew); t1=$EPOCHREALTIME
brillo=$(screencapture -x -b /tmp/nyan-medir.png && python3 -c "from PIL import Image; im=Image.open('/tmp/nyan-medir.png').convert('L'); print(round(sum(im.getdata())/(im.width*im.height)))"; rm -f /tmp/nyan-medir.png)
python3 -c "
dt=$t1-$t0; c0=[$c0[1],$c0[2],$c0[3]]; c1=[$c1[1],$c1[2],$c1[3]]
b,t,w=[(y-x)/dt*100 for x,y in zip(c0,c1)]
print(f'$etiqueta\t{dt:.0f}s\tBTT {b:.2f} %\tTouchBarServer {t:.2f} %\tWindowServer {w:.2f} %\tdespertares BTT {($w1-$w0)/dt:.1f}/s\tbrillo Touch Bar $brillo')" | tee -a $aqui/resultados.tsv
