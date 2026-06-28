from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fetch import Haber
from rank import sirala_ve_sec


class RankTests(unittest.TestCase):
    def test_min_puan_altindaki_haber_doldurma_icin_secilemez(self) -> None:
        haber = Haber(
            baslik="Generic artificial intelligence commentary",
            kaynak="Example",
            link="https://example.com",
            tarih=None,
            konu_id="ai",
            konu_ad="Yapay Zeka",
            kaynak_url="https://example.com",
        )
        self.assertEqual(sirala_ve_sec([haber], [], max_adet=8, min_puan=23), [])


if __name__ == "__main__":
    unittest.main()
