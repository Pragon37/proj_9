from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms, models

@login_required
def home(request):
    return render(request, 'review/home.html')

@login_required
def ticket_and_image_upload(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'review/create_ticket.html', context={'ticket_form': ticket_form})


@login_required
def ticket_update(request, id):
    """Retrieve a ticket and its related form and content"""
    ticket = models.Ticket.objects.get(id=id)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('post_detail', ticket.id)
    else:
        form = forms.TicketForm(instance=ticket)
    return render(request, 'review/ticket_update.html', {'form': form})


@login_required
def post_detail(request, id):
    ticket = models.Ticket.objects.get(id=id)
    return render(request, 'review/post_detail.html', {'ticket': ticket}) 


@login_required
def ticket_delete(request, id):
    """Retrieve a ticket and its related form and content"""
    ticket = models.Ticket.objects.get(id=id)
    if request.method == 'POST':
        ticket.delete()
        #Temporary stuff. It does not work if deleting the last ticket
        return redirect('home')
    return render(request, 'review/ticket_delete.html', {'ticket': ticket})

"""
<Form> could not be created because the data didn't validate.
If this happens for an ImageField check for enctype="multipart/form-data"
in the template !!!
"""

@login_required
def create_review(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if any([review_form.is_valid(),ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
    return render(request, 'review/create_review.html', context={'ticket_form': ticket_form, 'review_form': review_form})

@login_required
def review_update(request, id):
    """Retrieve a review and its related form and content"""
    review = models.Review.objects.get(id=id)
    if request.method == 'POST':
        review_form = forms.Review(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect('post_detail', review.id)
    else:
        review_form = forms.ReviewForm(instance=review)
    
    return render(request, 'review/review_update.html', context={'review_form': review_form})

@login_required
def review_delete(request, id):
    """Retrieve a review and its related form and content"""
    review = models.Review.objects.get(id=id)
    if request.method == 'POST':
        review.delete()
        #Temporary stuff. It does not work if deleting the last review
        return redirect('home')
    return render(request, 'review/review_delete.html', {'review': review})

@login_required
def follower_update(request, id):
    pass

