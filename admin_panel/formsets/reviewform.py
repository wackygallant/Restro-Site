from django.forms import ModelForm
from customer_panel.models import Testimonials

class ReviewForm(ModelForm):
    class Meta:
        model = Testimonials
        fields = ['first_name', 'last_name', 'review', 'rating']
