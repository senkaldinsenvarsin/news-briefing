# Codex'e yapıştırılacak talimat

Aşağıdaki metni olduğu gibi ChatGPT Codex'e yapıştır.

---

## Görev

GitHub reposunu geliştir: https://github.com/senkaldinsenvarsin/news-briefing

Yerel kopya: `/home/arda/news-briefing/`

Bu proje Google Haberler RSS'inden ABD haberlerini toplar (yapay zeka, insansı robot, uzay).

## Kurallar

- Değişiklikleri GitHub'a push et (`git add . && git commit -m "..." && git push`)
- Açıklamalar ve kullanıcıya dönük metinler Türkçe olsun
- Mümkünse sadece Python standart kütüphanesi (pip yok)
- Mevcut dosya yapısını bozma, üzerine ekle

## Mevcut dosyalar

- `config.yaml` — konular ve ayarlar
- `src/main.py` — ana program
- `src/fetch.py` — RSS çekme
- `src/filter.py` — gürültü eleme
- `src/rank.py` — önem sıralaması
- `src/summarize.py` — isteğe bağlı OpenAI özeti

## İyileştirmeler (öncelik sırasıyla)

1. `summarize.py` — OpenAI API ile Türkçe özet; API yoksa düzgün hata mesajı
2. Aynı haberin farklı kaynaklardaki kopyalarını daha iyi birleştir
3. `tests/` altına basit testler
4. `scripts/gunluk.sh` — günlük çalıştırma scripti

## Çalıştırma testi

```bash
cd /home/arda/news-briefing
python3 src/main.py
python3 src/main.py --ozet
```

Her iki komut da hatasız çalışmalı.

---