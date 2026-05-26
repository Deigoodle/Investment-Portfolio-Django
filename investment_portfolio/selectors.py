# investment_portfolio/selectors.py
from datetime import date
from typing import Dict, List, Any
from decimal import Decimal

from investment_portfolio.models import Portfolio, Holding, Price

def get_holdings_with_assets(portfolio_id: int) -> List[Holding]:
    """
    Returns holdings with its assets by portfolio_id
    """
    return list(Holding.objects.filter(
        portfolio_id=portfolio_id
    ).select_related('asset'))

def get_prices_by_date_range(
    asset_ids: List[int], 
    start_date: date, 
    end_date: date
) -> Dict[date, Dict[int, Decimal]]:
    """
    Get Prices between 2 dates for a list of assets
    
    Returns:
        {
            date1: {asset_id1: price, asset_id2: price, ...},
            date2: {...},
        }
    """
    prices = Price.objects.filter(
        asset_id__in=asset_ids,
        date__range=[start_date, end_date]
    ).select_related('asset').order_by('date')
    
    result = {}
    for price in prices:
        if price.date not in result:
            result[price.date] = {}
        result[price.date][price.asset.id] = price.value
    
    return result

def get_available_dates(portfolio_id: int) -> Dict[str, Any]:
    """
    Get the available dates for a portfolio_id
    """
    holdings = Holding.objects.filter(portfolio_id=portfolio_id)
    asset_ids = [h.asset.id for h in holdings]
    
    dates = Price.objects.filter(
        asset_id__in=asset_ids
    ).values_list('date', flat=True).distinct().order_by('date')
    
    first_date = dates.first()
    last_date = dates.last()
    
    return {
        'first_date': first_date.isoformat() if first_date else None,
        'last_date': last_date.isoformat() if last_date else None,
        'total_dates': dates.count()
    }