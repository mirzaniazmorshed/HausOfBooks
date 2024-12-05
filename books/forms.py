from . models import CreateBookReview
from django import forms
class CreateBookReviewForm(forms.ModelForm):
    class Meta:
        model = CreateBookReview
        fields = ['body']
    
    def clean_body(self):
        body  = self.cleaned_data.get('body')
        if len(body) < 10:
            raise forms.ValidationError('Your reviews should be at least 10 characters')
        return body
