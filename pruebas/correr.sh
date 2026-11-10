#!/bin/zsh
# Compila el plugin como lo hace BTT y corre las pruebas de comportamiento.
# Uso: zsh pruebas/correr.sh   (desde la raíz del repo, después de python3 generar.py)
set -e
raiz=${0:A:h:h}; tmp=$(mktemp -d); trap "rm -rf $tmp" EXIT
h=/Applications/BetterTouchTool.app/Contents/Resources/BTTSwiftPluginHeader.h
swiftc -O -emit-library -import-objc-header $h $raiz/NyanCat.swift -o $tmp/NyanCat.dylib -Xlinker -undefined -Xlinker dynamic_lookup
sed 's/private //g' $raiz/NyanCat.swift > $tmp/Nyan.swift  # las pruebas miran el estado interno
swiftc -import-objc-header $h $tmp/Nyan.swift $raiz/pruebas/main.swift -o $tmp/pruebas -Xlinker -undefined -Xlinker dynamic_lookup
$tmp/pruebas
