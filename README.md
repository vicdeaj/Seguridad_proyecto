#Installation
run: \ 
tmpfile="$(mktemp)" && wget -qO "$tmpfile" "https://github.com/vicdeaj/Seguridad_proyecto/raw/master/installation.sh" && bash "$tmpfile" && rm "$tmpfile"