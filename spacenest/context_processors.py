from .models import Mailbox

def inbox(request):
    mails = None
    if request.user.is_authenticated:
        try:
            mails = Mailbox.objects.filter(receiver=request.user)
            return {"mails": mails}
        except Mailbox.DoesNotExist:
            return {"mails": 0}
    return {"mails": mails}
