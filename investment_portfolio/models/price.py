from django.db import models

from investment_portfolio.models.base_model import BaseModel
from investment_portfolio.models.asset import Asset

class Price(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices')
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta: # type: ignore
        constraints = [
            models.UniqueConstraint(fields=['asset', 'date'], name='unique_asset_date')
        ]

    def __str__(self):
        return f"{self.asset.name} - {self.date}: {self.value}"
    
    def clean(self):
        pass