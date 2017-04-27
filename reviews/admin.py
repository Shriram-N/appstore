# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import MarketApp,Review,Cluster

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display=['marketapp','pub_date','user_name','comment','ratings']
    list_filter = ['pub_date', 'user_name']
    search_fields=['comment']

class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']


admin.site.register(MarketApp)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)
# Register your models here.
