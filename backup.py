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

def make_tarfile_incremental(output_filename, s_dir, reference_filename):
    #Propuesta de implementación Javimo
    #fecha_referencia = os.path.getmtime(reference_filename)
    with tarfile.open(output_filename, "w:gz") as tar:
        #for archivo in os.listdir(s_dir):
            #ruta_archivo = os.path.join(s_dir, archivo)
            #Comprobación de si ha sido modificado
            #fecha_modificacion = os.path.getmt
            #if fecha_modificacion > fecha_referencia:
                #Formato de la fecha (no se cual es el bueno, lo modificamos cuando lo hablemos)
                #fecha_modificacion_legible = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(fecha_modificacion))
                #La manera de nombrar el archivo también la cambiamos que no sé como es ahora mismo
                #nombre_archivo_copia = f"{archivo}_{fecha_modificacion_legible}.tar.gz"
                #tar.add(ruta_archivo, arcname=nombre_archivo_copia)
    
    
# coje dos directorios, y hace una backup del primero en el segundo
def crear_backup_completa(source, destination):
    nombre_backup = "{}.tar.gpg".format(int(time.time()))
    path_tarfile = tmp_dir+"/" + "out.tar.gz"
    make_tarfile(path_tarfile, source)
    path_encriptado = path_tarfile+".gpg"
    x = subprocess.run(["gpg","--batch","--no-symkey-cache","--passphrase",password,"-c","-o",path_encriptado, path_tarfile])
    os.rename(path_encriptado, destination + "/" + nombre_backup)

def crear_backup_incremental(source, destination, refs):
    if os.listdir(refs) == 0:
        crear_backup_completa(source,refs)

    # archivo de backup semanal
    nombre_archivo_referencia = max(os.listdir(refs))
    archivo_referencia = refs + "/" + nombre_archivo_referencia

    nombre_backup = "{}_{}.tar.gpg".format(int(time.time()), nombre_archivo_referencia)
    path_tarfile = tmp_dir + "/" + "out.tar.gz"
    make_tarfile_incremental(path_tarfile, source, archivo_referencia)
    path_encriptado = path_tarfile+".gpg"
    x = subprocess.run(["gpg","--batch","--no-symkey-cache","--passphrase",password,"-c","-o",path_encriptado, path_tarfile])
    os.rename(path_encriptado, destination + "/" + nombre_backup)

def check_espacio_disponible(backup_dir):
    path_semanal = backup_dir + "/semanal"
    path_mensual = backup_dir + "/mensual"
    path_diario = backup_dir + "/diaria"

    ocupacion_total = 0
    for path in [path_semanal, path_mensual, path_diario]:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                ocupacion_total += os.path.getsize(filepath)

    return ocupacion_total


def check_structura_backup(path):
    carpetas = os.listdir(path)
    if "semanal" not in carpetas:
        os.mkdir(backup_dir + "/semanal")

    if "mensual" not in carpetas:
        os.mkdir(backup_dir + "/mensual")

    if "diaria" not in carpetas:
        os.mkdir(backup_dir + "/diaria")


#configparser
configfile = "~/.backupconfig"
config = configparser.ConfigParser()
config.read(os.path.expanduser(configfile))

backup_dir = config.get("BasicConfig", "backup_dir")
source_dir = config.get("BasicConfig", "source_dir")
password = config.get("BasicConfig", "password")

tmp_dir = "/tmp/" + str(uuid.uuid4())
os.mkdir(tmp_dir) #Guardar el archivo comprimido antes de encriptarlo


#Programa principal

# Recogida y comprobación de los argumentos
tipo_copia = sys.argv[1]
num_args = len(sys.argv) - 1
if num_args != 1:
    print("Número de argumentos incorrecto, modo de uso: Primer parámetro(-w, -d, -m)")
    exit(0)

# establecer una ocupación máxima de disco (avisar antes de superarlo)

max_size = 100000000000 #100gb

ocupacion_used = check_espacio_disponible(backup_dir)
if ocupacion_used >= max_size*0.85:
     print("Aviso para el administrador, queda poco espacio para guardar las copias de seguridad.\n"
           "No se va a realizar ninguna copia de seguridad hasta que el problema esté solucionado.")
     exit(0)

# checkear estructura del backupdir

check_structura_backup(backup_dir)

if tipo_copia == "-d":
    lista_archivos_diaria = os.listdir(backup_dir + "/diaria")
    n_backups_diaria = len(lista_archivos_diaria)
    backup_mas_vieja_diaria = min(lista_archivos_diaria)
    if n_backups_diaria >= 7:
        os.remove(backup_mas_vieja_diaria)

    crear_backup_incremental(source_dir, backup_dir + "/diaria", backup_dir + "/semanal")
    exit(0)


if tipo_copia == "-w":
    lista_archivos_semanal = os.listdir(backup_dir + "/semanal")
    n_backups_semanales = len(lista_archivos_semanal)
    backup_mas_vieja_semanal = min(lista_archivos_semanal)
    if n_backups_semanales >= 4:
        os.remove(backup_mas_vieja_semanal)

    crear_backup_completa(source_dir, backup_dir + "/semanal")
    exit(0)


if tipo_copia == "-m":
    lista_archivos_mensual= os.listdir(backup_dir + "/mensual")
    n_backups_mensual = len(lista_archivos_mensual)
    backup_mas_vieja_mensual = min(lista_archivos_mensual)
    if n_backups_mensual >= 12:
        os.remove(backup_mas_vieja_mensual)

    crear_backup_completa(source_dir, backup_dir + "/mensual")
    exit(0)

print("Argumento mal utilizado, modo de uso: Primer parámetro(-w, -d, -m)")
exit(1)




shutil.rmtree(tmp_dir)
