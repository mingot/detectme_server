from rest_framework import serializers
from .models import Performance, TopImage


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('detector', 'average_precision', 'precision',
                  'recall', 'test_set')

class TopImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopImage
        fields = ('id', 'image_jpeg',
                  'image_height', 'image_width',
                  'box_x', 'box_y',
                  'box_width', 'box_height',
                  'detector')
        read_only = ('uploaded_at', 'image_height', 'image_width')

