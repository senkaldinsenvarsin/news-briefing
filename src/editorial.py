"""Haber değeri ve yayınlanabilirlik için editör kuralları."""

from __future__ import annotations

from fetch import Haber


PAYWALL_KAYNAKLAR = [
    "albuquerque journal",
    "bloomberg.com",
    "financial times",
    "ft.com",
]

FINANS_GURULTU = [
    "stock",
    "stocks",
    "stock is",
    "smart money",
    "investor",
    "investment",
    "growth stocks",
    "growth opportunity",
    "worth more than",
    "ipo",
    "nasdaq",
    "portfolio",
    "etf",
    "ipo lifted",
    "according to billionaire investor",
    "shares",
]

OPINION_GURULTU = [
    "opinion:",
    "op-ed",
    "commentary:",
]

SOSYAL_HUKUK_GURULTU = [
    "lawmakers",
    "commission",
    "regulating",
    "regulation",
    "policy",
    "lawsuit",
    "politics",
    "job market",
    "job scams",
    "students",
    "hiring",
    "theater",
    "spielberg",
    "our minds",
    "types of ai users",
    "burdens of the ai era",
    "keynote",
    "event planners",
    "ultimate guide",
    "public university",
    "county employees",
]

UZAY_TEKNOLOJI_TERIMLERI = [
    "nasa",
    "spacex",
    "starship",
    "starlink",
    "satellite",
    "launch",
    "moon",
    "mars",
    "artemis",
    "rocket",
    "space station",
    "astronomy",
    "telescope",
    "mission",
    "orbit",
]

AI_TEKNOLOJI_TERIMLERI = [
    "openai",
    "google",
    "deepmind",
    "anthropic",
    "nvidia",
    "microsoft",
    "model",
    "agentic",
    "chatbot",
    "data center",
    "data centers",
    "artificial intelligence",
    "ai",
    "demand",
    "supply",
    "research deal",
    "electric bill",
    "cursor",
    "grok",
    "coding",
]

ROBOT_TEKNOLOJI_TERIMLERI = [
    "humanoid",
    "robot",
    "robotics",
    "embodied ai",
    "manufacturing",
    "nvidia",
    "agi",
    "optimus",
]

KAYNAK_KARA_LISTE = [
    "bitget",
    "futuristsspeakers.com",
]


def _icerir(metin: str, kelimeler: list[str]) -> bool:
    return any(k in metin for k in kelimeler)


def paywall_riski_mi(haber: Haber) -> bool:
    kaynak = haber.kaynak.lower()
    return _icerir(kaynak, PAYWALL_KAYNAKLAR)


def ret_nedeni(haber: Haber) -> str | None:
    baslik = haber.baslik.lower()
    kaynak = haber.kaynak.lower()
    konu = haber.konu_id

    if _icerir(kaynak, KAYNAK_KARA_LISTE):
        return "dusuk kaliteli kaynak"

    if paywall_riski_mi(haber):
        return "paywall riski"

    if _icerir(baslik, OPINION_GURULTU):
        return "opinion/kose yazisi"

    if konu in ("ai", "uzay") and _icerir(baslik, FINANS_GURULTU):
        return "finans/yatirim haberi"

    if konu == "ai" and _icerir(baslik, SOSYAL_HUKUK_GURULTU):
        return "teknoloji disi sosyal/hukuk gundemi"

    if konu == "uzay" and not _icerir(baslik, UZAY_TEKNOLOJI_TERIMLERI):
        return "uzay teknolojisiyle dogrudan ilgili degil"

    if konu == "uzay" and _icerir(baslik, ["cursor", "grok", "coding market", "enterprise coding"]):
        return "yanlis kategori: yapay zeka haberi"

    if konu == "ai" and not _icerir(baslik, AI_TEKNOLOJI_TERIMLERI):
        return "yapay zeka teknolojisiyle dogrudan ilgili degil"

    if konu == "robot" and not _icerir(baslik, ROBOT_TEKNOLOJI_TERIMLERI):
        return "robot teknolojisiyle dogrudan ilgili degil"

    return None


def editor_filtresi(haberler: list[Haber]) -> tuple[list[Haber], list[tuple[Haber, str]]]:
    kabul: list[Haber] = []
    retler: list[tuple[Haber, str]] = []
    for haber in haberler:
        neden = ret_nedeni(haber)
        if neden:
            retler.append((haber, neden))
        else:
            kabul.append(haber)
    return kabul, retler
