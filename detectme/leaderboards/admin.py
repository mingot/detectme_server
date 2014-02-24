from django.contrib import admin
from .models import Performance, Category, UserScore, Competition, TopImage


admin.site.register(Performance)
admin.site.register(Category)
admin.site.register(UserScore)
admin.site.register(Competition)
admin.site.register(TopImage)
