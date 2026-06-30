"""Small, cached-friendly Japanese-to-Korean keyword translation client."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable

import requests


API_URL = "https://api.mymemory.translated.net/get"

# Curated translations keep demo mode deterministic and avoid unnecessary calls.
CURATED_JA_KO = {
    "猛暑日": "폭염일",
    "プロ野球速報": "프로야구 속보",
    "台風情報": "태풍 정보",
    "新作アニメ": "신작 애니메이션",
    "花火大会": "불꽃축제",
    "推し活": "최애 활동",
    "iPhone": "아이폰",
    "MLB": "메이저리그",
    "コンビニ新商品": "편의점 신상품",
    "旅行セール": "여행 할인",
    "資格試験": "자격시험",
    "夏フェス": "여름 페스티벌",
}


class TranslationError(RuntimeError):
    """Raised when the external translation service returns no usable text."""


def translate_ja_to_ko(text: str, timeout: int = 8) -> str:
    clean = text.strip()
    if not clean:
        return clean
    if clean in CURATED_JA_KO:
        return CURATED_JA_KO[clean]
    try:
        response = requests.get(
            API_URL,
            params={"q": clean, "langpair": "ja|ko", "mt": 1},
            headers={"User-Agent": "AsiaTrendDashboard/1.0"},
            timeout=timeout,
        )
        response.raise_for_status()
        body = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise TranslationError(f"번역 요청 실패: {exc}") from exc

    translated = str(body.get("responseData", {}).get("translatedText", "")).strip()
    if not translated or "MYMEMORY WARNING" in translated.upper():
        raise TranslationError("번역 결과가 비어 있습니다.")
    return translated


def translate_many(texts: Iterable[str], max_workers: int = 5) -> dict[str, str]:
    unique = list(dict.fromkeys(text.strip() for text in texts if text.strip()))
    results = {text: CURATED_JA_KO[text] for text in unique if text in CURATED_JA_KO}
    pending = [text for text in unique if text not in results]
    if not pending:
        return results

    with ThreadPoolExecutor(max_workers=min(max_workers, len(pending))) as executor:
        futures = {executor.submit(translate_ja_to_ko, text): text for text in pending}
        for future in as_completed(futures):
            text = futures[future]
            try:
                results[text] = future.result()
            except TranslationError:
                # Callers intentionally fall back to the Japanese original.
                continue
    return results
