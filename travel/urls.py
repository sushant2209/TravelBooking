from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'travel-options', views.TravelOptionViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('', views.travel_list, name='travel_list'),
    path('<int:pk>/', views.travel_detail, name='travel_detail'),
    path('<int:travel_id>/book/', views.booking_create, name='booking_create'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('api/', include(router.urls))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
