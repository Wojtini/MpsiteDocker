from django import forms
from django.forms import HiddenInput

from .models import Movie, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'name',
            'category',
            'link',
            'duration',
            'whoAdded',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['whoAdded'].disabled = True
        # self.fields['whoAdded'].widget = HiddenInput()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'user',
            'movie',
            'rating',
            'comment',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].disabled = True
        self.fields['movie'].disabled = True
        self.fields['user'].widget = HiddenInput()
        self.fields['movie'].widget = HiddenInput()

