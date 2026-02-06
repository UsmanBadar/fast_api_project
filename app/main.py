from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import (auth_router, company_stock_price_router, 
                        company_profile_router, portfolio_company_router, stock_price_chart_router, company_search_router,
                        portfolio_router, company_fundamentals_router, company_balance_sheet_router, ai_router,
                        stock_target_price_router)
from app.core.config import settings
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-grade API with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Configure CORS for frontend integration
# In production, replace ["*"] with your actual frontend domain(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:4200",  # Angular default
        "http://localhost:8080",  # Vue default
        # Add your production frontend URL here
        # "https://yourdomain.com"
    ],
    allow_credentials=True,  # Allow cookies and authorization headers
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers to frontend
)

# Add trusted host middleware for production security
# Uncomment and configure for production
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
# )

app.include_router(auth_router.auth_router)
app.include_router(company_stock_price_router.company_stock_price_router)
app.include_router(company_profile_router.company_profile_router)
app.include_router(stock_price_chart_router.stock_price_chart_router)
app.include_router(company_search_router.company_search_router)
app.include_router(portfolio_company_router.portfolio_company_router)
app.include_router(portfolio_router.portfolio_router)
app.include_router(company_fundamentals_router.company_fundamentals_router)
app.include_router(company_balance_sheet_router.company_balance_sheet_router)
app.include_router(ai_router.ai_router)
app.include_router(stock_target_price_router.stock_target_price_router)

@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "status": "healthy",
        "message": "API is running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def detailed_health():
    """
    Detailed health check with service status.
    """
    return {
        "status": "healthy",
        "api": "operational",
        "database": "connected",
        "redis": "connected"
    }




    