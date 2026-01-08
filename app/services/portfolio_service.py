from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.portfolio_company_model import PortfolioCompanyModel
from app.schemas.portfolio_company_schema import PortfolioCompanySchema
from app.schemas.portfolio_schema import PorfolioCompanyWithSharePriceSchema
from app.services.company_latest_stock_price_service import get_latest_company_stock_price_service



async def add_portfolio_company_service(username: str, company: PortfolioCompanySchema, db: AsyncSession):
    try:
        check_db_query = await db.execute(select(PortfolioCompanyModel).where(
            PortfolioCompanyModel.user_name == username,
            PortfolioCompanyModel.symbol == company.symbol
        ))
        existing_company = check_db_query.scalars().first()
        if existing_company:
            return existing_company
        new_company = PortfolioCompanyModel(
            user_name=username,
            symbol=company.symbol,
            company_name=company.company_name,
            shares_owned=company.shares_owned,
            average_purchase_price=company.average_purchase_price,
            total_investment=company.total_investment,
            current_price=company.current_price,
            total_value=company.total_value,
            profit_loss=company.profit_loss,
            profit_loss_percentage=company.profit_loss_percentage,
            currency=company.currency
        )
        db.add(new_company)
        await db.commit()
        await db.refresh(new_company)
        return new_company
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database operation failed: {e}")
    


async def remove_portfolio_company_service(username: str, company_symbol: str, db: AsyncSession):
    try:
        query = await db.execute(select(PortfolioCompanyModel).where(
            PortfolioCompanyModel.user_name == username,
            PortfolioCompanyModel.symbol == company_symbol
        ))
        company = query.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found in portfolio")
        await db.delete(company)
        await db.commit()
        return {"detail": "Company removed from portfolio"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove company from portfolio: {e}")
    





async def get_portfolio_companies_with_share_price_service(username: str, db: AsyncSession):
    try:
        query = await db.execute(select(PortfolioCompanyModel).where(
            PortfolioCompanyModel.user_name == username
        ))
        companies = query.scalars().all()
        result = []
        for company in companies:
            latest_price_data = await get_latest_company_stock_price_service(company.symbol)
            company_dict = {
                'id': company.id,
                'user_name': company.user_name,
                'symbol': company.symbol,
                'company_name': company.company_name,
                'shares_owned': company.shares_owned,
                'average_purchase_price': company.average_purchase_price,
                'total_investment': company.total_investment,
                'current_price': company.current_price,
                'total_value': company.total_value,
                'profit_loss': company.profit_loss,
                'profit_loss_percentage': company.profit_loss_percentage,
                'currency': company.currency
            }
            company_dict['latest_share_price'] = latest_price_data[0]['price']
            result.append(PorfolioCompanyWithSharePriceSchema(**company_dict))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve portfolio companies: {e}")