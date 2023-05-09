#!/bin/bash

# Set the path to your script
SCRIPT_PATH=/path/to/script.sh

# Add the daily cron job to the user's crontab
daily="0 0 * * * $SCRIPT_PATH -d"

# Add the weekly cron job to the user's crontab
weekly="0 0 * * 0 $SCRIPT_PATH -w"

# Add the monthly cron job to the user's crontab
monthly="0 0 1 * * $SCRIPT_PATH -m"

(crontab -l 2> /dev/null; echo "$daily") | sort -u | crontab -
(crontab -l 2> /dev/null; echo "$weekly") | sort -u | crontab -
(crontab -l 2> /dev/null; echo "$monthly") | sort -u | crontab -