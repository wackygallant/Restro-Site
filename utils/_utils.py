import random
from django.core.mail import send_mail
from django.conf import settings

def get_username(request):
    if request.user.is_authenticated:
        return request.user.username 
    else:
        return "Guest"
    
def order_number_generator(prefix, number):
        return f"{prefix}-{str(number).zfill(6)}"

def booking_id_generator(prefix, number):
        return f"{prefix}-{str(number).zfill(6)}"

def generate_otp():
    return str(random.randint(100000, 999999))
