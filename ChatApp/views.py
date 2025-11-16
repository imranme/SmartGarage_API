"""
Dealerships views for J4NEXT API
"""

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
def dealership_detail(request, pk):
    dealership = get_object_or_404(Dealership, pk=pk, is_active=True)
    serializer = ChatAppSerializer(dealership)
    
    return Response({
        'status': 'success',
        'data': serializer.data
    }, status=status.HTTP_200_OK)