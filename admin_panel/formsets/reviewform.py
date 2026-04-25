from django.forms import ModelForm
from customer_panel.models import Reviews

class ReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['first_name', 'last_name', 'review', 'rating']
