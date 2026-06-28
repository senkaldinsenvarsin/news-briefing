"""Aday haberler için kısa editör özetleri üretir."""

from __future__ import annotations

from fetch import Haber


def kisa_ozet(haber: Haber) -> str:
    baslik = haber.baslik.strip()
    kaynak = haber.kaynak.strip()
    konu = haber.konu_ad

    return (
        f"{konu} alanında öne çıkan gelişme: {baslik}. "
        f"Hızlı kontrol için kaynak: {kaynak}."
    )
