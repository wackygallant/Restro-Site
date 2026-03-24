import random

def get_username(request):
    if request.user.is_authenticated:
        return request.user.username 
    else:
        return "Guest"
    
def order_number_generator(prefix, number):
        return f"{prefix}-{str(number).zfill(6)}"

def generate_otp():
    return str(random.randint(100000, 999999))
