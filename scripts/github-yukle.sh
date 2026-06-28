#!/bin/bash
# GitHub'a yükle (önce bir kez: gh auth login)

set -e
cd /home/arda/news-briefing

if ! gh auth status >/dev/null 2>&1; then
  echo "Önce tarayıcıdan GitHub girişi gerekli:"
  echo "  gh auth login --web"
  exit 1
fi

# Repo yoksa oluştur ve yükle
if gh repo view "$(gh api user -q .login)/news-briefing" >/dev/null 2>&1; then
  echo "Repo zaten var, güncelleniyor..."
  git push -u origin main
else
  echo "Yeni repo oluşturuluyor..."
  gh repo create news-briefing --public --source=. --remote=origin --push
fi

echo ""
echo "Tamam! Adres:"
gh repo view --web --json url -q .url