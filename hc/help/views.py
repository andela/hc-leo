from django.shortcuts import render
from hc.help.models import Faq

def faq(request):
    faqs = Faq.objects.all()

    ctx = {
        "page": "faq",
        "faqs": faqs
    }
    return render(request, "help/faq.html", ctx)
