from datetime import datetime
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_delete, post_save
from detectors.models import Detector
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=50)

    @property
    def num_teams(self):
        return (Performance.objects.filter(category=self)
                .values('detector_author').distinct().count())
        
    @property
    def num_entries(self):
        return Performance.objects.filter(category=self).count()

    def __unicode__(self):
        return u'%s' % self.name


class Competition(models.Model):
    start_date = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)

    @property
    def days_to_go(self):
        days = 0
        if self.finish_date:
            dt = self.finish_date - datetime.now()
            days = dt.days
        return days


class Performance(models.Model):
    """
    Stores performance metrics for the detector.
    Calculated outside with a test set.
    """
    created_at = models.DateTimeField(auto_now=True)
    average_precision = models.FloatField()
    precision = models.TextField(blank=True, null=True)
    recall = models.TextField(blank=True, null=True)
    test_set = models.TextField(blank=True, null=True)
    detector = models.ForeignKey(Detector)
    detector_author = models.ForeignKey('accounts.DetectMeProfile',
                                        null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)

    def save(self, *args, **kwargs):
        # creates the UserScore entry and save category and detector_author
        name = self.detector.name
        try:
            category = Category.objects.get(name=name.split("_")[0])
        except Category.DoesNotExist:
            category = Category.objects.get(name="NA")
        self.category = category
        self.detector_author = self.detector.author
        user_score = UserScore.objects.get_or_create(user=self.detector.author,
                                                     category=category)
        super(Performance, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Performance of %s - %s by %s is %s' % (self.detector.name,
                                                        self.detector.pk,
                                                        self.detector.author.username,
                                                        self.average_precision)


class UserScore(models.Model):
    """
    Summarizes participants of the competition results
    """
    user = models.ForeignKey('accounts.DetectMeProfile')
    category = models.ForeignKey(Category)

    @property
    def best_performance(self):
        return (Performance.objects
                .filter(detector_author=self.user, category=self.category)
                .order_by('-average_precision'))[0]

    @property
    def num_entries(self):
        perf = (Performance.objects
                .filter(detector_author=self.user, category=self.category)
                .count())
        return perf



    def __unicode__(self):
        return u'%s: %s entries with max_score %s' % (self.user.username,
                                                      self.num_entries,
                                                      self.best_performance)

class TopImage(models.Model):
    created_at = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    image_jpeg = models.ImageField(upload_to='top_images/',
                                   default='average_image/default.jpg')
    image_height = models.PositiveSmallIntegerField(editable=False, blank=True)
    image_width = models.PositiveSmallIntegerField(editable=False, blank=True)
    box_x = models.FloatField()
    box_y = models.FloatField()
    box_height = models.FloatField()
    box_width = models.FloatField()
    detector = models.ForeignKey(Detector)

    def save(self, *args, **kwargs):
        self.image_width = self.image_jpeg.width
        self.image_height = self.image_jpeg.height
        super(TopImage, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.image_jpeg.name


@receiver(post_delete, sender=TopImage)
def topImage_post_delete_handler(sender, **kwargs):
    """
    Delete associated images when deleting a detector
    """
    topImage = kwargs['instance']
    storage, path = (topImage.image_jpeg.storage,
                     topImage.image_jpeg.path)
    storage.delete(path)

