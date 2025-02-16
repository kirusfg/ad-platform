def notifications_processor(request):
    if request.user.is_authenticated:
        # Get the 5 most recent notifications
        return {"notifications": request.user.notifications.filter(is_read=False).order_by("-created_at")[:5]}
    return {"notifications": []}
