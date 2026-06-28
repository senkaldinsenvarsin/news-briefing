from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import main
from fetch import Haber
from read_article import _makale_gibi_mi
from social import sosyal_post_uret


class SocialFlowTests(unittest.TestCase):
    def test_post_numaralari_parses_comma_list(self) -> None:
        self.assertEqual(main.post_numaralari(["main.py", "--post", "1,3,7"]), [1, 3, 7])

    def test_adaylari_yaz_outputs_json_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            adaylar = [
                {
                    "no": 1,
                    "konu_id": "ai",
                    "konu_ad": "Yapay Zeka",
                    "baslik": "OpenAI announces new model",
                    "kaynak": "Example",
                    "kaynak_url": "https://example.com",
                    "link": "https://example.com/news",
                    "tarih": "2026-06-28T12:00:00+00:00",
                    "puan": 30,
                    "kisa_ozet": "Yapay Zeka alanında öne çıkan gelişme.",
                    "icerik": "Long article text",
                }
            ]

            md_dosya = tmp_path / "adaylar.md"
            json_dosya = tmp_path / "adaylar.json"
            main.adaylari_yaz(adaylar, md_dosya, json_dosya)

            self.assertEqual(json.loads(json_dosya.read_text(encoding="utf-8")), adaylar)
            md = md_dosya.read_text(encoding="utf-8")
            self.assertIn("python3 src/main.py --post 1,3,7", md)
            self.assertIn("OpenAI announces new model", md)
            self.assertIn("Kısa özet", md)

    def test_api_yokken_sadece_secilen_haber_prompta_girer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proje = Path(tmp)
            secilen = [
                {"no": 2, "baslik": "Selected AI news", "link": "https://example.com/selected"}
            ]
            metin = sosyal_post_uret(secilen, proje)

            self.assertIn("OpenAI API anahtarı bulunamadı", metin)
            self.assertIn("Selected AI news", metin)
            self.assertNotIn("Unselected AI news", metin)

    def test_google_news_kod_parcasi_makale_sayilmaz(self) -> None:
        kod = "body,html{height:100%;overflow:hidden}" * 30
        self.assertFalse(_makale_gibi_mi(kod))

    def test_uzaydan_gelen_cursor_haberi_ai_kategorisine_tasinir(self) -> None:
        h = Haber(
            baslik="SpaceX deal for Cursor reshuffles enterprise coding market",
            kaynak="Example",
            link="https://example.com",
            tarih=None,
            konu_id="uzay",
            konu_ad="Uzay",
            kaynak_url="https://example.com",
        )
        main.kategori_duzelt(h)
        self.assertEqual(h.konu_id, "ai")
        self.assertEqual(h.konu_ad, "Yapay Zeka")


if __name__ == "__main__":
    unittest.main()
