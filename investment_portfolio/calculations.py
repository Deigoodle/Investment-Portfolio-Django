from decimal import Decimal
from typing import Dict, List

from investment_portfolio.models import Holding, Price

def calculate_portfolio_value(holdings: List[Holding], prices: Dict[int, Decimal]) -> Decimal:
    """
    Calculate V_t = Σ c_i,0 * p_i,t
    """
    total = Decimal('0')
    for holding in holdings:
        price = prices.get(holding.asset.id)
        if price:
            total += holding.quantity * price
    return total

def calculate_weights(asset_values: Dict[str, float], total_value: float) -> Dict[str, float]:
    """
    Calculate w_i,t = x_i,t / V_t
    """
    if total_value == 0:
        return {asset: 0 for asset in asset_values}
    return {asset: value / total_value for asset, value in asset_values.items()}