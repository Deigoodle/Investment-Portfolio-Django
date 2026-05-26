# investment_portfolio/services.py
import pandas as pd
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError

from investment_portfolio.models import Asset, Portfolio, Price, Holding

V0 = Decimal('1000000000')

@transaction.atomic
def load_weights_and_prices(file_path: str):
    """
    Carga los datos del Excel a la base de datos.
    """
    # Read Sheets
    weights_df = pd.read_excel(file_path, sheet_name='weights')
    prices_df = pd.read_excel(file_path, sheet_name='Precios')
    
    # Add Assets
    asset_names = weights_df['activos'].to_list()
    assets = {}
    print(f"Adding Assets")
    for name in asset_names:
        asset, created = Asset.objects.get_or_create(name=name)
        assets[name] = asset
        print(f'Asset: "{name}" - {'Created' if created else 'Already exists'}')

    # Verify that every asset has price data
    price_columns = [col for col in prices_df.columns if col != 'Dates']
    missing_in_prices = set(asset_names) - set(price_columns)
    if missing_in_prices:
        raise ValidationError(f"Assets with no data: {missing_in_prices}")
    
    # Add Portfolios
    portfolio_columns = [col for col in weights_df.columns if col not in ['Fecha', 'activos']]
    portfolios = {}
    print(f"Adding Portfolios")
    for col in portfolio_columns:
        portfolio, created = Portfolio.objects.get_or_create(name=col)
        portfolios[col] = portfolio
        print(f"Portfolio: {col} - {'Created' if created else 'Already exists'}")

    # Read Weights to calculate Holdings
    initial_weights = {portfolio_name: {} for portfolio_name in portfolios.keys()}
    for _, row in weights_df.iterrows():
        asset_name = row['activos']
        for portfolio_name in portfolios.keys():
            weight = Decimal(str(row[portfolio_name])) # Use decimal to reduce float error
            initial_weights[portfolio_name][asset_name] = weight
    
    # Add Prices
    print(f"Adding Prices")
    for _, row in prices_df.iterrows():
        date = pd.to_datetime(row['Dates']).date()
        for asset_name, asset in assets.items():
            value = row[asset_name]
            if pd.notna(value):
                Price.objects.update_or_create(
                    asset=asset,
                    date=date,
                    defaults={'value': Decimal(str(value))}
                )
        print(f"Prices added for date: {date}")

    # Calculate Holdings
    initial_date = pd.to_datetime(prices_df['Dates'].iloc[0]).date()
    print(f"Calculating Holdings with date: {initial_date}")

    for portfolio_name, portfolio in portfolios.items():
        weights = initial_weights[portfolio_name]
        
        for asset_name, weight in weights.items():
            asset = assets[asset_name]
            initial_price = Price.objects.get(asset=asset, date=initial_date)
            
            amount = weight * V0
            quantity = amount / initial_price.value
            
            Holding.objects.update_or_create(
                portfolio=portfolio,
                asset=asset,
                date=initial_date,
                defaults={'quantity': quantity}
            )
            print(f"Holding: {portfolio_name} - {asset_name}: {quantity}")
    
    return {
        'assets': len(assets),
        'portfolios': len(portfolios),
        'prices': Price.objects.count(),
        'holdings': Holding.objects.count(),
        'initial_date': initial_date,
    }