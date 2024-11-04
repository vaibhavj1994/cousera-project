from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter()
router.register(r'tables', views.BookingViewSet)

urlpatterns = [
    path('menu/', views.MenuItemsView.as_view()),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view()),
    path('cart/menu-items/', views.CartView.as_view(), name='cart'),
    path('orders/<int:pk>/', views.SingleOrderView.as_view(), name='single-order'),
    path('orders/', views.OrderView.as_view(), name='orders'),

    # Manager group URLs
    path('groups/manager/users/', views.ManagerGroup.as_view({'get': 'list', 'post': 'create'}), name='manager-group-users'),
    path('groups/manager/users/<int:userId>/', views.ManagerGroup.as_view({'delete': 'destroy'}), name='manager-group-remove-user'),

    # Delivery crew group URLs
    path('groups/delivery-crew/users/', views.DeliveryCrewGroup.as_view({'get': 'list', 'post': 'create'}), name='delivery-crew-group-users'),
    path('groups/delivery-crew/users/<int:userId>/', views.DeliveryCrewGroup.as_view({'delete': 'destroy'}), name='delivery-crew-group-remove-user'),
    
    path('booking/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
]