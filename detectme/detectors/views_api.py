from datetime import datetime
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from redis_metrics import metric

from .models import Detector, Rating, AnnotatedImage
from .serializers import DetectorSerializer, AnnotatedImageSerializer,\
                          RatingSerializer, SupportVectorSerializer,\
                          AbuseReportSerializer, PaginatedDetectorSerializer
# from .views import get_allowed_detectors

NUM_ELEMENTS_IN_PAGE = 12


class DetectorAPIList(generics.ListCreateAPIView):
    serializer_class = DetectorSerializer
    paginate_by = None

    def pre_save(self, obj):
        DMmetric('api_detectors_create')
        obj.author = self.request.user.get_profile()

    def get_queryset(self):
        DMmetric('api_detectors_list')
        q = self.request.QUERY_PARAMS

        if 'search' in q:
            res = Detector.objects.search(q['search'], self.request.user)
        else:
            res = Detector.objects.allowed_detectors(self.request.user)

        if 'featured' in q:
            res = Detector.objects.featured_detectors()

        if 'page' in q:
            self.paginate_by = NUM_ELEMENTS_IN_PAGE

        if 'private' in q:
            res = Detector.objects.self_detectors(self.request.user)



        return res
               


class DetectorAPITimeList(generics.ListAPIView):
    """
    Send list of detectors uploaded later than the time parameter.
    Used for just sending last updates
    """
    serializer_class = DetectorSerializer
    paginate_by = None

    def get_queryset(self):
        uploaded_time = int(self.kwargs['time'])
        uploaded_time = datetime.fromtimestamp(uploaded_time)
        query = Detector.objects.query_allowed_detectors(self.request.user)
        query = query & Q(uploaded_at__gte=uploaded_time)
        return (Detector.objects.filter(query)
                .order_by('-created_at'))
            

class DetectorAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetectorSerializer
    model = Detector
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
                          # IsOwnerOrReadOnly,)
    paginate_by = None
    
    def pre_save(self, obj):
        DMmetric('api_detectors_update')
        # remove all the images and wait for the new ones to be updated
        obj.annotatedimage_set.all().delete()
        obj.author = self.request.user.get_profile()

    def get_queryset(self):
        qs = super(DetectorAPIDetail, self).get_queryset()
        return qs.filter(Detector.objects.query_allowed_detectors(self.request.user))


class AnnotatedImageAPIList(generics.ListCreateAPIView):
    serializer_class = AnnotatedImageSerializer
    model = AnnotatedImage
    paginate_by = None

    def pre_save(self, obj):
        #DMmetric('api_annotatedimages_create')
        obj.author = self.request.user.get_profile()


class AnnotatedImageAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnotatedImageSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          # IsOwnerOrReadOnly,)
    paginate_by = None
    def pre_save(self, obj):
        obj.author = self.request.user.get_profile()


class AnnotatedImagesForDetector(generics.ListAPIView):
    serializer_class = AnnotatedImageSerializer
    paginate_by = None
    def get_queryset(self):
        # Returns list of AnnotatedImage for the requested detector
        detector = self.kwargs['detector']
        return AnnotatedImage.objects.filter(detector=detector)


class SupportVectorsForDetector(generics.RetrieveAPIView):
    serializer_class = SupportVectorSerializer
    model = Detector
    
    def get_queryset(self):
        DMmetric('api_supportvectors_list')
        return super(SupportVectorsForDetector, self).get_queryset()


class RatingAPIList(APIView):
    """
    Store the rating as a new rating only if it is the first
    time this user rates this detector
    """
    def post(self, request, format=None):
        serializer = RatingSerializer(data=request.DATA)
        author = self.request.user.get_profile()

        if serializer.is_valid():

            try:
                previous_rating = Rating.objects.get(author=author,
                                                     detector=serializer.object.detector)
                previous_rating.rating = serializer.object.rating
                previous_rating.save()
            
            except Rating.DoesNotExist:
                serializer.object.author = author
                serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AbuseReportAPICreate(generics.CreateAPIView):
    """
    Store a new abuse report from the mobile device.
    """
    serializer_class = AbuseReportSerializer

    def pre_save(self, obj):
        obj.author = self.request.user.get_profile()
        obj.abuse_type ='OT'


def DMmetric(name):
    if settings.PRODUCTION:
        metric(name)



