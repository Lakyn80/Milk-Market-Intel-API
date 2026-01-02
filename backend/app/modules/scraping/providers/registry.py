import re
from typing import Dict, Optional, Tuple

import httpx

try:
    from bs4 import BeautifulSoup
except ImportError as exc:  # pragma: no cover - explicit hint
    raise RuntimeError(
        "BeautifulSoup is required for registry enrichment. Install via `pip install beautifulsoup4`."
    ) from exc


class RegistryEnrichmentProvider:
    """
    Single-company enrichment via Rusprofile HTML.
    - Not part of discovery pipeline.
    - Accepts a company name and returns registry fields.
    """

    SEARCH_URL = "https://www.rusprofile.ru/search"

    LEGAL_FORMS_ABBR = (
        "\u041e\u041e\u041e",  # OOO
        "\u0410\u041e",        # AO
        "\u041f\u0410\u041e",   # PAO
        "\u0417\u0410\u041e",   # ZAO
        "\u0418\u041f",        # IP
    )

    STATUS_WHITELIST = (
        "\u0414\u0435\u0439\u0441\u0442\u0432\u0443\u044e\u0449\u0430\u044f",  # Active
        "\u0414\u0435\u0439\u0441\u0442\u0432\u0443\u044e\u0449\u0430\u044f \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f",  # Active org
        "\u041b\u0438\u043a\u0432\u0438\u0434\u0438\u0440\u043e\u0432\u0430\u043d\u0430",  # Liquidated (fem)
        "\u041b\u0438\u043a\u0432\u0438\u0434\u0438\u0440\u043e\u0432\u0430\u043d\u043e",  # Liquidated (neut)
        "\u0412 \u043f\u0440\u043e\u0446\u0435\u0441\u0441\u0435 \u043b\u0438\u043a\u0432\u0438\u0434\u0430\u0446\u0438\u0438",  # In liquidation
        "\u041f\u0440\u0435\u043a\u0440\u0430\u0442\u0438\u043b\u043e \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c",  # Activity ceased
    )

    def __init__(self, timeout: float = 15.0) -> None:
        self.timeout = timeout

    def enrich_company(self, company_name: str) -> Dict[str, Optional[str]]:
        """
        Look up the company on Rusprofile and parse registry data.
        """
        with httpx.Client(
            timeout=self.timeout,
            headers={"User-Agent": "milk-market-intel/1.0"},
            follow_redirects=True,
        ) as client:
            search_url = self._find_first_company_url(client, company_name)
            if not search_url:
                raise RuntimeError(f"Nenalezen zadny vysledek pro: {company_name}")

            resp = client.get(search_url)
            resp.raise_for_status()
            return self._parse_company_page(resp.text, search_url)

    def _find_first_company_url(self, client: httpx.Client, company_name: str) -> Optional[str]:
        # Rusprofile sends 303 to add type=ul; include it up front.
        resp = client.get(self.SEARCH_URL, params={"query": company_name, "type": "ul"})
        resp.raise_for_status()

        # If search redirects to a single-company detail, use that URL directly.
        final_url = str(resp.url)
        if "/id/" in final_url or "/company/" in final_url:
            return final_url

        soup = BeautifulSoup(resp.text, "html.parser")

        # Preferred selector
        first = soup.select_one(".company-item .company-item__title a")
        if not first:
            # Fallback selector used on some variants
            first = soup.select_one('[itemprop="url"]')

        if first and first.get("href"):
            href = first["href"]
            if href.startswith("http"):
                return href
            return f"https://www.rusprofile.ru{href}"
        return None

    def _normalize_legal_form(self, text: str) -> Optional[str]:
        """Map long form to abbreviation, return None if unknown."""
        if not text:
            return None
        norm = text.strip().upper()
        for abbr in self.LEGAL_FORMS_ABBR:
            if abbr in norm:
                return abbr

        lower = norm.lower()
        if " \u043e\u043e\u043e" in lower or "\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u043e \u0441 \u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u043d\u043e\u0439 \u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u044c\u044e" in lower:
            return "\u041e\u041e\u041e"
        if "\u0430\u043a\u0446\u0438\u043e\u043d\u0435\u0440\u043d\u043e\u0435 \u043e\u0431\u0449\u0435\u0441\u0442\u0432\u043e" in lower and "\u043f\u0443\u0431\u043b\u0438\u0447" in lower:
            return "\u041f\u0410\u041e"
        if "\u0430\u043a\u0446\u0438\u043e\u043d\u0435\u0440\u043d\u043e\u0435 \u043e\u0431\u0449\u0435\u0441\u0442\u0432\u043e" in lower:
            return "\u0410\u041e"
        if "\u0437\u0430\u043a\u0440\u044b\u0442\u043e\u0435 \u0430\u043a\u0446\u0438\u043e\u043d\u0435\u0440\u043d\u043e\u0435 \u043e\u0431\u0449\u0435\u0441\u0442\u0432\u043e" in lower:
            return "\u0417\u0410\u041e"
        if "\u0438\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u043d\u0438\u043c\u0430\u0442\u0435\u043b\u044c" in lower:
            return "\u0418\u041f"
        return None

    def _split_legal_form(self, name: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        """Extract legal form from the beginning of the name and return cleaned name without form/quotes."""
        if not name:
            return None, None

        cleaned = name.strip()
        cleaned = cleaned.strip(' "\'\u00ab\u00bb\u201e\u201c\u201d')

        pattern = re.compile(
            r"^(?P<form>\u041e\u041e\u041e|\u0410\u041e|\u041f\u0410\u041e|\u0417\u0410\u041e|\u0418\u041f)\s+[\"\u00ab\u00bb\u201e\u201c\u201d]*?(?P<body>.+)$",
            re.IGNORECASE,
        )
        match = pattern.match(cleaned)
        if match:
            form = match.group("form").upper()
            body = match.group("body").strip(' "\'\u00ab\u00bb\u201e\u201c\u201d')
            # Drop stray leading/trailing quotes again if unbalanced
            body = re.sub(r'^[\"\u00ab\u00bb\u201e\u201c\u201d]+', "", body).strip()
            body = re.sub(r'[\"\u00ab\u00bb\u201e\u201c\u201d]+$', "", body).strip()
            body = body.replace('"', "").replace("\u00ab", "").replace("\u00bb", "").strip()
            return form, body

        return None, cleaned

    def _parse_company_page(self, html: str, url: str) -> Dict[str, Optional[str]]:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        text_lower = text.lower()

        def find_first(pattern: str) -> Optional[str]:
            match = re.search(pattern, text)
            return match.group(1).strip() if match else None

        def find_by_label(labels: tuple[str, ...]) -> Optional[str]:
            label_match = soup.find(
                lambda tag: tag.name in {"div", "span", "td", "th", "dt"}
                and any(lbl in tag.get_text(" ", strip=True) for lbl in labels)
            )
            if label_match:
                nxt = label_match.find_next(
                    lambda tag: tag.name in {"div", "span", "td", "dd"}
                    and tag.get_text(strip=True)
                )
                if nxt:
                    return nxt.get_text(" ", strip=True)
            return None

        legal_name_el = soup.find("h1")
        legal_name_raw = legal_name_el.get_text(strip=True) if legal_name_el else None

        # Derive legal form and clean name
        form_from_name, cleaned_name = self._split_legal_form(legal_name_raw)

        ogrn = find_first(r"\u041e\u0413\u0420\u041d\s*([\d]{10,15})")  # OGRN
        inn = find_first(r"\u0418\u041d\u041d\s*([\d]{10,12})")  # INN

        form_from_label_raw = find_by_label(
            ("\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u043e\u043d\u043d\u043e-\u043f\u0440\u0430\u0432\u043e\u0432\u0430\u044f \u0444\u043e\u0440\u043c\u0430", "\u041e\u041f\u0424")
        )
        form_from_label = self._normalize_legal_form(form_from_label_raw) if form_from_label_raw else None
        legal_form = form_from_name or form_from_label

        # Status
        status_raw = find_by_label(("\u0421\u0442\u0430\u0442\u0443\u0441",))
        status = None
        if status_raw:
            lower = status_raw.lower()
            for st in self.STATUS_WHITELIST:
                if st.lower() in lower:
                    status = st
                    break
        # Fallback: search in the whole page text
        if not status:
            for st in self.STATUS_WHITELIST:
                if st.lower() in text_lower:
                    status = st
                    break

        # Address
        address = find_by_label(("\u0410\u0434\u0440\u0435\u0441",))
        if not address:
            addr_node = soup.select_one("[itemprop='address']")
            if addr_node:
                address = addr_node.get_text(" ", strip=True)
        if not address:
            address = find_first(r"\u0410\u0434\u0440\u0435\u0441\s*([^,]{5,200})")

        if not address:
            meta_addr = soup.find("meta", attrs={"itemprop": "address"})
            if meta_addr and meta_addr.get("content"):
                address = meta_addr["content"]

        return {
            "legal_name": cleaned_name,
            "ogrn": ogrn,
            "inn": inn,
            "legal_form": legal_form,
            "status": status,
            "address": address,
            "source_url": url,
        }
