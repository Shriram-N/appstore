# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Review, MarketApp,Cluster
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ReviewForm
import datetime
from .suggestions import update_clusters


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review_detail.html', {'review': review})


def marketapp_list(request):
    marketapp_list = MarketApp.objects.order_by('-name')
    context = {'marketapp_list':marketapp_list}
    return render(request, 'marketapp_list.html', context)


def marketapp_detail(request, marketapp_id):
    marketapp = get_object_or_404(MarketApp, pk=marketapp_id)
    form = ReviewForm()
    return render(request, 'marketapp_detail.html', {'marketapp': marketapp,'form': form})# Create your views here.

@login_required
def add_review(request,marketapp_id):
    marketapp = get_object_or_404(MarketApp, pk=marketapp_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        ratings=form.cleaned_data['ratings']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        user_name = request.user.username
        review = Review()
        review.marketapp = marketapp
        review.user_name = user_name
        review.ratings = ratings
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
         # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:marketapp_detail', args=(marketapp.id,)))

    return render(request, 'marketapp_detail.html', {'marketapp': marketapp, 'form': form})

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'user_review_list.html', context)

@login_required
def user_recommendation_list(request):
        # get this user reviews
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('marketapp')
    # from the reviews, get a set of marketapp IDs
    user_reviews_marketapp_ids = set(map(lambda x: x.marketapp.id, user_reviews))
    # then get a marketapp list excluding the previous IDs

    # get request user cluster name (just the first one righ now)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster has been assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name


     # get usernames for other members of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

     # get reviews by those users, excluding marketapps reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(marketapp__id__in=user_reviews_marketapp_ids)
    other_users_reviews_marketapp_ids = set(map(lambda x: x.marketapp.id, other_users_reviews))

     # then get a marketapp list including the previous IDs, order by rating
    marketapp_list = sorted(
        list(MarketApp.objects.filter(id__in=other_users_reviews_marketapp_ids)),
        key=lambda x: x.average_rating,
        reverse=True
    )


    return render(
        request,
        'user_recommendation_list.html',
        {'username': request.user.username,'marketapp_list': marketapp_list})
