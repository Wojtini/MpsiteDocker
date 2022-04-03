from django.contrib import auth
from django.contrib.auth import models
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .\
    models import Movie, Review
from django.contrib.auth.models import User
from .forms import MovieForm, ReviewForm

@login_required
@permission_required('movierating.view_movie', raise_exception=True)
def index(request):
    group = models.Group.objects.get(name="MovieRepo")
    all_users = group.user_set.all()
    # all_users = User.objects.values()
    all_movies = Movie.objects.values()

    for movie in all_movies:
        movie['reviews'] = []
        general_rating = 0
        reviews_count = 0

        for user in all_users:
            # zawsze zwraca jedno...
            all_reviews = Review.objects.select_related().filter(movie=movie['name'], user=user.id)
            if len(all_reviews) == 0:
                movie['reviews'].append('brak')
            else:
                review = all_reviews[0]
                reviews_count += 1
                general_rating += review.rating
                movie['reviews'].append(review)

        if reviews_count == 0:
            movie['number_of_watches'] = 0
        else:
            movie['number_of_watches'] = reviews_count
            general_rating = general_rating // reviews_count

        movie['general_rating'] = general_rating

    all_movies = sorted(list(all_movies), key=lambda d: d['general_rating'], reverse=True)

    return render(request, "moviespreadsheet.html",
                  context={
                    'movies_list': all_movies,
                    'users_list': all_users,
                    'rangetest': [1],
                  })


@login_required
@permission_required('movierating.add_movie', raise_exception=True)
def addmovierequest(request):
    form = MovieForm(request.POST or None, initial={"whoAdded": request.user})
    if form.is_valid():
        form.save()
        return redirect("/movierating")

    return render(request, "addmovie.html",
                  context={
                      'form': form,
                  })


@login_required
@permission_required('movierating.add_review', raise_exception=True)
def addreviewrequest(request, moviename):
    form = None
    try:
        instance = get_object_or_404(Review, user=request.user, movie=moviename)
        form = ReviewForm(request.POST or None, instance=instance)
    except Exception:
        form = ReviewForm(request.POST or None, initial={"user": request.user, "movie": moviename})

    if form.is_valid():
        form.save()
        return redirect("/movierating")

    return render(request, "addreview.html",
                  context={
                      'form': form,
                      'movie_name': moviename,
                  })


@login_required
@permission_required('movierating.add_review', raise_exception=True)
def reviewmanager(request):
    pass
