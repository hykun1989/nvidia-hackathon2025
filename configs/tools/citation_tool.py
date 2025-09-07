import re
import json
from typing import List, Dict, Any
from collections import Counter
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s\)\]\\\">']+")

def _extract_urls_and_snippets(text: str, context_chars: int = 120) -> List[Dict[str, Any]]:
    results = []
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip('.,)')
        start = max(0, m.start() - context_chars)
        end = min(len(text), m.end() + context_chars)
        snippet = text[start:end].strip()
        results.append({"url": url, "snippet": snippet})
    return results

def aggregate_citations(observations: List[Any], top_k: int = 3) -> Dict[str, Any]:
    if not observations:
        return {"sources": [], "markdown": "No observations provided."}

    all_url_snips = []
    for obs in observations:
        text = ""
        if isinstance(obs, dict):
            text = obs.get("text") or obs.get("content") or json.dumps(obs, ensure_ascii=False)
        else:
            text = str(obs)
        all_url_snips.extend(_extract_urls_and_snippets(text))

    if not all_url_snips:
        return {"sources": [], "markdown": "未在观测结果中找到可解析的 URL。"}

    counts = Counter([u["url"] for u in all_url_snips])
    aggregated = {}
    for entry in all_url_snips:
        url = entry["url"]
        if url not in aggregated:
            aggregated[url] = {"url": url, "snippet": entry["snippet"], "count": 0}
        aggregated[url]["count"] += 1
        if len(entry["snippet"]) < len(aggregated[url]["snippet"]):
            aggregated[url]["snippet"] = entry["snippet"]

    sorted_sources = sorted(aggregated.values(), key=lambda x: (-x["count"], len(x["snippet"])))
    top = sorted_sources[:top_k]

    for s in top:
        try:
            s["domain"] = urlparse(s["url"]).netloc
        except Exception:
            s["domain"] = ""

    md_lines = [f"### Top-{len(top)} 引用来源与片段", ""]
    for i, s in enumerate(top, 1):
        md_lines.append(f"{i}. [{s['domain']}]({s['url']})  (hits: {s['count']})")
        md_lines.append("")
        md_lines.append(f"> {s['snippet']}")
        md_lines.append("")

    markdown = "\n".join(md_lines)
    return {"sources": top, "markdown": markdown}

if __name__ == "__main__":
    import sys
    data = sys.stdin.read()
    try:
        observations = json.loads(data)
    except Exception:
        observations = [data]
    print(json.dumps(aggregate_citations(observations), ensure_ascii=False, indent=2))