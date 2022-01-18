"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import review.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', review.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('review/create_ticket', review.views.ticket_and_image_upload, name='create_ticket'),
    path('review/<int:id>/', review.views.post_detail, name='post_detail'),
    path('review/<int:id>/ticket_update/', review.views.ticket_update, name='ticket_update'),
    path('review/<int:id>/ticket_delete/', review.views.ticket_delete, name='ticket_delete'),
    path('review/create_review', review.views.create_review, name='create_review'),
    path('review/write_review', review.views.write_review, name='write_review'),
    path('review/<int:id>/review_update/', review.views.review_update, name='review_update'),
    path('review/<int:id>/review_delete/', review.views.review_delete, name='review_delete'),
    path('review/follower_update/', review.views.follower_update, name='follower_update'),
    path('review/post_update/', review.views.post_update, name='post_update'),
    path('review/feed/', review.views.feed, name='feed'),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
