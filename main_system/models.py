from django.db import models
import random
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    apply = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2', null=True, blank=True, default=None)
    balance = models.IntegerField(default=0, null=True, blank=True)
    activate = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    conditions = models.TextField(null=True, blank=True, default=None)
    Lender_approval = models.BooleanField(default=False)
    Borrower_approval = models.BooleanField(default=False)
    percentage = models.IntegerField(default=0, null=True, blank=True)
    duration = models.IntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return f"{self.user}"


class Lender(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    conditions = models.TextField()
    Lender_approval = models.BooleanField(default=False)
    Borrower_approval = models.BooleanField(default=False)
    percentage = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)


    @property
    def total_all(self):
        total_all = self.amount * self.percentage/100
        total_all += self.amount
        return total_all

    def __str__(self):
        return f"{self.user} lending {self.amount} on {self.date_created}"


class applyLoan(models.Model):
    post = models.ForeignKey(Lender, related_name='loans', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    def __str__(self):
        return '%s - %s' % (self.post.user, self.name)

    @property
    def children(self):
        return applyLoan.objects.filter(parent=self).order_by('date').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False



class AppyLoan(models.Model):
    loan = models.ForeignKey(Lender, on_delete=models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)
    apply = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class Borrower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    purpose = models.TextField()
    percentage = models.IntegerField(default=0)
    Lender_approval = models.BooleanField(default=False)
    Borrower_approval = models.BooleanField(default=False)
    duration = models.IntegerField(default=0)

    @property
    def total(self):
        total = self.amount * self.percentage / 100
        total += self.amount
        return total

    def __str__(self):
        return f"{self.user }"


class Tranfer(models.Model):
    recieving_user = models.CharField(max_length=30, blank=False, null=False)
    amount= models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.amount} transfered to {self.recieving_user}"

