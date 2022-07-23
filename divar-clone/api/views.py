from decimal import Decimal
from django.shortcuts import render
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status 


@api_view(['GET'])
def pay_for_item(request, price: Decimal):
    print(f'Making transaction for {price} dollars...')
    return Response({'details': 'Paid successfully!'}, status=status.HTTP_200_OK)
    
