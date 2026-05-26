from django.db import models

from investment_portfolio.models.base_model import BaseModel
from investment_portfolio.models.portfolio import Portfolio
from investment_portfolio.models.asset import Asset

class Holding(BaseModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta: # type: ignore
        constraints = [
            models.UniqueConstraint(fields=['portfolio', 'asset', 'date'], name='unique_portfolio_asset_date')
        ]
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name} - {self.date}: {self.quantity}"
    
    def clean(self):
        pass