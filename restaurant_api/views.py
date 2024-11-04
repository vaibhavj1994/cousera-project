from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, User

from rest_framework.response import Response
from rest_framework import generics, viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from restaurant.models import Menu, Booking, Cart, Order, OrderItem
from .serializers import MenuSerializer, BookingSerializer, CartSerializer, OrderSerializer, UserSerializer


class IsManagerorAdmin(permissions.BasePermission):
    """
    Custom permission to only allow managers to access certain views.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name='Manager').exists())


class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    ordering_fields = ['price']
    search_fields = ['title']
    filterset_fields = ['price']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Any authenticated user can view menu items
        else:
            return [IsAuthenticated(), IsAdminUser()]  # Only admin can create menu items


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Any authenticated user can view a single menu item
        else:
            return [IsAuthenticated(), IsAdminUser()]  # Only admin can update or delete menu items
        

#Given the similarity of operations for Manager and Delivery Crew groups --> 2 ViewSet classes

class ManagerGroup(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    def list(self, request):
        managers = User.objects.all().filter(groups__name='Manager') # __ for related fields
        users = UserSerializer(managers, many=True)
        return Response(users.data)
    
    def create(self,request):
        username = request.data.get("username")
        if not username: # username not provided
            return Response({"message":"Invalid user"}, status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"message": "Successfully added to Manager Group"}, status.HTTP_201_CREATED)
    
    def destroy(self, request, userId=None):
        user = get_object_or_404(User, id=userId)
        managers = Group.objects.get(name="Manager")
        if user in managers.user_set.all():
            managers.user_set.remove(user)
            return Response({"message": "Successfully removed from Manager Group"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not found in Manager Group"}, status=status.HTTP_404_NOT_FOUND)
        

class DeliveryCrewGroup(viewsets.ViewSet):
    permission_classes = [IsManagerorAdmin] # custom permission to allow only managers and superadmin

    def list(self, request):
        delivery_crew = User.objects.filter(groups__name='Delivery Crew')
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data)

    def create(self, request):
        username = request.data.get("username")
        if not username:
            return Response({"message": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=username)
        delivery_crew = Group.objects.get(name="Delivery Crew")
        delivery_crew.user_set.add(user)
        
        return Response({"message": "Successfully added to Delivery Crew Group"}, status=status.HTTP_201_CREATED)

    def destroy(self, request, userId=None):
        user = get_object_or_404(User, id=userId)
        delivery_crew = Group.objects.get(name="Delivery Crew")
        if user in delivery_crew.user_set.all():
            delivery_crew.user_set.remove(user)
            return Response({"message": "Successfully removed from Delivery Crew Group"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not found in Delivery Crew Group"}, status=status.HTTP_404_NOT_FOUND)
        

class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    # Filter Cart queryset by the authenticated user only.
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.filter(user=self.request.user).delete()
        return Response({"message": "All items removed from cart"})
    

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['total']

    # Filters Order queryset based on user's role
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)
    
    # Override create method to add functionality (creating order items, emptying carts...)
    def create(self, request):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        if cart_items.count() == 0:
            return Response({"message": "No item in cart"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        total = sum(item.price for item in cart_items)
        order = serializer.save(user=user, total=total)

        for item in cart_items:
            OrderItem.objects.create(order=order, menuitem = item.menuitem, quantity=item.quantity, unit_price=item.unit_price, price=item.price)

        cart_items.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self,request, *args, **kwargs):
        order = self.get_object() # method to get the object based on <pk> URL parameter
        user = request.user

        # Allow only if the user is a customer and owns the order
        if user.groups.exists() or order.user != user:
            return Response({"message": "You do not have permission to access this order."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user

        if user.groups.filter(name='Manager').exists():
            delivery_crew_id = request.data.get('delivery_crew')
            if delivery_crew_id:
                order.delivery_crew = get_object_or_404(User, id=delivery_crew_id)
            order_status = request.data.get('status', None)
            if order_status and order_status in ['0','1']:
                order.status = int(order_status)
            elif order_status: #if the status is provided but is invalid
                return Response({"message": "Status can be 0 or 1 only"}, status=status.HTTP_400_BAD_REQUEST)
            
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        
        elif user.groups.filter(name='Delivery Crew').exists() and order.delivery_crew == user:
            order_status = request.data.get('status', None)
            if order_status and order_status in ['0','1']:
                order.status = int(order_status)
            elif order_status:
                return Response({"message": "Status can be 0 or 1 only"}, status=status.HTTP_400_BAD_REQUEST)
            
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        
        return Response({"message": "Not allowed to update this order"}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.groups.filter(name='Manager').exists():
            order.delete()
            return Response({"message": "Order deleted"}, status=status.HTTP_200_OK)
        return Response({"message": "Not allowed to delete this order"}, status=status.HTTP_403_FORBIDDEN)
    
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsManagerorAdmin]
