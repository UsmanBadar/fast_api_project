import json
from fastapi.responses import JSONResponse
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.services.company_fundamentals_service import get_or_fetch_company_fundamentals
from app.services.company_profile_service import fetch_company_profile
from app.services.company_balance_sheet_service import fetch_company_balance_sheet
from app.services.ai_service.ai_prompt import generate_prompt




async def run_ai_service(symbol: str, db: AsyncSession) -> dict:
    fundamentals = await get_or_fetch_company_fundamentals(symbol, db)
    profile = await fetch_company_profile(symbol)
    balance_sheet = await fetch_company_balance_sheet(symbol)

    anthropic_client = ChatAnthropic(api_key=settings.CLAUDE_API_KEY,
                                      model="claude-opus-4-20250514", temperature=0.7,
                                      max_tokens=1000, top_p=1, stop=None)

    prompt = generate_prompt(profile.model_dump(), fundamentals, balance_sheet.model_dump())

    response = anthropic_client.invoke(
        input = [prompt]
    )

    llm_text = response.content.strip()
    if llm_text.startswith('"') and llm_text.endswith('"'):
        llm_text = json.loads(llm_text)  # converts the quoted JSON string into real JSON text
    data = json.loads(llm_text)
    return JSONResponse(content=data)
