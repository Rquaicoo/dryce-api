
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
import random
from django.contrib.auth.models import User
#import send_mail
from django.core.mail import send_mail
from vendor.models import Vendor


def sendEmail(subject, message, from_email, recipient):
    try:
        send_mail(subject, message, from_email, recipient)
        return True
    except Exception as e:
        print(e)
        return False

# Create your views here.

class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classses = [AllowAny]

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)

        
        serializer.is_valid(raise_exception=True)
        #check if email exists
        if User.objects.filter(email=serializer.validated_data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        #check if username exists
        elif User.objects.filter(username=serializer.validated_data['username']).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.validated_data)

            #generate user token
            token = Token.objects.create(user=serializer.instance)
            token = token.key

            #generate otp
            otp = ''.join(str(random.randint(0,9)) for i in range(4))
            
            user = User.objects.get(username=serializer.validated_data['username'])
            RegularUser.objects.create(
                user = user,
                otp = otp,
            )

            #send otp to user
            send_mail('OTP', 'Your OTP is ' + otp, 'dryce.com', [serializer.validated_data['email']], fail_silently=True)


            token_data = {"token": token}
            return Response(
                {**serializer.validated_data, **token_data},
                status = status.HTTP_201_CREATED,
                headers=headers
            )


class LogoutUserAPIView(APIView):
    
    def get(self, request,):
        if request.user.is_authenticated:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response(status=status.HTTP_200_OK)
    
    def post(self, request):
        #delete the token
        data = dict(request.data)["token"]
        token = Token.objects.get(key=data)
        token.delete()
        return Response(status=status.HTTP_200_OK)

class ContactAPIView(APIView):
    def get(self,request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class VerifyUserAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            data = dict(request.data)
            user = request.user
            regular_user = RegularUser.objects.get(user=user)
            if regular_user.otp == data['otp']:
                regular_user.verified = True
                regular_user.save()
                return Response({"message":"succcessful"},status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ValidEmailAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        data = dict(request.data)
        if User.objects.filter(email=data['email']).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)

class ValidUsernameAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = dict(request.data)
        emails = User.objects.filter(username=data['username'])
        if User.objects.filter(username=data['username']).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)

    
class OTPAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
            data = dict(request.data)
            try:
                user = User.objects.get(email=data['email'])
                user = RegularUser.objects.get(user=user)
                otp = ''.join(str(random.randint(0,9)) for i in range(4))
                user.otp = otp
                user.save()
                send_mail('OTP', 'Your OTP is ' + otp, 'dryce.com', [data['email']], fail_silently=True)
                return Response({"message": "OTP sent."},status=status.HTTP_200_OK)
            except:
                return Response({"error":"Your email does not exist"},status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = dict(request.data)
        user = User.objects.get(email=data['email'])
        user = RegularUser.objects.get(user=user)
        if data['otp'] == user.otp:
            user.set_password(data['password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "data is incorrect"},status=status.HTTP_400_BAD_REQUEST)


class SearchRegulerUserAPIView(APIView):
    def post(self, request):
        data = dict(request.data)
        user = User.objects.get(username__icontains=data['username'])
        serializer = SearchRegularUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            regular_user = RegularUser.objects.get(user=user)
            user_serializer = ProfileSerializer(user)
            regular_user_serializer = RegularUserSerializer(regular_user)
            return Response({"user": user_serializer.data, "regular_user": regular_user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            data = dict(request.data)
            user = request.user
            user = RegularUser.objects.get(user=user)
            user.name = data['name']
            user.address = data['address']
            user.phone = data['phone']
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CartAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = RegularUser.objects.get(user=request.user)
            cart = Cart.objects.get(user=user, status="pending")
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user

            #check if cart with status pending exists
            if Cart.objects.filter(user=user, status="pending").exists():
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                data = dict(request.data)
                shirts = int(data["shirt"])
                jeans = int(data["jeans"])
                cardigans = int(data["cardigan"])
                trousers = int(data["trouser"])
                dress = int(data["dress"])
                blouses = int(data["blouses"])

                #create id for cart
                id = ''.join(str(random.randint(0,9)) for i in range(10))
                cost = (shirts * 30) + (jeans * 30) * (cardigans * 30) * (trousers * 30) * (dress * 30) * (blouses * 30)
                Cart.objects.create(user=user, shirts=shirts, jeans=jeans, cardigans=cardigans, trousers=trousers, dress=dress, blouses=blouses, cost=cost, identifier=id, status="pending")
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if request.user.is_authenticated:
            user = request.user
            data = dict(request.data)
            cart = Cart.objects.get(user=user, status="pending")
            cart.shirts = int(data["shirt"])
            cart.jeans = int(data["jeans"])
            cart.cardigans = int(data["cardigan"])
            cart.trousers = int(data["trouser"])
            cart.dress = int(data["dress"])
            cart.blouses = int(data["blouses"])
            cart.cost = (cart.shirts * 30) + (cart.jeans * 30) * (cart.cardigans * 30) * (cart.trousers * 30) * (cart.dress * 30) * (cart.blouses * 30)
            cart.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.user.is_authenticated:
            user = request.user
            cart=Cart.objects.filter(user=user, status="pending")
            cart.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class OrderAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            user = RegularUser.objects.get(user=user)
            order = Order.objects.filter(user=user)
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            user = RegularUser.objects.get(user=user)
            data = dict(request.data)
            cart = data["cart"]
            payment_method = data["payment_method"]
            delivery = data["delivery"]
            
            try:
                Order.objects.create(user=user, cart=cart, payment_method=payment_method, delivery=delivery)
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class RatingAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            data = dict(request.data)
            vendor = Vendor.objects.get(id=data['vendor_id'])
            rating = int(data["rating"])
            vendor.rating = rating
            vendor.rating_count += 1
            vendor.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
  