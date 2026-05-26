from datetime import date
from typing import Dict, List, Any

from investment_portfolio.selectors import get_holdings_with_assets, get_prices_by_date_range
from investment_portfolio.calculations import calculate_portfolio_value, calculate_weights

def get_portfolio_evolution(
    portfolio_id: int, 
    start_date: date, 
    end_date: date
) -> List[Dict[str, Any]]:
    
    # Fetch data
    holdings = get_holdings_with_assets(portfolio_id)
    if not holdings:
        return []
    
    asset_ids = [h.asset.id for h in holdings]
    prices_by_date = get_prices_by_date_range(asset_ids, start_date, end_date)
    
    # Calculate evolution
    evolution = []
    for current_date in sorted(prices_by_date.keys()):
        daily_prices = prices_by_date[current_date]
        
        # Calculate values per asset
        asset_values = {}
        for holding in holdings:
            price = daily_prices.get(holding.asset.id)
            if price:
                value = float(holding.quantity * price)
                asset_values[holding.asset.name] = value
            else:
                asset_values[holding.asset.name] = 0.0
        
        # Calculate total value and weights
        total_value = round(float(calculate_portfolio_value(holdings, daily_prices)), 2)
        weights = calculate_weights(asset_values, total_value)
        
        evolution.append({
            'date': current_date.isoformat(),
            'total_value': total_value,
            'weights': weights
        })
    
    return evolution