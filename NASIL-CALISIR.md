# Sistem nasıl çalışıyor? (çok basit anlatım)

## Tek cümleyle

Program haberleri **toplar ve sıralar**. Haberleri **okuyup Türkçe özetleyen** ayrı bir yapay zekadır.

---

## Oyuncular

### 1) Program (bilgisayarındaki kod)
- Google Haberler'den listeyi çeker
- Gereksiz haberleri atar (hisse tavsiyesi vb.)
- Önemli olanları puanlar
- Dosyaya yazar

**Haber okumaz.** Sadece başlık ve link toplar. İnsan gibi makale okumaz.

### 2) Özet yapay zekası (haber okuyan)
İki seçenek:

| Yol | Kim okur? | Ücret |
|-----|-----------|-------|
| Grok'a yapıştır | Ben (Grok) | Ücretsiz |
| `--ozet` komutu | OpenAI | API ücreti |

Bu adımda haberler **gerçekten okunur** ve Türkçe özet yazılır.

### 3) Codex (ChatGPT Codex)
- Sadece **kodu yazmak / düzeltmek** için
- Haber okumaz
- Günlük brifing üretmez

### 4) Grok (ben — sohbet)
- Sistemi kurarım, açıklarım
- `onemli.md` dosyasını yapıştırırsan özetlerim
- Codex'in yazdığı kodu kontrol ederim

---

## İki yapay zeka = karışıklık yok

```
Codex  →  Kod yazar     (tamirci)
Grok   →  Tasarım + özet (editör)
OpenAI →  Otomatik özet  (isteğe bağlı)
Program → Liste toplar   (robot, AI değil)
```

Aynı anda iki AI haber okumaz. Roller ayrı.

---

## GitHub gerekli mi?

**Hayır.**

Her şey şu klasörde:
```
/home/arda/news-briefing/
```

Dosyaları normal klasör gibi kullanırsın. GitHub = internette yedekleme; şimdilik lazım değil.

---

## Senin yapacağın (3 adım)

```bash
cd ~/news-briefing
python3 src/main.py
```

Sonra `output/` klasöründeki `...-onemli.md` dosyasını aç.

Türkçe özet için dosyayı bana yapıştır:
> Bu haberleri Türkçe özetle

Bu kadar.