from django.contrib import admin
from .models import Account, Borrower, Lender, Tranfer, AppyLoan, applyLoan

admin.site.register(Account)
admin.site.register(Borrower)
admin.site.register(Lender)
admin.site.register(Tranfer)
admin.site.register(applyLoan)
