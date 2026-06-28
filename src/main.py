#!/usr/bin/env python3
"""Haber Brifingi — ana program."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

# src/ içinden import için
sys.path.insert(0, str(Path(__file__).resolve().parent))

from brief import kisa_ozet
from editorial import editor_filtresi
from fetch import haberleri_cek
from filter import filtrele
from rank import sirala_ve_sec
from read_article import haber_icerigi_oku
from social import sosyal_post_uret
from summarize import turkce_ozet_uret


KATEGORI_TASIMA = [
    ("uzay", ["cursor", "grok", "coding market", "enterprise coding"], "ai", "Yapay Zeka"),
]


def kategori_duzelt(haber) -> None:
    baslik = haber.baslik.lower()
    for kaynak_konu, kelimeler, hedef_id, hedef_ad in KATEGORI_TASIMA:
        if haber.konu_id == kaynak_konu and any(k in baslik for k in kelimeler):
            haber.konu_id = hedef_id
            haber.konu_ad = hedef_ad
            return


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


def tarih_json(tarih) -> str | None:
    if tarih is None:
        return None
    return tarih.isoformat()


def post_numaralari(argv: list[str]) -> list[int] | None:
    if "--post" not in argv:
        return None
    index = argv.index("--post")
    if index + 1 >= len(argv):
        print("Hata: --post için haber numarası yaz. Örnek: python3 src/main.py --post 1,3,7")
        sys.exit(1)
    ham = argv[index + 1].replace(" ", "")
    try:
        numaralar = [int(x) for x in ham.split(",") if x]
    except ValueError:
        print("Hata: Haber numaraları virgülle ayrılmış sayı olmalı. Örnek: 1,3,7")
        sys.exit(1)
    if not numaralar:
        print("Hata: En az bir haber numarası seçmelisin.")
        sys.exit(1)
    return numaralar


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
            if getattr(haber, "kaynak_url", ""):
                satirlar.append(f"- **Kaynak sitesi:** {haber.kaynak_url}")
            satirlar.append(f"- **Tarih:** {tarih_yaz(haber.tarih)}")
            satirlar.append(f"- **Link:** {haber.link}")
            satirlar.append("")

    cikti_dosya.write_text("\n".join(satirlar), encoding="utf-8")


def adaylari_yaz(adaylar: list[dict], md_dosya: Path, json_dosya: Path) -> None:
    json_dosya.write_text(json.dumps(adaylar, ensure_ascii=False, indent=2), encoding="utf-8")

    satirlar = [
        "# Paylaşım İçin Aday Haberler",
        "",
        "Bu dosyada haberleri gör, paylaşmak istediklerinin numarasını seç.",
        "",
        "Post üretmek için örnek:",
        "`python3 src/main.py --post 1,3,7`",
        "",
        "Not: Sosyal medya postu ve görsel promptu sadece seçtiğin numaralar için üretilir.",
        "",
    ]
    for aday in adaylar:
        satirlar.append(f"## {aday['no']}. {aday['baslik']}")
        satirlar.append(f"- **Konu:** {aday['konu_ad']}")
        satirlar.append(f"- **Kaynak:** {aday['kaynak']}")
        if aday.get("kaynak_url"):
            satirlar.append(f"- **Kaynak sitesi:** {aday['kaynak_url']}")
        satirlar.append(f"- **Tarih:** {aday['tarih'] or 'tarih bilinmiyor'}")
        satirlar.append(f"- **Puan:** {aday['puan']}")
        satirlar.append(f"- **Kısa özet:** {aday['kisa_ozet']}")
        satirlar.append(f"- **Link:** {aday['link']}")
        if aday.get("icerik"):
            kisa = aday["icerik"][:700].replace("\n", " ")
            satirlar.append(f"- **Okunan içerik kısa parça:** {kisa}")
        else:
            satirlar.append("- **Okunan içerik:** Alınamadı; başlık/kaynak/link mevcut.")
        satirlar.append("")

    md_dosya.write_text("\n".join(satirlar), encoding="utf-8")


def elenenleri_yaz(elenenler: list[dict], dosya: Path) -> None:
    satirlar = [
        "# Elenen Haberler",
        "",
        "Bu haberler paywall, finans gürültüsü veya konu dışı olduğu için aday listesine alınmadı.",
        "",
    ]
    if not elenenler:
        satirlar.append("_Elenen haber yok._")
    for haber in elenenler:
        satirlar.append(f"## {haber['baslik']}")
        satirlar.append(f"- **Konu:** {haber['konu_ad']}")
        satirlar.append(f"- **Kaynak:** {haber['kaynak']}")
        if haber.get("kaynak_url"):
            satirlar.append(f"- **Kaynak sitesi:** {haber['kaynak_url']}")
        satirlar.append(f"- **Neden:** {haber['neden']}")
        satirlar.append(f"- **Link:** {haber['link']}")
        satirlar.append("")
    dosya.write_text("\n".join(satirlar), encoding="utf-8")


def post_modu_calistir(proje_koku: Path, numaralar: list[int]) -> None:
    bugun = datetime.now().strftime("%Y-%m-%d")
    output_dir = proje_koku / "output"
    aday_json = output_dir / f"{bugun}-adaylar.json"
    if not aday_json.exists():
        print(f"Hata: Bugünün aday dosyası bulunamadı: {aday_json}")
        print("Önce haberleri toplamak için şunu çalıştır:")
        print("  python3 src/main.py")
        sys.exit(1)

    adaylar = json.loads(aday_json.read_text(encoding="utf-8"))
    aday_map = {aday["no"]: aday for aday in adaylar}
    eksik = [no for no in numaralar if no not in aday_map]
    if eksik:
        print(f"Hata: Bu haber numaraları bulunamadı: {', '.join(map(str, eksik))}")
        print(f"Geçerli aralık: 1-{len(adaylar)}")
        sys.exit(1)

    secilenler = [aday_map[no] for no in numaralar]
    metin = sosyal_post_uret(secilenler, proje_koku)
    post_dosya = output_dir / f"{bugun}-sosyal-postlar.md"
    post_dosya.write_text(f"# Sosyal Medya Post Taslakları — {bugun}\n\n{metin}\n", encoding="utf-8")

    print(f"✓ Seçilen haber sayısı: {len(secilenler)}")
    print(f"✓ Sosyal medya taslakları: {post_dosya}")


def main() -> None:
    proje_koku = Path(__file__).resolve().parent.parent
    numaralar = post_numaralari(sys.argv)
    if numaralar is not None:
        post_modu_calistir(proje_koku, numaralar)
        return

    ayarlar = yukle_ayarlar(proje_koku)
    ozet_istegi = "--ozet" in sys.argv

    bolge = ayarlar.get("bolge", {})
    dil = bolge.get("dil", "en-US")
    ulke = bolge.get("ulke", "US")
    gun = ayarlar.get("gun_sayisi", 3)
    max_onemli = ayarlar.get("max_onemli", 8)
    min_puan = ayarlar.get("min_puan", 0)
    guvenilir = ayarlar.get("guvenilir_kaynaklar", [])

    bugun = datetime.now().strftime("%Y-%m-%d")
    output_dir = proje_koku / "output"
    output_dir.mkdir(exist_ok=True)

    ham_gruplar = []
    onemli_gruplar = []
    adaylar = []
    elenenler = []
    toplam = 0
    sira = 1

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
        for haber in ham:
            kategori_duzelt(haber)
        temiz = filtrele(ham, konu.get("dusuk_oncelik", []))
        editoryal_temiz, editoryal_elenen = editor_filtresi(temiz)
        for haber, neden in editoryal_elenen:
            elenenler.append(
                {
                    "konu_id": haber.konu_id,
                    "konu_ad": haber.konu_ad,
                    "baslik": haber.baslik,
                    "kaynak": haber.kaynak,
                    "kaynak_url": haber.kaynak_url,
                    "link": haber.link,
                    "tarih": tarih_json(haber.tarih),
                    "neden": neden,
                }
            )
        onemli = sirala_ve_sec(editoryal_temiz, guvenilir, max_onemli, min_puan)

        print(f"    {len(onemli)} önemli aday okunuyor...")
        for haber, puan in onemli:
            haber.icerik = haber_icerigi_oku(haber.link)
            adaylar.append(
                {
                    "no": sira,
                    "konu_id": haber.konu_id,
                    "konu_ad": haber.konu_ad,
                    "baslik": haber.baslik,
                    "kaynak": haber.kaynak,
                    "kaynak_url": haber.kaynak_url,
                    "link": haber.link,
                    "tarih": tarih_json(haber.tarih),
                    "puan": puan,
                    "kisa_ozet": kisa_ozet(haber),
                    "icerik": haber.icerik,
                }
            )
            sira += 1

        ham_gruplar.append({"ad": konu["ad"], "emoji": konu.get("emoji", ""), "haberler": ham})
        onemli_gruplar.append(
            {"ad": konu["ad"], "emoji": konu.get("emoji", ""), "haberler": onemli}
        )

    ham_dosya = output_dir / f"{bugun}-ham.md"
    onemli_dosya = output_dir / f"{bugun}-onemli.md"
    aday_md = output_dir / f"{bugun}-adaylar.md"
    aday_json = output_dir / f"{bugun}-adaylar.json"
    elenen_dosya = output_dir / f"{bugun}-elenenler.md"

    rapor_yaz(ham_gruplar, ham_dosya, f"Ham Haber Listesi — {bugun}")
    rapor_yaz(onemli_gruplar, onemli_dosya, f"Önemli Haberler — {bugun}", puanli_mi=True)
    adaylari_yaz(adaylar, aday_md, aday_json)
    elenenleri_yaz(elenenler, elenen_dosya)

    print("")
    print(f"✓ Toplam {toplam} haber toplandı")
    print(f"✓ Ham liste:    {ham_dosya}")
    print(f"✓ Önemli liste: {onemli_dosya}")
    print(f"✓ Aday liste:   {aday_md}")
    print(f"✓ Elenenler:    {elenen_dosya}")
    print("")
    print("Paylaşmak istediğin haberleri seçtikten sonra örnek:")
    print("  python3 src/main.py --post 1,3,7")

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
