from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Dealership
from .serializers import ChatAppSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def dealership_list(request):
    
    ChatApp = Dealership.objects.filter(is_active=True).order_by('dealership_name')
    
    # Filter by city if provided
    city = request.query_params.get('city', None)
    if city:
        ChatApp = ChatApp.filter(city__icontains=city)
    
    # Search by name if provided
    search = request.query_params.get('search', None)
    if search:
        ChatApp = ChatApp.filter(dealership_name__icontains=search)
    
    serializer = ChatAppSerializer(ChatApp, many=True)
    
    return Response({
        'status': 'success',
        'count': ChatApp.count(),
        'data': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def dealership_list(request):
    dealerships = Dealership.objects.filter(is_active=True).order_by('dealership_name')

    # Filter by city
    city = request.query_params.get('city')
    if city:
        dealerships = dealerships.filter(city__icontains=city)

    # Search by name
    search = request.query_params.get('search')
    if search:
        dealerships = dealerships.filter(dealership_name__icontains=search)

    serializer = ChatAppSerializer(dealerships, many=True)

    return Response({
        'status': 'success',
        'count': dealerships.count(),
        'data': serializer.data
    }, status=status.HTTP_200_OK)
