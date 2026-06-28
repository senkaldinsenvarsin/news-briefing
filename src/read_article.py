"""Haber linklerinden makale metni çıkarmaya çalışır."""

from __future__ import annotations

import html
import re
import urllib.request


def _html_metin_yap(raw_html: str) -> str:
    raw_html = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw_html)
    raw_html = re.sub(r"(?is)<style.*?>.*?</style>", " ", raw_html)
    raw_html = re.sub(r"(?is)<noscript.*?>.*?</noscript>", " ", raw_html)
    raw_html = re.sub(r"(?is)<(br|p|div|li|h[1-6])\b[^>]*>", "\n", raw_html)
    raw_html = re.sub(r"(?is)<[^>]+>", " ", raw_html)
    metin = html.unescape(raw_html)
    metin = re.sub(r"[ \t\r\f\v]+", " ", metin)
    metin = re.sub(r"\n\s+", "\n", metin)
    metin = re.sub(r"\n{3,}", "\n\n", metin)
    return metin.strip()


def _makale_gibi_mi(metin: str) -> bool:
    if len(metin) < 300:
        return False
    kucuk = metin[:1200].lower()
    kotu_isaretler = [
        "function(){",
        "window.ij_values",
        "body,html{",
        "var _f_css",
        "webkit-text-size-adjust",
        "boq-dots",
        "apps-debug-tracers",
    ]
    if any(isaret in kucuk for isaret in kotu_isaretler):
        return False
    kelime_sayisi = len(re.findall(r"\b[a-zA-Z]{3,}\b", metin))
    cumle_sayisi = len(re.findall(r"[.!?]\s+[A-Z]", metin))
    return kelime_sayisi >= 60 and cumle_sayisi >= 2


def haber_icerigi_oku(link: str, zaman_asimi: int = 20, max_karakter: int = 6000) -> str:
    """Linki açıp okunabilir düz metin döndürür; başarısızsa boş metin döner."""
    istek = urllib.request.Request(
        link,
        headers={"User-Agent": "Mozilla/5.0 (compatible; HaberBrifingi/1.0)"},
    )
    try:
        with urllib.request.urlopen(istek, timeout=zaman_asimi) as yanit:
            content_type = yanit.headers.get("Content-Type", "")
            veri = yanit.read(max_karakter * 4)
    except Exception:
        return ""

    if "text/html" not in content_type and "text/plain" not in content_type:
        return ""

    charset = "utf-8"
    eslesme = re.search(r"charset=([\w-]+)", content_type, re.I)
    if eslesme:
        charset = eslesme.group(1)

    metin = veri.decode(charset, errors="replace")
    if "text/html" in content_type:
        metin = _html_metin_yap(metin)

    metin = metin[:max_karakter].strip()
    if not _makale_gibi_mi(metin):
        return ""
    return metin
