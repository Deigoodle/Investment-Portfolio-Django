from django.urls import path
from investment_portfolio.apis import PortfolioEvolutionApi
from investment_portfolio.apis import PortfolioDatesApi

urlpatterns = [
    path('portfolios/<int:portfolio_id>/evolution/', PortfolioEvolutionApi.as_view(), name='portfolio-evolution'),
    path('portfolios/<int:portfolio_id>/dates/', PortfolioDatesApi.as_view(), name='portfolio-dates'),
]