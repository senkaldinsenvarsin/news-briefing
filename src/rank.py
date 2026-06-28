"""Haberlere önem puanı verir."""

from __future__ import annotations

import re
from datetime import datetime, timezone

from fetch import Haber


ONEMLI_KELIMELER = [
    "openai",
    "google",
    "microsoft",
    "nvidia",
    "anthropic",
    "nasa",
    "spacex",
    "figure",
    "tesla",
    "optimus",
    "regulation",
    "ban",
    "launch",
    "breakthrough",
    "billion",
    "ipo",
    "merger",
    "humanoid",
    "robot",
    "starship",
    "artemis",
    "iss",
    "policy",
    "lawsuit",
    "fda",
    "pentagon",
    "defense",
]


def _kaynak_puani(kaynak: str, guvenilir: list[str]) -> int:
    kaynak_l = kaynak.lower()
    for domain in guvenilir:
        if domain in kaynak_l:
            return 15
    if "(+" in kaynak:
        # Birden fazla kaynakta geçiyor
        try:
            sayi = int(re.search(r"\+(\d+)", kaynak).group(1))
            return 10 + min(sayi * 3, 15)
        except (AttributeError, ValueError):
            return 10
    return 0


def _tazelik_puani(tarih: datetime | None) -> int:
    if tarih is None:
        return 0
    if tarih.tzinfo is None:
        tarih = tarih.replace(tzinfo=timezone.utc)
    simdi = datetime.now(timezone.utc)
    saat = (simdi - tarih).total_seconds() / 3600
    if saat < 6:
        return 20
    if saat < 24:
        return 15
    if saat < 48:
        return 10
    if saat < 72:
        return 5
    return 0


def _baslik_puani(baslik: str) -> int:
    kucuk = baslik.lower()
    puan = 0
    for kelime in ONEMLI_KELIMELER:
        if kelime in kucuk:
            puan += 4
    if any(x in kucuk for x in ("announces", "unveils", "launches", "first", "new")):
        puan += 5
    return min(puan, 30)


def puanla(haber: Haber, guvenilir_kaynaklar: list[str]) -> int:
    return (
        _kaynak_puani(haber.kaynak, guvenilir_kaynaklar)
        + _tazelik_puani(haber.tarih)
        + _baslik_puani(haber.baslik)
    )


def sirala_ve_sec(
    haberler: list[Haber],
    guvenilir_kaynaklar: list[str],
    max_adet: int,
) -> list[tuple[Haber, int]]:
    puanli = [(h, puanla(h, guvenilir_kaynaklar)) for h in haberler]
    puanli.sort(key=lambda x: x[1], reverse=True)
    return puanli[:max_adet]