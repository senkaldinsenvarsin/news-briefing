#!/bin/bash
# Her gün otomatik haber toplama

cd /home/arda/news-briefing || exit 1
python3 src/main.py >> output/cron-log.txt 2>&1

# API anahtarın varsa Türkçe özet de üret:
# python3 src/main.py --ozet >> output/cron-log.txt 2>&1