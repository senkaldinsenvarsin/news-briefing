#!/usr/bin/env python3
"""Haber Brifingi — ana program."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

# src/ içinden import için
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fetch import haberleri_cek
from filter import filtrele
from rank import sirala_ve_sec
from summarize import turkce_ozet_uret


def yukle_ayarlar(proje_koku: Path) -> dict:
    config_dosya = proje_koku / "config.json"
    if not config_dosya.exists():
        print("Hata: config.json bulunamadı.")
        sys.exit(1)
    return json.loads(config_dosya.read_text(encoding="utf-8"))


def tarih_yaz(tarih) -> str:
    if tarih is None:
        return "tarih bilinmiyor"
    return tarih.strftime("%d %b %Y, %H:%M")


def rapor_yaz(
    konu_gruplari: dict,
    cikti_dosya: Path,
    baslik: str,
    puanli_mi: bool = False,
) -> None:
    satirlar = [
        f"# {baslik}",
        f"",
        f"Oluşturulma: {datetime.now().strftime('%d %B %Y, %H:%M')}",
        f"",
    ]

    for konu in konu_gruplari:
        emoji = konu.get("emoji", "")
        ad = konu["ad"]
        satirlar.append(f"## {emoji} {ad}")
        satirlar.append("")

        haberler = konu["haberler"]
        if not haberler:
            satirlar.append("_Bu konuda haber bulunamadı._")
            satirlar.append("")
            continue

        for i, oge in enumerate(haberler, 1):
            if puanli_mi:
                haber, puan = oge
                satirlar.append(f"### {i}. [{puan} puan] {haber.baslik}")
            else:
                haber = oge
                satirlar.append(f"### {i}. {haber.baslik}")

            satirlar.append(f"- **Kaynak:** {haber.kaynak}")
            satirlar.append(f"- **Tarih:** {tarih_yaz(haber.tarih)}")
            satirlar.append(f"- **Link:** {haber.link}")
            satirlar.append("")

    cikti_dosya.write_text("\n".join(satirlar), encoding="utf-8")


def main() -> None:
    proje_koku = Path(__file__).resolve().parent.parent
    ayarlar = yukle_ayarlar(proje_koku)
    ozet_istegi = "--ozet" in sys.argv

    bolge = ayarlar.get("bolge", {})
    dil = bolge.get("dil", "en-US")
    ulke = bolge.get("ulke", "US")
    gun = ayarlar.get("gun_sayisi", 3)
    max_onemli = ayarlar.get("max_onemli", 8)
    guvenilir = ayarlar.get("guvenilir_kaynaklar", [])

    bugun = datetime.now().strftime("%Y-%m-%d")
    output_dir = proje_koku / "output"
    output_dir.mkdir(exist_ok=True)

    ham_gruplar = []
    onemli_gruplar = []
    toplam = 0

    print("Haberler toplanıyor...")
    for konu in ayarlar["konular"]:
        print(f"  → {konu['ad']}...")
        try:
            ham = haberleri_cek(
                arama=konu["arama"],
                konu_id=konu["id"],
                konu_ad=konu["ad"],
                dil=dil,
                ulke=ulke,
                gun_sayisi=gun,
            )
        except Exception as e:
            print(f"    Uyarı: {konu['ad']} çekilemedi: {e}")
            ham = []

        toplam += len(ham)
        temiz = filtrele(ham, konu.get("dusuk_oncelik", []))
        onemli = sirala_ve_sec(temiz, guvenilir, max_onemli)

        ham_gruplar.append({"ad": konu["ad"], "emoji": konu.get("emoji", ""), "haberler": ham})
        onemli_gruplar.append(
            {"ad": konu["ad"], "emoji": konu.get("emoji", ""), "haberler": onemli}
        )

    ham_dosya = output_dir / f"{bugun}-ham.md"
    onemli_dosya = output_dir / f"{bugun}-onemli.md"

    rapor_yaz(ham_gruplar, ham_dosya, f"Ham Haber Listesi — {bugun}")
    rapor_yaz(onemli_gruplar, onemli_dosya, f"Önemli Haberler — {bugun}", puanli_mi=True)

    print("")
    print(f"✓ Toplam {toplam} haber toplandı")
    print(f"✓ Ham liste:    {ham_dosya}")
    print(f"✓ Önemli liste: {onemli_dosya}")

    if ozet_istegi:
        print("")
        print("Türkçe özet oluşturuluyor...")
        onemli_metin = onemli_dosya.read_text(encoding="utf-8")
        ozet = turkce_ozet_uret(onemli_metin, proje_koku)
        ozet_dosya = output_dir / f"{bugun}-turkce-ozet.md"
        ozet_dosya.write_text(f"# Türkçe Haber Özeti — {bugun}\n\n{ozet}\n", encoding="utf-8")
        print(f"✓ Türkçe özet:  {ozet_dosya}")
    else:
        print("")
        print("Türkçe özet için:")
        print("  python3 src/main.py --ozet")
        print("veya onemli.md dosyasını Grok'a yapıştır.")


if __name__ == "__main__":
    main()