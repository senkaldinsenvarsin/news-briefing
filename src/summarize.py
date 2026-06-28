"""İsteğe bağlı: OpenAI ile Türkçe özet üretir."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path


def _env_oku(proje_koku: Path) -> dict[str, str]:
    env_dosya = proje_koku / ".env"
    degerler: dict[str, str] = {}
    if not env_dosya.exists():
        return degerler
    for satir in env_dosya.read_text(encoding="utf-8").splitlines():
        satir = satir.strip()
        if not satir or satir.startswith("#") or "=" not in satir:
            continue
        anahtar, deger = satir.split("=", 1)
        degerler[anahtar.strip()] = deger.strip()
    return degerler


def turkce_ozet_uret(haber_metni: str, proje_koku: Path) -> str:
    """
    OpenAI API ile Türkçe özet.
    API anahtarı yoksa anlaşılır Türkçe hata mesajı döner.
    """
    env = _env_oku(proje_koku)
    api_key = env.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    model = env.get("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key or api_key == "buraya-anahtarini-yaz":
        return (
            "⚠️ Türkçe özet için OpenAI API anahtarı gerekli.\n\n"
            "Yapman gerekenler:\n"
            "1. `.env.ornek` dosyasını `.env` olarak kopyala\n"
            "2. OPENAI_API_KEY satırına anahtarını yaz\n"
            "3. `python3 src/main.py --ozet` komutunu tekrar çalıştır\n\n"
            "Veya ücretsiz yol: `output/...-onemli.md` dosyasını Grok'a yapıştır "
            "ve 'Türkçe özetle' de."
        )

    prompt = f"""Sen bir haber editörüsün. Aşağıdaki İngilizce haber listesini oku.
Her haber için Türkçe kısa özet yaz.

Kurallar:
- En fazla 10 haber özetle
- Her haber: başlık (Türkçe), neden önemli (1 cümle), özet (2 cümle), kaynak
- Sade ve anlaşılır Türkçe kullan
- Teknik İngilizce terim kullanma

Haber listesi:
{haber_metni}
"""

    govde = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Türkçe haber editörü. Kısa ve net yaz."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    istek = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(govde).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(istek, timeout=120) as yanit:
            veri = json.loads(yanit.read().decode("utf-8"))
        return veri["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        hata = e.read().decode("utf-8", errors="replace")
        return f"⚠️ OpenAI API hatası ({e.code}): {hata[:300]}"
    except Exception as e:
        return f"⚠️ Özet oluşturulamadı: {e}"