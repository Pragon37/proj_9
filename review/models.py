from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
"""
A few remainders for me:
    fields of models are defined in django.db.models.fields
    but are imported in django.db.models.
    By convention use:
        from django.db import models and refer to <Foo>Field with models.<Foo>Field
        
Field.null if true Djamgo stores empty value with null in the DB.
if Field.blank is True the field may be empty.It does not relation to the DB
it is there for validation. It allows to work with empty forms. 

"""

class Ticket(models.Model):
    def __str__(self):
        return f'{self.title}'

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=128, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
 

class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='followed_by')
    class Meta():
        unique_together=('user', 'followed_user', )

class Review(models.Model):
    def __str__(self):
        return f'{self.ticket}'
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

