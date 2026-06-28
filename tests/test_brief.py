from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from brief import kisa_ozet
from fetch import Haber


class BriefTests(unittest.TestCase):
    def test_kisa_ozet_baslik_konu_kaynak_icerir(self) -> None:
        haber = Haber(
            baslik="Google DeepMind strikes AI research deal with A24",
            kaynak="IBC.org",
            link="https://example.com",
            tarih=None,
            konu_id="ai",
            konu_ad="Yapay Zeka",
            kaynak_url="https://example.com",
        )

        ozet = kisa_ozet(haber)

        self.assertIn("Yapay Zeka", ozet)
        self.assertIn("Google DeepMind", ozet)
        self.assertIn("IBC.org", ozet)


if __name__ == "__main__":
    unittest.main()
