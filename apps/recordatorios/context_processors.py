
from .models import Recordatorio

def unread_notifications(request):
    """
    Context processor para obtener el número de notificaciones no leídas.
    """
    if request.user.is_authenticated and not request.user.is_staff:
        count = Recordatorio.objects.filter(usuario=request.user, leido=False).count()
        return {'unread_notification_count': count}
    return {'unread_notification_count': 0}
