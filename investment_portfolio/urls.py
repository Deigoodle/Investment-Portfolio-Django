# investment_portfolio/urls.py
from django.urls import path
from investment_portfolio.apis import PortfolioEvolutionApi

urlpatterns = [
    path('portfolios/<int:portfolio_id>/evolution/', PortfolioEvolutionApi.as_view(), name='portfolio-evolution'),
]