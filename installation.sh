#!/bin/bash

echo "Welcome to the Backup Script Installation Utility Wizard"
echo "You can modify this setting modifying the file ~/.backupScript/backupConfig"

echo "Tell me the directory to backup: (/tmp/source)"
read source_dir

echo "Tell me the directory were backup will be stored: (/tmp/backup)"
read backup_dir

echo "Tell me the password to use: (CHANGEME)"
read password


rm -rf ~/.backupScript

mkdir ~/.backupScript
mkdir ~/.backupScript/bin

# download files
wget https://github.com/vicdeaj/Seguridad_proyecto/raw/master/backup.py -P ~/.backupScript/bin
mv ~/.backupScript/bin/backup.py ~/.backupScript/bin/backup
chmod 755 ~/.backupScript/bin/backup

wget https://github.com/vicdeaj/Seguridad_proyecto/raw/master/restore.py -P ~/.backupScript/bin
mv ~/.backupScript/bin/restore.py ~/.backupScript/bin/restore
chmod 755 ~/.backupScript/bin/restore

wget https://github.com/vicdeaj/Seguridad_proyecto/raw/master/configExample.txt -P ~/.backupScript
mv ~/.backupScript/configExample.txt ~/.backupScript/backupConfig
chmod 644 ~/.backupScript/backupConfig

# patch config
sed -i "s#^\(backup_dir\s*=\s*\).*\$#\1${backup_dir}#" "$HOME/.backupScript/backupConfig"
sed -i "s#^\(source_dir\s*=\s*\).*\$#\1${source_dir}#" "$HOME/.backupScript/backupConfig"
sed -i "s#^\(password\s*=\s*\).*\$#\1${password}#" "$HOME/.backupScript/backupConfig"


# Set the path to your script
SCRIPT_PATH=/path/to/script.sh

# Add the daily cron job to the user's crontab
daily="0 0 * * * $SCRIPT_PATH -d"

# Add the weekly cron job to the user's crontab
weekly="0 0 * * 0 $SCRIPT_PATH -w"

# Add the monthly cron job to the user's crontab
monthly="0 0 1 * * $SCRIPT_PATH -m"

#(crontab -l 2> /dev/null; echo "$daily") | sort -u | crontab -
#(crontab -l 2> /dev/null; echo "$weekly") | sort -u | crontab -
#(crontab -l 2> /dev/null; echo "$monthly") | sort -u | crontab -