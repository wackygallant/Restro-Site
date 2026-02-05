def get_username(request):
    if request.user.is_authenticated:
        return request.user.username 
    else:
        return "Guest"