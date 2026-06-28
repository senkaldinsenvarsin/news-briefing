"""Seçilen haberlerden sosyal medya post taslakları üretir."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from summarize import _env_oku


def _manual_prompt(haberler: list[dict]) -> str:
    veri = json.dumps(haberler, ensure_ascii=False, indent=2)
    return f"""# Seçilen Haberler İçin Sosyal Medya Üretim Promptu

Aşağıdaki seçilmiş haberleri kullanarak Türkçe sosyal medya içerikleri hazırla.

Kurallar:
- Sadece verilen seçilmiş haberleri kullan.
- Her haber için X/Twitter postu, Instagram/Threads açıklaması ve LinkedIn postu yaz.
- Her haber için 4:5 dikey görsel üst yazısı üret.
- Her haber için 1080x1350 sosyal medya görsel promptu üret.
- Görsel stili: koyu dramatik arka plan, büyük beyaz başlık, teknoloji haber görseli, net konu sembolleri.
- Uydurma satın alma, rakam, tarih veya şirket ilişkisi ekleme.
- Kaynak linkini koru.

Seçilen haberler:
{veri}
"""


def sosyal_post_uret(haberler: list[dict], proje_koku: Path) -> str:
    """OpenAI varsa post üretir; yoksa seçilen haberler için manuel prompt verir."""
    env = _env_oku(proje_koku)
    api_key = env.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    model = env.get("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key or api_key == "buraya-anahtarini-yaz":
        return (
            "⚠️ OpenAI API anahtarı bulunamadı. Aşağıdaki prompt sadece seçtiğin "
            "haberler için hazırlandı; bunu Grok veya ChatGPT'ye yapıştırabilirsin.\n\n"
            + _manual_prompt(haberler)
        )

    prompt = _manual_prompt(haberler)
    govde = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Türkçe sosyal medya haber editörü. Kısa, doğru ve paylaşılabilir yaz.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
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
        return f"⚠️ OpenAI API hatası ({e.code}): {hata[:500]}"
    except Exception as e:
        return f"⚠️ Sosyal medya postu oluşturulamadı: {e}"
