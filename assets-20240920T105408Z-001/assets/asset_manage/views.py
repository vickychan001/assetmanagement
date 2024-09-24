from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
@swagger_auto_schema(
    method='post',
    request_body=ManagerRegSerializer,
    responses={201: 'Successfully registered', 400: 'Bad request'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def manager_signup(request):
    serializer = ManagerRegSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Successfully registered"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=EmployeeRegSerializer,
    responses={201: 'Successfully registered', 400: 'Bad request'}
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def employee_signup(request):
    serializer = EmployeeRegSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Successfully registered"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=AddAssetSerializer,
    responses={201: 'Asset added successfully', 400: 'Bad request'}
)

@api_view(['POST'])

def add_asset(request):
    serializer = AddAssetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Asset added successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: AddAssetSerializer(many=True), 400: 'Bad request'}
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def asset_view(request):
    asset = Assets.objects.all()
    serializer = AddAssetSerializer(asset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    responses={200: EmployeeRegSerializer(many=True), 400: 'Bad request'}
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def employee_view(request):
    employee = CustomUser.objects.filter(is_staff=False, is_superuser=False)
    serializer = EmployeeRegSerializer(employee, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh Token'),
        },
        required=['refresh']
    ),
    responses={200: 'Access token refreshed', 400: 'Invalid Token'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_view(request):
    try:
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        return Response({
            'access': str(token.access_token),
            'refresh': str(token)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh Token'),
        },
        required=['refresh']
    ),
    responses={200: 'User logged out successfully', 400: 'Invalid Token or Token already blacklisted'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        token.blacklist()
        return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "Invalid Token or Token already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: 'Logged in successfully with access and refresh tokens', 400: 'Invalid credentials'}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)},
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def asset_assigned_update(request):
    user_id = request.data.get('id')

    if not user_id:
        return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(CustomUser, id=user_id)
    serializer = AssetAssignedSerializer(user, data=request.data, partial=True)

    # Check if the data is valid
    if serializer.is_valid():
        serializer.save()  # Save the updated asset_assigned field
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


