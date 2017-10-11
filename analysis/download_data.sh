#!/bin/zsh

ssh ______INSTER_URL__________ "php -f ___________downloadlastweek.php" > parking.csv
python3 main.py
chromium-browser hourly-deck-capacity.png
