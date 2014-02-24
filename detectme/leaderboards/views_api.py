from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser
from .models import TopImage
from .serializers import PerformanceSerializer,TopImageSerializer


class PerformanceAPICreate(generics.CreateAPIView):
    serializer_class = PerformanceSerializer
    parser_classes = (JSONParser,)
    permission_classes = (IsAdminUser,)

class TopImageAPIList(generics.ListCreateAPIView):
    serializer_class = TopImageSerializer
    model = TopImage
    paginate_by = None

    def pre_save(self, obj):
        #DMmetric('api_annotatedimages_create')
        obj.author = self.request.user.get_profile()

