from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from editorial import ret_nedeni
from fetch import Haber


def haber(baslik: str, kaynak: str = "Example", konu_id: str = "ai") -> Haber:
    return Haber(
        baslik=baslik,
        kaynak=kaynak,
        link="https://example.com",
        tarih=None,
        konu_id=konu_id,
        konu_ad="Test",
        kaynak_url="https://example.com",
    )


class EditorialTests(unittest.TestCase):
    def test_ai_yatirim_haberi_elenir(self) -> None:
        h = haber("Big Tech AI camps but smart money is not chasing OpenAI")
        self.assertEqual(ret_nedeni(h), "finans/yatirim haberi")

    def test_ai_urun_anlasmasi_kalir(self) -> None:
        h = haber("Google DeepMind strikes AI research deal with A24")
        self.assertIsNone(ret_nedeni(h))

    def test_ai_hukuk_sosyal_gundemi_elenir(self) -> None:
        h = haber("Regulating artificial intelligence will be colossal task for lawmakers")
        self.assertEqual(ret_nedeni(h), "teknoloji disi sosyal/hukuk gundemi")

    def test_ai_elektrik_altyapi_haberi_kalir(self) -> None:
        h = haber("Could artificial intelligence raise your electric bill?")
        self.assertIsNone(ret_nedeni(h))

    def test_ai_pop_kultur_rehber_haberi_elenir(self) -> None:
        h = haber("Steven Spielberg's A.I. Artificial Intelligence foretold our solitude")
        self.assertEqual(ret_nedeni(h), "teknoloji disi sosyal/hukuk gundemi")

    def test_ai_yorum_yazisi_elenir(self) -> None:
        h = haber("What Will AI Do To Our Minds?")
        self.assertEqual(ret_nedeni(h), "teknoloji disi sosyal/hukuk gundemi")

    def test_paywall_kaynak_elenir(self) -> None:
        h = haber("Robots, not chatbots, will realise AI potential", "Financial Times")
        self.assertEqual(ret_nedeni(h), "paywall riski")

    def test_robot_uretim_haberi_kalir(self) -> None:
        h = haber(
            "AGIBOT's 15,000th Robot Rolls Off the Production Line",
            "AgiBot",
            "robot",
        )
        self.assertIsNone(ret_nedeni(h))

    def test_uzay_finans_haberi_elenir(self) -> None:
        h = haber("Is SpaceX Really Worth More Than Micron and AMD Combined?", "Yahoo", "uzay")
        self.assertEqual(ret_nedeni(h), "finans/yatirim haberi")

    def test_uzay_ipo_haberi_elenir(self) -> None:
        h = haber("NASA awards and the biggest IPO ever: a commercial space boom", "NBC", "uzay")
        self.assertEqual(ret_nedeni(h), "finans/yatirim haberi")

    def test_uzay_cursor_haberi_yanlis_kategori_sayilir(self) -> None:
        h = haber("SpaceX buys Cursor in enterprise coding market", "Yahoo", "uzay")
        self.assertEqual(ret_nedeni(h), "yanlis kategori: yapay zeka haberi")


if __name__ == "__main__":
    unittest.main()
