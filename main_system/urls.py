from django.contrib import admin
from django.urls import path, include
from .views import Home, Login, Signup, Logout, borrowers, transfer, dashboard, \
    CreateBorrower, DeleteBorrowers, DeleteLender, LenderDetail, about, \
    CreateLoan, lendersList, ApproveLoan, AllTransactions, UserPostList, update,\
    verification, VerificationSuccess, ApprovalSuccess, loandetails

urlpatterns = [
    path('',Home),
    path('dashboard/', dashboard, name='dashboard'),
    #path('apply/<int:id>/', applyloan, name='apply_section'),
    path('about/', about, name='about'),
    path('VerificationSuccess', VerificationSuccess, name='VerificationSuccess'),
    path('ApprovalSuccess', ApprovalSuccess, name='ApprovalSuccess'),
    path('login/', Login, name='login'),
    path('register/', Signup.as_view(), name='register'),
    path('logout/', Logout, name='logout'),
    path('loan_list/', borrowers.as_view(), name='loan_list'),
    path('lenders_list/', lendersList, name='lenders_list'),
    path('transfer/', transfer, name='transfer'),
    path('newlender/',CreateLoan, name='newlender'),
    path('request-loan', CreateBorrower.as_view(), name='CreateBorrower'),
    path('delete', DeleteBorrowers.as_view(), name='DeleteBorrowers'),
    path('delete/<int:pk>/', DeleteLender.as_view(), name='DeleteLender'),
    path('loan-details/<int:id>/', LenderDetail, name='LenderDetails'),
    path('approve/', ApproveLoan, name='ApproveLoan'),
    path('transactions', AllTransactions, name='AllTransactions'),
    path('lend-fund/', UserPostList, name='My_post'),
    path('update/<int:pk>/', update.as_view(), name='update'),
    path('loandetails/<int:id>/',loandetails, name='loandetails'),
    path('verification-application', verification.as_view(), name='verification')
]
