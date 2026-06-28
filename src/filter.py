"""Düşük kaliteli / alakasız haberleri eler."""

from __future__ import annotations

from fetch import Haber, benzersiz_anahtar


def dusuk_oncelik_mi(haber: Haber, dusuk_kelimeler: list[str]) -> bool:
    baslik = haber.baslik.lower()
    return any(k.lower() in baslik for k in dusuk_kelimeler)


def tekrarlari_birlestir(haberler: list[Haber]) -> list[Haber]:
    """Aynı olayın farklı kaynaklardaki kopyalarını tek haberde toplar."""
    gruplar: dict[str, Haber] = {}
    ek_kaynaklar: dict[str, list[str]] = {}

    for haber in haberler:
        anahtar = benzersiz_anahtar(haber.baslik)
        if anahtar not in gruplar:
            gruplar[anahtar] = haber
            ek_kaynaklar[anahtar] = []
        else:
            ek_kaynaklar[anahtar].append(haber.kaynak)

    sonuc = []
    for anahtar, haber in gruplar.items():
        ekstra = ek_kaynaklar.get(anahtar, [])
        if ekstra:
            haber.kaynak = f"{haber.kaynak} (+{len(ekstra)} kaynak)"
        sonuc.append(haber)
    return sonuc


def filtrele(haberler: list[Haber], dusuk_kelimeler: list[str]) -> list[Haber]:
    elenen = [h for h in haberler if not dusuk_oncelik_mi(h, dusuk_kelimeler)]
    return tekrarlari_birlestir(elenen)