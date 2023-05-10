import glob
import os
import shutil
import configparser
import uuid
import subprocess
import time
import tarfile


#config
configfile = "~/.backupScript/backupConfig"
config = configparser.ConfigParser()
config.read(os.path.expanduser(configfile))

backup_dir = config.get("BasicConfig","backup_dir")
restore_dir = config.get("BasicConfig", "source_dir")
password = config.get("BasicConfig", "password")

archivos = []
while True:
    for archivo in glob.glob(os.path.join(backup_dir, '**'), recursive=True):
        if os.path.isfile(archivo):
            tipo = os.path.split(os.path.split(archivo)[0])[1]
            timestamp = os.path.getmtime(archivo)
            archivos.append((timestamp, tipo, archivo))

    archivos.sort()
    contador = 0
    for archivo in archivos:
        mod_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(archivo[0]))
        print(f"{contador} : {mod_time} : {archivo[1]}")
        contador += 1

    copia_restaurar = input("Elige una copia para restaurar:")
    if copia_restaurar.isdigit() and 0 <= int(copia_restaurar) <= contador:
        idCopia = int(copia_restaurar)
        break
    else:
        print("No ha seleccionado un índice válido.")



#Comprobacion de si existe directorio del restore
if not os.path.exists(restore_dir):
    os.makedirs(restore_dir)
else:
    for filename in os.listdir(restore_dir):
        file_path = os.path.join(restore_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Error al eliminar el archivo {0}. Razón: {1}'.format(file_path, e))


tmp_dir = "/tmp/" + str(uuid.uuid4())
os.mkdir(tmp_dir)

def restaurar_backup_completa(pathBackup):
    pathTar = tmp_dir + "/tmp.tar"
    subprocess.run(
        ["gpg", "--batch", "--no-symkey-cache", "--passphrase", password, "-d", "-o", pathTar, pathBackup],stderr=subprocess.DEVNULL)
    with tarfile.open(pathTar, mode="r:gz") as tar:
        tar.extractall(path=os.path.split(restore_dir)[0])


def restaurar_backup_incremental(pathBackup):
    pathTar = tmp_dir + "/tmp2.tar"
    subprocess.run(
        ["gpg", "--batch", "--no-symkey-cache", "--passphrase", password, "-d", "-o", pathTar, pathBackup],stderr=subprocess.DEVNULL)
    with tarfile.open(pathTar, mode="r:gz") as tar:
        for file_ in tar:
            try:
                tar.extract(file_, path=os.path.split(restore_dir)[0])
            except IOError:
                os.remove(file_.name)
                tar.extract(file_, path=os.path.split(restore_dir)[0])
        try:
            to_remove = open(os.path.split(restore_dir)[0] + "/.archivos_a_eliminar", "r").readlines()
            os.remove(os.path.split(restore_dir)[0] + "/.archivos_a_eliminar")
            for l in to_remove:
                os.remove(os.path.split(restore_dir)[0] + "/" +l.strip())
        except FileNotFoundError:
            pass




copiaARestaurar = archivos[idCopia] # (timestamp, tipo, path)
if copiaARestaurar[1] == "diaria":
    backupRef = backup_dir + "/semanal/" + os.path.split(copiaARestaurar[2])[1].split("_")[1] # Todo check path bien
    restaurar_backup_completa(backupRef)
    restaurar_backup_incremental(copiaARestaurar[2])
else:
    restaurar_backup_completa(copiaARestaurar[2])


shutil.rmtree(tmp_dir)
