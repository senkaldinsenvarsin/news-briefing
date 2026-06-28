# Kurulum Rehberi (Türkçe, basit)

## Gerekenler

- Linux bilgisayarın (zaten var)
- Python 3 (zaten yüklü)
- İnternet bağlantısı

**Gerekmeyenler:**
- GitHub hesabı
- İngilizce programlama bilgisi
- Ücretli bir şey (özet için API kullanmazsan)

---

## Adım 1: Haberleri topla

Terminali aç ve şunu yaz:

```bash
cd ~/news-briefing
python3 src/main.py
```

Başarılı olursa şunu görürsün:
```
Rapor hazır: .../output/2026-06-28-onemli.md
```

Bu dosyayı herhangi bir metin editörüyle açabilirsin.

---

## Adım 2: Türkçe özet (ücretsiz yol)

1. `output/` klasöründeki `...-onemli.md` dosyasını aç
2. İçeriği kopyala
3. Grok'a yapıştır ve de:
   > Bu haberleri oku, en önemli 10 tanesini Türkçe özetle. Her biri için: başlık, neden önemli, 2 cümle özet, link.

Bu yol **yarı otomatik**: toplama otomatik, özet seninle birlikte.

---

## Adım 3: Tam otomasyon (isteğe bağlı)

OpenAI hesabın varsa:

1. `cp .env.ornek .env` komutunu çalıştır
2. `.env` dosyasını aç, `OPENAI_API_KEY=` satırına anahtarını yaz
3. Şunu çalıştır:
   ```bash
   python3 src/main.py --ozet
   ```

Bu sefer `...-turkce-ozet.md` dosyası da oluşur.

---

## Adım 4: Her sabah otomatik çalışsın (isteğe bağlı)

Terminalde:
```bash
crontab -e
```

Açılan dosyanın en altına şunu ekle (sabah 08:00):
```
0 8 * * * /home/arda/news-briefing/scripts/gunluk.sh
```

Kaydet ve çık. Artık her sabah 08:00'de haberler toplanır.

---

## Codex ile birlikte geliştirme

1. `CODEX-ICIN.md` dosyasını aç
2. İçeriği Codex'e yapıştır
3. Codex kodu günceller
4. Bana "Codex şunu yaptı, kontrol et" de — ben kontrol ederim

GitHub kullanmana gerek yok. Dosyalar `~/news-briefing/` içinde.