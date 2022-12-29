from django.db import models
from django.contrib.auth.models import User

class Receiver(models.Model):
    received_emails=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.received_emails


class Emails(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.PROTECT,blank=True,null=True)
    subject=models.CharField(max_length=200)
    sender=models.TextField()
    receiver=models.ForeignKey(Receiver,on_delete=models.CASCADE,blank=True,null=True)
    compose=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return self.subject
    
class EmailsSer(models.Model):
    user_id=models.TextField()
    subject=models.TextField()
    sender=models.TextField()
    receiver=models.TextField()
    compose=models.TextField()
    def __str__(self):
        return self.subject
