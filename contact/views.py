from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import ContactMessage
from .forms import ContactForm


# Create your views here.
def contact(request):
    """ A view to return the contact page """

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_message = form.save()

            try:
                contact_message.full_clean()
                contact_message.save() 
                # Send email to site owner
                send_mail(
                    contact_message.subject,
                    contact_message.message,
                    contact_message.email,
                    ['craftshack595@gmail.com'],  # Replace with your email address
                )
                messages.success(
                    request,
                    'Your message has been sent successfully!')
                return redirect('home')
            except:
                messages.error(
                    request,
                    'There was an error sending your message. Please try again.')

    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})
