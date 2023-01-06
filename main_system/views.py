import decimal
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Account, Lender, Borrower, Tranfer,applyLoan
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import TransferForm, SignupForm, BorrowersForm, LenderForm, ApplyForm
from django.contrib.auth.forms import User


def Home(request):
    return render(request, 'index.html', )

def about(request):
    return render(request, 'about.html', )


def dashboard(request):
    return render(request, 'dashboard.html')


#this is the login
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {'error': 'Invalid login details'}
            return render(request, 'login2.html', context)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'login2.html')


#this is the logout
def Logout(request):
    logout(request)
    return redirect('login')


#This is the Signup/Registeration
class Signup(SuccessMessageMixin, generic.CreateView):
    form_class = SignupForm
    template_name = 'register2.html'

    def get_success_url(self):
        messages.success(self.request, 'Your account has being created successfully, Please login')
        return reverse('login')


#This is to show the list of all  active Borrowers
class borrowers(ListView):
    model = Borrower
    template_name = 'borrowers.html'
    ordering = '-date_created'

    def get_queryset(self):
        return Borrower.objects.filter(Lender_approval=False).order_by('-date_created')


#This is creates a loan request with authentication
def CreateLoan(request):
    msg = " "
    if request.method == 'POST':
        user = request.user
        amount = request.POST['amount']
        conditions = request.POST['conditions']
        percentage = request.POST['percentage']
        duration = request.POST['duration']

        lender =request.user

        lender_accunt = Account.objects.get(user=lender)
        if lender_accunt.balance < int(amount):
            msg = 'Sorry, You dont have enough fund'
        else:
            createlender = Lender.objects.create(user=request.user, amount=amount, conditions=conditions, percentage=percentage, duration=duration)
            lender_accunt.balance = lender_accunt.balance - int(amount)
            createlender.save()
            lender_accunt.save()
            return redirect('lenders_list')
    return render(request, 'transfer2.html', {'msg': msg})


#This shows the list of all active Lenders
def lendersList(request):
    url = 'lender.html'

    lenders = Lender.objects.all()
    return render(request, url, {'lenders': lenders})


#This is for direct Fund Transfer
def transfer(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        amount = request.POST['amount']

        senderUser = User.objects.get(username=request.user)
        receiverUser = User.objects.get(username=username)

        sender = Account.objects.get(user=senderUser)
        reciever = Account.objects.get(user=receiverUser)

        if sender.balance < int(amount):
            msg = "Sorry, You don't have enough fund to perfrom this operation"
        else:
            sender.balance = sender.balance - int(amount)
            reciever.balance = reciever.balance + int(amount)
            sender.save()
            reciever.save()
            msg = "Transaction successful"
    return render(request, 'transfer.html', {'msg': msg})


#This Creates the request to borrow money
class CreateBorrower(CreateView):
    model = Borrower
    template_name = 'create_borrow.html'
    form_class = BorrowersForm
    success_url = reverse_lazy('loan_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateBorrower, self).form_valid(form)

#This shows the details of loan created
def LenderDetail(request, id=id):
    post = get_object_or_404(Lender, id=id)

    loanapply = applyLoan.objects.filter(post=post)
    if request.method == 'POST':
        comment_form = ApplyForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('comment')
            comments = applyLoan.objects.create(post=post, name=request.user, comment=content)
            comments.save()
            messages.success(request, 'Your comment has being posted successfully')
            return redirect('lenders_list')
    else:
        comment_form = ApplyForm()


    context = {
        'lenders': post,

        'loanapply': loanapply,
        'apply_form': ApplyForm,



    }
    return render(request, 'lender-details.html', context)


def ApproveLoan(request, id):

    loan = get_object_or_404(applyLoan, id=id)

    msg = ""

    lenderUser = User.objects.get(username=request.user)
    receiverUser = loan.name
    amount = loan

    sender = Account.objects.get(user=lenderUser)
    reciever = Account.objects.get(user=receiverUser)

    Recieveramount = reciever.balance
    senderamount = sender.balance



    context = {
        'loan':loan,
        'receiverUser': receiverUser,
        'sender':sender,
        'balance' : amount,

    }

    return render(request, 'approve.html', context)



class DeleteBorrowers(DeleteView):
    model = Borrower
    template_name = 'delete_borrower.html'


class DeleteLender(DeleteView):
    model = Lender
    template_name = 'delete_lender.html'
    success_url = reverse_lazy('lenders_list')

