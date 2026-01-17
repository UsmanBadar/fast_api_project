import json
import textwrap
from typing import Any, Dict, List

def generate_prompt(company_profile: Dict[str, Any],
                    fundamental_metrics: List[Dict[str, Any]],
                    balance_sheet: Dict[str, Any]) -> str:
    payload = {
        "company_profile": company_profile,
        "fundamentals": fundamental_metrics,
        "balance_sheet": balance_sheet
    }

    prompt = f"""
    Role: You are an equity research assistant.

    Task:
    Analyse the company using ONLY the data inside INPUT_DATA_JSON.
    Do not invent numbers, dates, products, risks, news, or assumptions.
    If a required value is missing, use null or "not_provided".

    Output rules:
    Return STRICT JSON ONLY.
    No markdown.
    No code fences.
    No commentary.
    No extra keys.
    All numbers must be numbers.
    All percentages must be numbers (example 75, not "75%").
    Arrays must be arrays of strings.
    If target price cannot be calculated because current share price is missing, set target_price_12mo to null and upside_pct to null and include a short reason in target_price_note.

    JSON_SCHEMA (must match exactly):
    {{
      "symbol": "string",
      "company_name": "string",
      "as_of_date": "YYYY-MM-DD or not_provided",
      "overall_rating": "BUY or HOLD or SELL",
      "confidence_pct": number,
      "strengths": ["string", "string", "string"],
      "concerns": ["string", "string", "string"],
      "investment_outlook": "string",
      "upside_pct": number or null,
      "target_price_note": "string",
      "risk_level": "Low or Moderate or High",
      "suitability": "string",
      "recommendation": {{
        "accumulate_below": number or null,
        "stop_loss": number or null,
        "allocation_guidance": {{
          "balanced_pct_range": "string",
          "conservative_pct_range": "string"
        }},
        "notes": "string"
      }},
      "data_used": ["string", "string", "string"]
    }}

    Rating guidance:
    Use HOLD when valuation is premium and or leverage is high and or free cash flow is declining despite earnings strength.
    Use BUY when growth is strong, cash generation is strong, leverage is manageable, and valuation is not extreme based on provided ratios.
    Use SELL when growth is negative or deteriorating materially and balance sheet risk is high based on provided ratios.

    INPUT_DATA_JSON:
    {json.dumps(payload, default=str, ensure_ascii=False)}
    """

    return textwrap.dedent(prompt).strip()
