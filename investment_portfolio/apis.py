from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from investment_portfolio.services import get_portfolio_evolution
from investment_portfolio.selectors import get_available_dates

class PortfolioEvolutionApi(APIView):
    class InputSerializer(serializers.Serializer):
        start = serializers.DateField()
        end = serializers.DateField()
    
    def get(self, request, portfolio_id):
        # Validate input
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        # Call service (all business logic is there)
        evolution = get_portfolio_evolution(
            portfolio_id=portfolio_id,
            start_date=serializer.validated_data['start'],
            end_date=serializer.validated_data['end']
        )
        
        if not evolution:
            return Response(
                {'error': 'Portfolio not found or no data in date range'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(evolution)
    
class PortfolioDatesApi(APIView):
    def get(self, request, portfolio_id):
        dates = get_available_dates(portfolio_id)
        return Response(dates)