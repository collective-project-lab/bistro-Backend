from rest_framework.generics import ListAPIView
from .serializers import MenuItemSerializer
from .models import MenuItem

class MenuItemListView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.filter(is_available=True)
    


