from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ParseError, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404

from investment_portfolio.services import get_portfolio_evolution
from investment_portfolio.selectors import get_available_dates
from investment_portfolio.services.etl import load_weights_and_prices

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
            raise Http404("Portfolio not found or no data in date range")
        
        return Response(evolution)
    
class PortfolioDatesApi(APIView):
    def get(self, request, portfolio_id):
        dates = get_available_dates(portfolio_id)
        if not dates['first_date']:
            raise Http404("Portfolio not found")
        return Response(dates)
    
class UploadDataApi(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    class InputSerializer(serializers.Serializer):
        file = serializers.FileField()
    
    def post(self, request):
        # Validate input
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file = serializer.validated_data['file']
        
        # Validate file type
        if not file.name.endswith(('.xlsx', '.xls')):
            raise ParseError(detail='Invalid file format. Please upload an Excel file (.xlsx or .xls)')
        
        try:
            # Delegate all processing to the service
            result = load_weights_and_prices(file)
            
            return Response({
                'message': 'Data uploaded and processed successfully',
                'assets': result['assets'],
                'portfolios': result['portfolios'],
                'prices': result['prices'],
                'holdings': result['holdings'],
                'initial_date': result['initial_date'].isoformat()
            }, status=status.HTTP_201_CREATED)
            
        except DjangoValidationError as e:
            raise ValidationError(detail={'error': str(e)})
        except KeyError as e:
            raise ParseError(detail=f'Missing expected sheet or column: {str(e)}')
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise ValidationError(detail={'error': 'An unexpected error occurred'})