# Restro-Site 🍽️

A comprehensive restaurant management system built with Django, featuring online ordering, table reservations, and customer management.

## 🚀 Features

### 🍔 Menu Management
- **Categorized Menu Items**: Organize dishes by categories (appetizers, mains, desserts, etc.)
- **Special Offers**: Support for special pricing and promotional items
- **Detailed Descriptions**: Rich descriptions and images for menu items
- **Dynamic Filtering**: Filter menu items by category

### 🛒 Online Ordering System
- **Shopping Cart**: Add/remove items with quantity management
- **Order Tracking**: Complete order lifecycle from pending to completed
- **Unique Order IDs**: Auto-generated order IDs in format `ORD-YYYY-NNNN`
- **Order History**: Users can view their complete order history

### 📅 Table Reservation System
- **Time Slot Management**: Configurable time slots for reservations
- **Booking Status**: Track reservation status (pending, confirmed, ended)
- **User Profiles**: Link reservations to customer accounts
- **Party Size**: Support for different group sizes

### 💳 Payment Integration
- **Multiple Payment Methods**: 
  - Cash on Delivery
  - Khalti (Nepal) 
  - eSewa (Nepal)
- **Payment Tracking**: Complete payment status management // UPDATE PENDING
- **Transaction Records**: Detailed payment history and transaction IDs // UPDATE PENDING

### 👥 Customer Management
- **User Registration & Authentication**: Secure user accounts
- **Profile Management**: Customer profiles with order history
- **Shipping Addresses**: Multiple address management for delivery
- **OTP Verification**: Email-based OTP system for security

### 🌟 Customer Engagement
- **Testimonials**: Customer reviews and ratings system
- **Team Showcase**: Display restaurant staff and their roles
- **About Us**: Restaurant information and story

## 🛠️ Tech Stack

- **Backend**: Django 6.0.1
- **Database**: PostgreSQL (configurable)
- **Frontend**: HTML5, CSS3, JavaScript(VERY LESS)
- **Authentication**: Django's built-in auth system
- **File Upload**: Django's ImageField for menu items and team photos
- **Email**: SMTP configuration for notifications

## 📋 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Restro-Site.git
   cd Restro-Site
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   - Copy `.env copy` to `.env` and update the variables

5. **Database Setup**
   ```bash
   # Create database migrations
   python manage.py makemigrations
   
   # Apply migrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load Initial Data** (Optional)
   ```bash
   # Load menu data from menu.json if available
   python manage.py loaddata menu.json
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

9. **Access the Application**
   - Main Site: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 🏗️ Project Structure

