# GitHub Rehberi — Sıfırdan, Türkçe

Bu rehber `news-briefing` projesini GitHub'a yüklemen için yazıldı.
Programlama bilmen gerekmez; adımları sırayla takip et.

---

## GitHub nedir? (1 cümle)

GitHub = projelerini internette sakladığın bir site. Yedek + Codex/Grok ile paylaşım kolaylığı.

---

## BÖLÜM 1: GitHub hesabı aç

1. Tarayıcıda git: **https://github.com**
2. Sağ üst **Sign up** (Kayıt ol)
3. E-posta, şifre belirle — ücretsiz plan yeterli
4. E-postanı doğrula

---

## BÖLÜM 2: Bilgisayarında bir kez ayar (5 dakika)

Terminali aç ve **kendi adın ve e-postanla** şunu yaz (örnekleri değiştir):

```bash
git config --global user.name "Arda"
git config --global user.email "senin@email.com"
```

> `user.email` olarak GitHub'a kayıtlı e-postanı kullan.

Kontrol:
```bash
git config --global user.name
git config --global user.email
```

---

## BÖLÜM 3: GitHub'da boş depo (repository) oluştur

1. GitHub'da giriş yap
2. Sağ üst **+** → **New repository**
3. Ayarlar:
   - **Repository name:** `news-briefing`
   - **Public** veya **Private** (ikisi de olur; private = sadece sen görürsün)
   - **ÖNEMLİ:** "Add a README file" kutusunu **işaretleme**
   - "Add .gitignore" → **işaretleme**
4. **Create repository** tıkla

Açılan sayfada komutlar görünür. **"…or push an existing repository from the command line"** bölümünü kullanacağız.

---

## BÖLÜM 4: Projeyi GitHub'a yükle

Terminalde sırayla (zaten hazırlandı, sadece push kaldı):

```bash
cd ~/news-briefing
git status
```

İlk commit zaten yapıldıysa doğrudan:

```bash
git remote add origin https://github.com/KULLANICI_ADIN/news-briefing.git
git branch -M main
git push -u origin main
```

> `KULLANICI_ADIN` yerine kendi GitHub kullanıcı adını yaz.
> Örnek: `https://github.com/arda42/news-briefing.git`

### Şifre sorarsa

GitHub artık şifre kabul etmez. İki yol:

**Yol A — Tarayıcı ile giriş (kolay):**
```bash
sudo apt install gh
gh auth login
```
Sorulara: GitHub.com → HTTPS → Login with a web browser → kodu yapıştır.

Sonra tekrar:
```bash
git push -u origin main
```

**Yol B — Kişisel erişim anahtarı (token):**
1. GitHub → sağ üst profil → **Settings**
2. Sol menü en altta **Developer settings**
3. **Personal access tokens** → **Tokens (classic)** → **Generate new token**
4. İsim: `news-briefing`, süre: 90 days, kutucuk: **repo** işaretle
5. Oluşan token'ı kopyala (bir daha gösterilmez!)
6. `git push` şifre sorunca: kullanıcı adın + **şifre yerine token'ı** yapıştır

---

## BÖLÜM 5: Başardın mı kontrol et

Tarayıcıda aç:
```
https://github.com/KULLANICI_ADIN/news-briefing
```

Dosyaları görüyorsan tamam: `README.md`, `src/`, `config.json` vb.

---

## Sonradan değişiklik yüklemek (günlük kullanım)

Codex veya Grok bir şey değiştirdikten sonra:

```bash
cd ~/news-briefing
git add .
git commit -m "Yapılan değişikliğin kısa açıklaması"
git push
```

Bu 3 komut = "güncellemeyi GitHub'a gönder"

| Komut | Ne yapar? (basit) |
|-------|-------------------|
| `git add .` | Tüm değişiklikleri paketle |
| `git commit -m "..."` | Pakete not yapıştır |
| `git push` | GitHub'a yükle |

---

## Codex ile GitHub

Codex bazen doğrudan GitHub repo'na bağlanabilir. Repo URL'ini ver:
```
https://github.com/KULLANICI_ADIN/news-briefing
```

---

## Asla GitHub'a yükleme

- `.env` dosyası (API anahtarın) — `.gitignore` bunu engelliyor
- `output/` içindeki günlük raporlar — gereksiz

---

## Sorun çıkarsa

| Hata | Çözüm |
|------|-------|
| `remote origin already exists` | `git remote set-url origin https://github.com/...` |
| `Authentication failed` | `gh auth login` veya yeni token |
| `Permission denied` | Repo adı / kullanıcı adı yanlış olabilir |

Takıldığın adımı bana yaz; birlikte çözeriz.