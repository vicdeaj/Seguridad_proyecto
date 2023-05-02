#from Crypto.Cipher import AES
#from Crypto.Protocol.KDF import PBKDF2
#from Crypto.Random import get_random_bytes
import os, sys
import configparser
import shutil
import tarfile
import uuid
import subprocess


#configparser
configfile = "~/.backupconfig"
config = configparser.ConfigParser()
config.read(os.path.expanduser(configfile))

backup_dir = config.get("BasicConfig", "backup_dir")
source_dir = config.get("BasicConfig", "source_dir")
password = config.get("BasicConfig", "password")

tmp_dir = "/tmp/" + str(uuid.uuid4())
os.mkdir(tmp_dir) #Guardar el archivo comprimido antes de encriptarlo

#Recogida y comprobación de los argumentos
# tipo_copia = sys.argv[1]
# num_args = len(sys.argv) - 1
# if num_args != 1:
#     print("Número de argumentos incorrecto, modo de uso: Primer parámetro(-w, -d, -m)")
#     exit(1)

# establecer una ocupación máxima de disco (avisar antes de superarlo)

# max_size = 100000000000 #100gb
# montajes = {} #diccionario montajes
# with open("/proc/mounts", "r") as f:
#     for linea in f:
#         particion, punto_montaje, tipo_fs, opciones, _, _ = linea.split()
#         montajes[punto_montaje] = particion
#
# ocupacion = shutil.disk_usage(montajes[backup_dir])

# if ocupacion.total >= max_size*0.85:
#     print("Aviso para el administrador, queda poco espacio para guardar las copias de seguridad.\n"
#           "No se va a realizar ninguna copia de seguridad hasta que el problema esté solucionado.")
#     exit(1)

#Programa principal

# if tipo_copia == "-d":
#     pass
#
# if tipo_copia == "-w":
#     pass
#
# if tipo_copia == "-m":
#     pass
#
# print("Argumento mal utilizado, modo de uso: Primer parámetro(-w, -d, -m)")
# exit(1)


# backup semanal

def make_tarfile(output_filename, s_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(s_dir, arcname=os.path.basename(s_dir))


#key = PBKDF2(password, b"\xfe\xfa"*8, dkLen=32)
#aes = AES.new(key, AES.MODE_GCM,nonce=b"05"*12)

nombre_backup = "1.tar.gpg"

path_tarfile = tmp_dir+"/" + "out.tar.gz"
make_tarfile(path_tarfile, source_dir)
path_encriptado = path_tarfile+".gpg"
x = subprocess.run(["gpg","--batch","--no-symkey-cache","--passphrase",password,"-c","-o",path_encriptado, path_tarfile])
os.rename(path_encriptado, backup_dir + "/" + nombre_backup)

#shutil.rmtree(tmp_dir)
# # para cada archivo
# for dirpath, dirnames, filenames in os.walk(backup_dir):
#        for filename in filenames:
#            path = dirpath + "/" + filename
#            with open(path, "rb") as file:
#                contents = file.read()
#                print(contents)
#                cipher_contents, tag = aes.encrypt_and_digest(contents)
#                print(cipher_contents)
#                print(AES.new(PBKDF2(password, b"\xfe\xfa"*8, dkLen=32),AES.MODE_GCM, nonce=b"05"*12).decrypt_and_verify(cipher_contents,tag))
#                # escribir contenidos
#
#             # abrimos,leemos encriptamos, escribimos en el nuevo lugar


#x = open("archivo", "rb")