```
 Restro-Site
    ├── admin_panel
    │   ├── apps.py
    │   ├── formsets
    │   │   ├── menuitemform.py
    │   │   ├── reviewform.py
    │   │   └── usercreationform.py
    │   ├── __init__.py
    │   ├── urls.py
    │   └── viewsets
    │       ├── admin_dashboard.py
    │       ├── admin_menu.py
    │       ├── admin_order.py
    │       ├── admin_payments.py
    │       ├── admin_reservation.py
    │       ├── admin_reviews.py
    │       └── admin_user.py
    ├── api
    │   ├── __init__.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── viewsets.py
    ├── booking
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   └── tests.py
    ├── core
    │   ├── asgi.py
    │   ├── benchmark_middleware.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── customer_panel
    │   ├── admin.py
    │   ├── formsets
    │   │   ├── bookingform.py
    │   │   ├── orderform.py
    │   │   └── resetpassform.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── urls.py
    │   └── viewsets
    │       ├── booking.py
    │       ├── home.py
    │       ├── __init__.py
    │       ├── menu.py
    │       └── order.py
    ├── docker-compose.yml
    ├── Dockerfile
    ├── manage.py
    ├── media
    │   ├── menu_items
    │   │   ├── Food_Item_2Pcauod.png
    │   │   ├── Food_Item_3E6QGkS.png
    │   │   ├── Food_Item_aa6l09X.png
    │   │   ├── Food_Item_c1aDoZ5.png
    │   │   ├── Food_Item_DUsocid.png
    │   │   ├── Food_Item_HACncVG.png
    │   │   ├── Food_Item_hszht1j.png
    │   │   ├── Food_Item.png
    │   │   ├── Food_Item_SlFJllJ.png
    │   │   ├── Food_Item_V3L3qd0.png
    │   │   └── Food_Item_XFbsaiB.png
    │   └── teams
    │       ├── person_31oAOrj.jpg
    │       ├── person_5eEPb0l.jpg
    │       ├── person.jpg
    │       ├── person_KGh213O.jpg
    │       ├── person_r7wyBnX.jpg
    │       └── person_X8X8Dmu.jpg
    ├── menu
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   └── tests.py
    ├── menu.json
    ├── order
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   └── tests.py
    ├── payments
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── README.md
    ├── requirements.txt
    ├── Restro_backup.sql
    ├── static
    │   ├── admin_panel
    │   │   └── css
    │   │       ├── review.css
    │   │       └── style.css
    │   └── customer_panel
    │       ├── css
    │       │   ├── index.css
    │       │   └── styles.css
    │       └── js
    │           ├── about.js
    │           ├── index.js
    │           ├── menu_item.js
    │           └── menu.js
    ├── templates
    │   ├── admin_panel
    │   │   ├── admin_all_categories.html
    │   │   ├── admin_all_menu.html
    │   │   ├── admin_all_order.html
    │   │   ├── admin_all_payments.html
    │   │   ├── admin_all_reservation.html
    │   │   ├── admin_all_reviews.html
    │   │   ├── admin_all_user.html
    │   │   ├── admin_base.html
    │   │   ├── admin_category_create.html
    │   │   ├── admin_category_edit.html
    │   │   ├── admin_dashboard.html
    │   │   ├── admin_menuitem_create.html
    │   │   ├── admin_menuitem_edit.html
    │   │   ├── admin_payment_edit.html
    │   │   ├── admin_review_create.html
    │   │   ├── admin_review_edit.html
    │   │   ├── admin_user_create.html
    │   │   └── admin_user_edit.html
    │   ├── authentication
    │   │   ├── login.html
    │   │   ├── register.html
    │   │   └── reset_password.html
    │   └── customer_panel
    │       ├── about.html
    │       ├── all_bookings.html
    │       ├── all_orders.html
    │       ├── base.html
    │       ├── booktable.html
    │       ├── cart.html
    │       ├── checkout.html
    │       ├── edit_shipping_address.html
    │       ├── esewa_confirmation.html
    │       ├── index.html
    │       ├── menu.html
    │       ├── menu_item.html
    │       ├── payment_verify.html
    │       └── user_profile.html
    ├── user_accounts
    │   ├── admin.py
    │   ├── apps.py
    │   ├── formsets
    │   │   ├── registerform.py
    │   │   └── shippingaddform.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── viewsets
    │       ├── auth.py
    │       ├── CustomMixin.py
    │       └── user_profile.py
    └── utils
        ├── __init__.py
        ├── models.py
        └── _utils.py
```

## 🔧 Configuration

### Database Configuration
The project uses PostgreSQL by default. Update your `.env` file with your database credentials.

### Email Configuration
Configure SMTP settings in your `.env` file for email notifications (password reset, etc.).

### Static Files
- Static files are served from `/static/`
- User-uploaded media files are stored in `/media/`

## 🎯 Usage

### For Restaurant Staff
1. **Access Admin Panel**: Go to `/admin/` and login with superuser credentials
2. **Manage Menu**: Add/edit menu categories and items
3. **Manage Bookings**: View and manage table reservations
4. **Manage Orders**: Process customer orders
5. **Manage Payments**: Track payment status

### For Customers
1. **Browse Menu**: View restaurant menu by categories
2. **Place Orders**: Add items to cart and checkout
3. **Make Reservations**: Book tables for desired time slots
4. **Track Orders**: View order history and current status
5. **Manage Profile**: Update personal information and addresses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions, please:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Contact the project maintainers

## 🔄 Version History

- **v1.0.0** - Initial release with core features
  - Menu management
  - Online ordering
  - Table reservations
  - Payment integration
  - User management

---

