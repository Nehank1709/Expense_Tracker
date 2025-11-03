from django.shortcuts import render, redirect
from .models import CurrentBalance, TrackingHistory
from django.db.models import Sum
from django.contrib import messages

# Create your views here.

def index(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if float(amount) == 0:
            messages.error(request, "Amount cannot be zero.")
            return redirect('/')
        
        current_balance, created = CurrentBalance.objects.get_or_create(id=1) 
        tracking_history = TrackingHistory.objects.create(
            current_balance=current_balance,
            amount=amount,
            expense_type='DEBIT' if float(amount) < 0 else 'CREDIT',
            description=description
        )
        current_balance.amount += float(amount) 
        current_balance.save()

        # print(f"Description: {description}, Amount: {amount}")
        return redirect('/')
    
    income=0
    expense=0

    for transaction_history in TrackingHistory.objects.all():
        if transaction_history.expense_type == 'CREDIT':
            income += transaction_history.amount
        else:
            expense += abs(transaction_history.amount)
    
    current_balance, created = CurrentBalance.objects.get_or_create(id=1)
    context = {'income': income, 'expense': expense, 'transactions': TrackingHistory.objects.all(), 'current_balance': current_balance}
    return render(request, 'index.html', context)


def delete_transaction(request, transaction_id):
    transaction = TrackingHistory.objects.get(id=transaction_id)
    current_balance = transaction.current_balance

    if transaction.expense_type == 'CREDIT':
        current_balance.amount -= transaction.amount
    else:
        current_balance.amount += abs(transaction.amount)
    
    current_balance.save()
    transaction.delete()
    return redirect('/')
