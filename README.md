# Haber Brifingi — Otomatik Sistem

Bu proje, Google Haberler'deki ABD haberlerini toplar, önemli olanları seçer ve sana Türkçe özet rapor hazırlar.

## Kim ne yapıyor? (kısa ve net)

| Rol | Ne işe yarar? | Haber okur mu? |
|-----|---------------|----------------|
| **Sen** | Komutları çalıştırır, raporu okursun | Hayır |
| **Grok (ben)** | Sistemi tasarladım, yardım ederim, istersen burada da özetlerim | Evet (sohbet edersen) |
| **Codex** | Kodu yazmak / düzeltmek için kullanırsın | Hayır |
| **Çalışan program** | Her gün haberleri toplar | Hayır (sadece listeler) |
| **Özet yapay zekası** | Seçilen haberleri okuyup Türkçe özet yazar | **Evet** |

**Önemli:** İki yapay zeka aynı anda haber okumaz.

- **Codex** = tamirci (kodu yazar)
- **Özet AI** = okuyucu (haberleri okur) — bu OpenAI veya Grok API olabilir

GitHub **şart değil**. Her şey `~/news-briefing/` klasöründe duruyor.

---

## Hızlı başlangıç

### 1) Haberleri topla (yapay zeka gerekmez)

```bash
cd ~/news-briefing
python3 src/main.py
```

Bu komut `output/` klasörüne iki dosya yazar:
- `YYYY-MM-DD-ham.md` — tüm haber listesi
- `YYYY-MM-DD-onemli.md` — önemli görünenler (henüz Türkçe özet yok)

### 2) Türkçe özet al (yapay zeka gerekir)

**Seçenek A — Bana sor (ücretsiz, manuel):**
`output/` içindeki `onemli.md` dosyasını Grok'a yapıştır:
> "Bu haberleri oku ve Türkçe özetle"

**Seçenek B — Tam otomasyon (API anahtarı gerekir):**
`.env` dosyasına OpenAI anahtarını yaz, sonra:
```bash
python3 src/main.py --ozet
```

---

## Konular (config.json)

- Yapay zeka
- İnsansı robotlar
- Uzay

Bölge: ABD (`en-US`)

---

## Codex ile geliştirme

`CODEX-ICIN.md` dosyasını Codex'e yapıştır. Codex kodu yazar; haber okumaz.

---

## Günlük otomatik çalıştırma

`scripts/gunluk.sh` dosyasına bak. Cron kurulumu için `KURULUM.md` dosyasına bak.