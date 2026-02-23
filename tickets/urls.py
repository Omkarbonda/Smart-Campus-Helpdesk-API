from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet

router = DefaultRouter()
router.register(r'', TicketViewSet) # This will create routes at /tickets/ because it is included with prefix 'tickets/' in root urls

urlpatterns = [
    path('', include(router.urls)),
]
