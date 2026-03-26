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
  - eSewa (Nepal)
  - Khalti (Nepal)
- **Payment Tracking**: Complete payment status management
- **Transaction Records**: Detailed payment history and transaction IDs

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
- **Frontend**: HTML5, CSS3, JavaScript
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
   - Copy `.env copy` to `.env`
   - Configure the following environment variables:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Email Configuration (Optional)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

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
Restro-Site/
├── core/                    # Core Django settings and configuration
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── customer_panel/          # Main customer-facing application
│   ├── models.py           # Teams, Testimonials models
│   ├── views.py            # Main views
│   ├── urls.py             # Customer panel URLs
│   ├── viewsets/           # View classes for different features
│   │   ├── auth.py         # Authentication views
│   │   ├── booking.py      # Table reservation views
│   │   ├── custom_pages.py # Home, About pages
│   │   ├── menu.py         # Menu display views
│   │   ├── order.py        # Order management views
│   │   └── user_profile.py # User profile views
│   └── formsets/           # Form classes
├── menu/                   # Menu management
│   ├── models.py           # MenuCategories, MenuItems
│   └── admin.py            # Menu admin configuration
├── booking/                # Table reservation system
│   ├── models.py           # TimeSlot, Booking models
│   └── admin.py            # Booking admin
├── order/                  # Order management system
│   ├── models.py           # OrderCart, Order, OrderItem models
│   └── admin.py            # Order admin
├── payments/               # Payment processing
│   ├── models.py           # Payment model
│   └── admin.py            # Payment admin
├── user_accounts/          # User account management
│   ├── models.py           # ShippingAddress, OTP models
│   └── admin.py            # User account admin
├── utils/                  # Utility models and functions
│   ├── models.py           # BaseModel, CommonModel
│   └── _utils.py           # Utility functions
├── templates/              # HTML templates
│   ├── authentication/     # Login, register templates
│   └── customer_panel/     # Customer-facing templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User-uploaded media files
├── menu.json              # Sample menu data
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
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

**Built with ❤️ for the restaurant industry**
