#from Crypto.Cipher import AES
#from Crypto.Protocol.KDF import PBKDF2
#from Crypto.Random import get_random_bytes
import os, sys
import configparser
import shutil
import tarfile
import uuid
import subprocess
import time

# backup semanal

def make_tarfile(output_filename, s_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(s_dir, arcname=os.path.basename(s_dir))


# coje dos directorios, y hace una backup del primero en el segundo
def crear_backup_completa(source, destination):
    nombre_backup = "{}.tar.gpg".format(int(time.time()))
    path_tarfile = tmp_dir+"/" + "out.tar.gz"
    make_tarfile(path_tarfile, source)
    path_encriptado = path_tarfile+".gpg"
    x = subprocess.run(["gpg","--batch","--no-symkey-cache","--passphrase",password,"-c","-o",path_encriptado, path_tarfile])
    os.rename(path_encriptado, destination + "/" + nombre_backup)


#configparser
configfile = "~/.backupconfig"
config = configparser.ConfigParser()
config.read(os.path.expanduser(configfile))

backup_dir = config.get("BasicConfig", "backup_dir")
source_dir = config.get("BasicConfig", "source_dir")
password = config.get("BasicConfig", "password")

tmp_dir = "/tmp/" + str(uuid.uuid4())
os.mkdir(tmp_dir) #Guardar el archivo comprimido antes de encriptarlo

# Recogida y comprobación de los argumentos
tipo_copia = sys.argv[1]
num_args = len(sys.argv) - 1
if num_args != 1:
    print("Número de argumentos incorrecto, modo de uso: Primer parámetro(-w, -d, -m)")
    exit(1)

# establecer una ocupación máxima de disco (avisar antes de superarlo)

max_size = 100000000000 #100gb
montajes = {} #diccionario montajes
with open("/proc/mounts", "r") as f:
    for linea in f:
        particion, punto_montaje, tipo_fs, opciones, _, _ = linea.split()
        montajes[punto_montaje] = particion

ocupacion = shutil.disk_usage(montajes[backup_dir])

if ocupacion.total >= max_size*0.85:
    print("Aviso para el administrador, queda poco espacio para guardar las copias de seguridad.\n"
          "No se va a realizar ninguna copia de seguridad hasta que el problema esté solucionado.")
    exit(1)

#Programa principal

if tipo_copia == "-d":
     pass

if tipo_copia == "-w":
    lista_archivos = os.listdir(backup_dir + "/semanal")
    n_backups_semanales = len(lista_archivos)
    backup_mas_vieja = min(lista_archivos)
    if n_backups_semanales >= 4:
        os.remove(backup_mas_vieja)

    crear_backup_completa(source_dir, backup_dir + "/semanal")


if tipo_copia == "-m":
    lista_archivos = os.listdir(backup_dir + "/mensual")
    n_backups_semanales = len(lista_archivos)
    backup_mas_vieja = min(lista_archivos)

    crear_backup_completa(source_dir, backup_dir + "/mensual")
    exit(1)

print("Argumento mal utilizado, modo de uso: Primer parámetro(-w, -d, -m)")
exit(1)




shutil.rmtree(tmp_dir)