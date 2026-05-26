# investment_portfolio/apis.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from investment_portfolio.services import get_portfolio_evolution

class PortfolioEvolutionApi(APIView):
    class InputSerializer(serializers.Serializer):
        fecha_inicio = serializers.DateField()
        fecha_fin = serializers.DateField()
    
    def get(self, request, portfolio_id):
        # Validate input
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        # Call service (all business logic is there)
        evolution = get_portfolio_evolution(
            portfolio_id=portfolio_id,
            start_date=serializer.validated_data['fecha_inicio'],
            end_date=serializer.validated_data['fecha_fin']
        )
        
        if not evolution:
            return Response(
                {'error': 'Portfolio not found or no data in date range'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(evolution)