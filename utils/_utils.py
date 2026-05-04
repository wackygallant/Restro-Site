import random

import matplotlib
matplotlib.use('Agg')  # important for server environments

import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from order.models import Order

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


def generate_revenue_chart():
    today = now().date()
    dates = []
    revenues = []
    for i in range(14, -1, -1):
        day = today - timedelta(days=i)

        revenue = Order.objects.filter(
            order_status='completed',
            created_at__date=day
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        dates.append(day.strftime("%d %b"))
        revenues.append(float(revenue))

    plt.figure(figsize=(10, 4))
    plt.plot(dates, revenues, marker='o')
    plt.title("Revenue - Last 15 Days")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)

    plt.subplots_adjust(left=0.06, right=0.98, top=0.90, bottom=0.20)

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close()

    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')