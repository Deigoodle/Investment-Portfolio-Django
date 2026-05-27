from django.urls import path
from investment_portfolio.apis import (PortfolioEvolutionApi, 
                                       PortfolioDatesApi, 
                                       UploadDataApi
)

urlpatterns = [
    path('portfolios/<int:portfolio_id>/evolution/', PortfolioEvolutionApi.as_view(), name='portfolio-evolution'),
    path('portfolios/<int:portfolio_id>/dates/', PortfolioDatesApi.as_view(), name='portfolio-dates'),
    path('upload/', UploadDataApi.as_view(), name='upload-data'),
]