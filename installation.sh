#!/bin/bash

echo "Benvinguts a Backup Script Installation Utility Wizard"
echo "Despuse de la instalación, puedes modificar los ajustes en: ~/.backupScript/backupConfig"

echo "Carpeta que se va a resguardar: (/tmp/source)"
read source_dir

echo "Donde se van a guardar las backups: (/tmp/backup)"
read backup_dir

echo "Con que contraseña se van a cifrar: (CHANGEME)"
read password


rm -rf ~/.backupScript

mkdir ~/.backupScript
mkdir ~/.backupScript/bin

echo "Descargando archivos ..."
# download files
wget https://github.com/vicdeaj/Seguridad_proyecto/raw/master/backup.py -P ~/.backupScript/bin 2> /dev/null
mv ~/.backupScript/bin/backup.py ~/.backupScript/bin/backup
chmod 755 ~/.backupScript/bin/backup

wget https://github.com/vicdeaj/Seguridad_proyecto/raw/master/restore.py -P ~/.backupScript/bin 2> /dev/null
mv ~/.backupScript/bin/restore.py ~/.backupScript/bin/restore
chmod 755 ~/.backupScript/bin/restore

wget https://github.com/vicdeaj/Seguridad_proyecto/raw/master/configExample.txt -P ~/.backupScript 2> /dev/null
mv ~/.backupScript/configExample.txt ~/.backupScript/backupConfig
chmod 644 ~/.backupScript/backupConfig

# patch config
if [ -n "$backup_dir" ]; then
    sed -i "s#^\(backup_dir\s*=\s*\).*\$#\1${backup_dir}#" "$HOME/.backupScript/backupConfig"
fi

if [ -n "$source_dir" ]; then
  sed -i "s#^\(source_dir\s*=\s*\).*\$#\1${source_dir}#" "$HOME/.backupScript/backupConfig"
fi

if [ -n "$password" ]; then
  sed -i "s#^\(password\s*=\s*\).*\$#\1${password}#" "$HOME/.backupScript/backupConfig"
fi

# Set the path to your script
SCRIPT_PATH=$HOME/.backupScript/bin/backup

# Add the daily cron job to the user's crontab
daily="0 0 * * * $SCRIPT_PATH -d"
# Add the weekly cron job to the user's crontab
weekly="0 0 * * 0 $SCRIPT_PATH -w"
# Add the monthly cron job to the user's crontab
monthly="0 0 1 * * $SCRIPT_PATH -m"

echo "Quires instalar el script de backups en tu archivo cron? (Y/n)"
read instalar_cron

if [[ -z "$instalar_cron" || "$instalar_cron" == "Y" ]]; then
  (crontab -l 2> /dev/null; echo "$daily") | sort -u | crontab -
  (crontab -l 2> /dev/null; echo "$weekly") | sort -u | crontab -
  (crontab -l 2> /dev/null; echo "$monthly") | sort -u | crontab -
fi

echo "Quieres añadir los scripts a tu PATH (modifica .bashrc)? (Y/n)"
read anadir_path

if [[ -z "$anadir_path" || "$anadir_path" == "Y" ]]; then
  echo 'export PATH="$HOME/.backupScript/bin:$PATH"' >> "$HOME/.bashrc"
  echo "Ejecuta source ~/.bashrc para añadirlo al path de esta sesion"
fi

