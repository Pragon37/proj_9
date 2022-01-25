from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import CharField, Q, Value
from django.http import HttpResponseRedirect

from . import forms, models
from authentication.models import User

from itertools import chain

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
def follower_update(request):
    """
    Either a form submission to add a followee, or a delete action to remove a followee
    """
    my_followers = []
    all_users = User.objects.exclude(username=request.user).exclude(username='Pi')
    my_followers = all_users.filter(following__followed_user=request.user)
    #for everyuser in all_users:
    #    if everyuser.following.filter(followed_user=request.user):
    #        my_followers.append(everyuser)
    #        print(request.user, " is followed by : ", everyuser)
    print(my_followers)
    print("FOLLOWING : ", request.user.following.all())
    print("FOLLOWED_BY : ", request.user.followed_by.all())
    #all_followers = models.UserFollows.objects.filter(followed_user=request.user)
    all_followers = all_users.filter(following__followed_user=request.user)
    print("ALL_FOLLOWERS = ", all_followers)
         
#       print("EVERYUSER :", everyuser, everyuser.following.filter(followed_user=request.user))
#       for flw in everyuser.following.all():
#           print("FLW: ", flw, request.user)
#           print("FOUND : ", flw is request.user)
        
    message = ''
    if request.method == 'POST':
        if 'add_followee' in request.POST:
            form = forms.UserFollowsForm(request.POST, user=request.user)
            delete_form = forms.DeleteFollowsForm()
            if form.is_valid():
                username=form.cleaned_data['username'],
                new_relation = models.UserFollows()
                new_relation.user = User.objects.get(username=request.user)
                new_relation.followed_user = User.objects.get(username=username[0])
                #Check if the relation already exists
                if models.UserFollows.objects.filter(user=new_relation.user, 
                                                     followed_user=new_relation.followed_user).exists():
                    message = '{} follows {} already exists!'.format(new_relation.user, new_relation.followed_user)
                else:
                    models.UserFollows.save(new_relation)
        if 'delete_followee' in request.POST:
            form = forms.UserFollowsForm(user=request.user)
            delete_form = forms.DeleteFollowsForm(request.POST)
            if delete_form.is_valid():
                deleted_relation = models.UserFollows.objects.get(pk=request.POST['pk'])
                deleted_relation.delete()
    else:
        form = forms.UserFollowsForm(user=request.user)
        delete_form = forms.DeleteFollowsForm()
    return render(request, 'review/follower_update.html',
                  context={'form': form, 'delete_form': delete_form, 'message': message, 'my_followers': my_followers})


@login_required
def post_update(request):
    #gather my most recent tickets, then gather my reviews of this tickets, 
    #then my most recent reviews of the tickets from another user
    """Retrieve a tickets and its related form and content"""
    print("Request: ", request.user)
    tickets = models.Ticket.objects.filter(user__username=request.user).order_by('-time_created')
    print("Ticket: ", tickets)
    reviews = models.Review.objects.filter(user__username=request.user).order_by('-time_created')
    print("Review: ", reviews)
    #print("Review PK: ", reviews[0].pk)
    #print("Review Ticket: ", reviews[0].ticket)
    #print("Review Ticket Title: ", reviews[0].ticket.title)
    #print("Review Ticket User: ", reviews[0].ticket.user)
    return render(request, 'review/post_update.html', context={'reviews': reviews, 'tickets': tickets})

@login_required
def feed(request):
    followee = request.user.following.values_list('followed_user', flat=True)

    all_tickets = models.Ticket.objects.filter(Q(user=request.user) | Q(user__in=followee)) 
    all_tickets = all_tickets.annotate(content_type=Value('TICKET', CharField()))

    all_reviews = models.Review.objects.filter(Q(user=request.user) | Q(user__in=followee)) 
    all_reviews = all_reviews.annotate(content_type=Value('REVIEW', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(all_reviews, all_tickets), 
        key=lambda post: post.time_created, 
        reverse=True
    )
    print("POST = ", posts)
    return render(request, 'review/feed.html', context={'posts': posts})

@login_required
def write_review(request):
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        #This request coming from "Write review" form in feed/ticket_snippet
        if 'ticket_pk' in request.POST:
            ticket_pk =request.POST['ticket_pk'] 
            #This request comming from "Write review" form in feed/ticket_snippet
            print('TICKET_PK=', request.POST['ticket_pk'])
            ticket = models.Ticket.objects.get(id=request.POST['ticket_pk'])
            save_ticket = ticket
            return render(request, 'review/write_review.html', context={'ticket':ticket, 'review_form':review_form})
        elif 'rating' in request.POST:
#            #This request coming from "Send" form in write_review and may happen only
#            #when request Write Review has been issued. Hence ticket object exists.
            review_form = forms.ReviewForm(request.POST)
            print("REQUEST FROM SEND BTN IN WRITE_HTML ", request.POST)
            if review_form.is_valid():
                print("The review Form is valid")
                review = review_form.save(commit=False)
                review.ticket = models.Ticket.objects.get(id=request.POST['reviewed_ticket_pk']) 
                review.user = request.user
                print("REVIEW : ", review)
                print("REVIEW : ", review)
                print("RATING : ", review.rating)
                print("HEADLINE : ", review.headline)
                print("BODY : ", review.body)
                review.save()
                return redirect('feed')
            else:
                return render(request, 'review/write_review.html', context={'review_form':review_form})
    return redirect('feed')


