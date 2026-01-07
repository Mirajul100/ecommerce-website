from django import forms
from .models import ReviewProduct

class ReviewForm (forms.ModelForm):
    class Meta:
        model = ReviewProduct
        fields = ['subject' , 'review' , 'rating']