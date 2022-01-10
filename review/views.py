from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms, models
from authentication.models import User

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
    """
    #First test if it is a create or update.
    UserFollows.objects.filter(user
    """
    message = ''
    if request.method == 'POST':
        if 'add_followee' in request.POST:
            form = forms.UserFollowsForm(request.POST, user=request.user)
            delete_form = forms.DeleteFollowsForm()
            if form.is_valid():
                username=form.cleaned_data['username'],
                user_following = User.objects.get(username=request.user)
                user_followed = User.objects.get(username=username[0])
                new_relation = models.UserFollows()
                new_relation.user = User.objects.get(username=request.user)
                new_relation.followed_user = User.objects.get(username=username[0])
                print("New Relation : ", new_relation)
                if models.UserFollows.objects.filter(user=new_relation.user, 
                                                     followed_user=new_relation.followed_user).exists():
                    message = '{} follows {} already exists'.format(new_relation.user, new_relation.followed_user)
                else:
                    models.UserFollows.save(new_relation)
        if 'delete_followee' in request.POST:
            form = forms.UserFollowsForm(user=request.user)
            delete_form = forms.DeleteFollowsForm(request.POST)
            print("Request: ", request.POST)
            print("Request pk: ", request.POST['pk'])
            print("Request user: ", request.user)
            if delete_form.is_valid():
                deleted_relation = models.UserFollows.objects.get(pk=request.POST['pk'])
                #deleted_relation.user = User.objects.get(username=request.user)
                #deleted_relation.followed_user = User.objects.get(pk=request.POST['pk'])
                print("To be deleted : ", deleted_relation)
                pass
    else:
        form = forms.UserFollowsForm(user=request.user)
        delete_form = forms.DeleteFollowsForm()
    return render(request, 'review/follower_update.html',
                  context={'form': form, 'delete_form': delete_form, 'message': message})



