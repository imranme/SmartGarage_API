from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from .models import Service, SellVehicle
from .serializers import (
    ServiceListSerializer,
    ServiceDetailSerializer,
    ServiceCreateUpdateSerializer,
    ServiceCancelSerializer,
    SellVehicleListSerializer,
    SellVehicleCreateSerializer
)


class ServiceListCreateView(ListCreateAPIView):
    """List all services for authenticated user or create a new service"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceCreateUpdateSerializer
        return ServiceListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Service created successfully.',
                    'data': ServiceDetailSerializer(
                        serializer.instance
                    ).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific service"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ServiceCreateUpdateSerializer
        return ServiceDetailSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Service updated successfully.',
                    'data': ServiceDetailSerializer(
                        serializer.instance
                    ).data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': 'Service deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class ServiceCancelView(APIView):
    """Cancel a specific service"""
    permission_classes = [IsAuthenticated]

    def post(self, request, uid):
        try:
            service = Service.objects.get(uid=uid, user=request.user)
        except Service.DoesNotExist:
            return Response(
                {'error': 'Service not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if service.cancelled:
            return Response(
                {'error': 'Service is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ServiceCancelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(service, serializer.validated_data)
            return Response(
                {
                    'message': 'Service cancelled successfully.',
                    'data': ServiceDetailSerializer(service).data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SellVehicleListCreateView(ListCreateAPIView):
    """List user's own sell vehicle requests or create a new one"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SellVehicle.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SellVehicleCreateSerializer
        return SellVehicleListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Sell vehicle request created successfully.',
                    'data': SellVehicleListSerializer(
                        serializer.instance
                    ).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SellVehicleDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve or delete a sell vehicle request"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'

    def get_queryset(self):
        return SellVehicle.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return SellVehicleListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': 'Sell vehicle request deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
