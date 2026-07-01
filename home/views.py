from django.shortcuts import render


# Create your views here.
def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def privacy_policy(request):
    """ A view to return the privacy policy page """
    
    return render(request, 'home/privacy_policy.html')

def terms_and_conditions(request):
    """ A view to return the terms and conditions page """
    
    return render(request, 'home/terms_and_conditions.html')

def returns_and_refunds(request):
    """ A view to return the retuns and refunds page """
    
    return render(request, 'home/returns_and_refunds.html')

def shipping_policy(request):
    """ A view to return the shipping policy page """
    
    return render(request, 'home/shipping_policy.html')
