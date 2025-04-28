from .models import Room

def rooms_context(request):
    return {
        'rooms': Room.objects.all()
}