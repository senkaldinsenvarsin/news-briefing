"""Google Haberler RSS'ten haber çeker."""

from __future__ import annotations

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


@dataclass
class Haber:
    baslik: str
    kaynak: str
    link: str
    tarih: datetime | None
    konu_id: str
    konu_ad: str


def _rss_url(arama: str, dil: str, ulke: str, gun_sayisi: int) -> str:
    sorgu = f"{arama} when:{gun_sayisi}d"
    params = {
        "q": sorgu,
        "hl": dil,
        "gl": ulke,
        "ceid": f"{ulke}:{dil.split('-')[0]}",
    }
    base = "https://news.google.com/rss/search"
    return f"{base}?{urllib.parse.urlencode(params)}"


def _temiz_baslik(raw: str) -> str:
    # "Başlık - Kaynak" formatından başlığı ayır
    if " - " in raw:
        return raw.rsplit(" - ", 1)[0].strip()
    return raw.strip()


def _parse_tarih(text: str | None) -> datetime | None:
    if not text:
        return None
    try:
        return parsedate_to_datetime(text)
    except (TypeError, ValueError):
        return None


def haberleri_cek(
    arama: str,
    konu_id: str,
    konu_ad: str,
    dil: str = "en-US",
    ulke: str = "US",
    gun_sayisi: int = 3,
    zaman_asimi: int = 30,
) -> list[Haber]:
    url = _rss_url(arama, dil, ulke, gun_sayisi)
    istek = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; HaberBrifingi/1.0)"},
    )
    with urllib.request.urlopen(istek, timeout=zaman_asimi) as yanit:
        xml_veri = yanit.read()

    kok = ET.fromstring(xml_veri)
    haberler: list[Haber] = []

    for item in kok.findall("./channel/item"):
        baslik_el = item.find("title")
        link_el = item.find("link")
        tarih_el = item.find("pubDate")
        kaynak_el = item.find("source")

        if baslik_el is None or link_el is None:
            continue

        baslik = _temiz_baslik(baslik_el.text or "")
        kaynak = (kaynak_el.text if kaynak_el is not None else "") or "Bilinmiyor"
        link = (link_el.text or "").strip()

        if not baslik or not link:
            continue

        haberler.append(
            Haber(
                baslik=baslik,
                kaynak=kaynak,
                link=link,
                tarih=_parse_tarih(tarih_el.text if tarih_el is not None else None),
                konu_id=konu_id,
                konu_ad=konu_ad,
            )
        )

    return haberler


def benzersiz_anahtar(baslik: str) -> str:
    """Benzer başlıkları gruplamak için basit anahtar."""
    kucuk = baslik.lower()
    kucuk = re.sub(r"[^a-z0-9\s]", "", kucuk)
    kelimeler = [k for k in kucuk.split() if len(k) > 3]
    return " ".join(kelimeler[:6])