from django.db import models

from investment_portfolio.models.base_model import BaseModel

class Asset(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    def clean(self):
        pass