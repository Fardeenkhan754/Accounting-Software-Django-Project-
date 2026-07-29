from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import Account, Transaction
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import subprocess
from datetime import datetime
import os
import shutil
from django.conf import settings
from django.contrib import messages
import csv



def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("cash_book")

        else:
            return render(request, "login.html", {
                "error": "Invalid Username or Password"
            })

    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("login")

def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Date",
        "Account",
        "Description",
        "jama",
        "kharch"
    ])

    transactions = Transaction.objects.all()

    for t in transactions:
        writer.writerow([
            t.date,
            t.account.name,
            t.description,
            t.jama,
            t.kharch
        ])

    return response

def update_transaction(request, id):

    transaction = get_object_or_404(Transaction, id=id)

    accounts = Account.objects.all()

    if request.method == "POST":

        transaction.account = Account.objects.get(
            id=request.POST.get("account")
        )

        transaction.date = request.POST.get("date")
        transaction.description = request.POST.get("description")
        transaction.jama = int(request.POST.get("jama") or 0)
        transaction.kharch = int(request.POST.get("kharch") or 0)

        transaction.save()

        return redirect("reports")

    return render(
        request,
        "update_transaction.html",
        {
            "transaction": transaction,
            "accounts": accounts,
        },
    )

def backup_database(request):

    db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")

    backup_folder = os.path.join(settings.BASE_DIR, "backups")
    os.makedirs(backup_folder, exist_ok=True)

    # Backup files ki list lo
    backups = [
        os.path.join(backup_folder, file)
        for file in os.listdir(backup_folder)
        if file.endswith(".sqlite3")
    ]

    # Date ke hisab se sort karo (oldest first)
    backups.sort(key=os.path.getmtime)

    # Sirf 3 backups rakhna
    while len(backups) >= 3:
        os.remove(backups[0])
        backups.pop(0)

    # Naya backup banao
    filename = datetime.now().strftime("backup_%Y%m%d_%H%M%S.sqlite3")
    backup_path = os.path.join(backup_folder, filename)

    shutil.copy2(db_path, backup_path)

    messages.success(request, "Database backup created successfully.")

    return redirect(request.META.get("HTTP_REFERER", "cash_book"))

@login_required(login_url="login")
def add_customer(request):
    if request.method == "POST":
        # to get data:
        name = request.POST.get("name")
        category = request.POST.get("category")
        dabit = int(request.POST.get("dabit") or 0)
        credit = int(request.POST.get("credit") or 0)

        Account.objects.create(
            name=name,
            category=category,
            dabit=dabit,
            credit=credit,
        )

    # to show data
    accounts = Account.objects.all()

    template = loader.get_template("Add-Account.html")

    context = {
        "accounts": accounts,
    }
    
    return HttpResponse(template.render(context, request))

@login_required(login_url="login")
def cash_book(request):
    template = loader.get_template("Cash-Book.html")
    accounts = Account.objects.all()
    context = {
        "accounts": accounts,
    }

    if request.method == "POST":
        account_id = request.POST.get("account")

        account = Account.objects.get(id=account_id)

        date = request.POST.get("date")
        description = request.POST.get("description")
        jama = int(request.POST.get("jama") or 0)
        kharch = int(request.POST.get("kharch") or 0)

        Transaction.objects.create(
            account=account,
            date=date,
            description=description,
            jama=jama,
            kharch=kharch
        )
        return redirect("/cash_book")

    return HttpResponse(template.render(context, request))

@login_required(login_url="login")
def reports(request):
    template = loader.get_template("Reports.html")

    if request.method == "GET":
        transactions = Transaction.objects.none()

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date and end_date:
            transactions = Transaction.objects.filter(
                date__range=[start_date, end_date]
            ).order_by("date")
        
        total_jama = transactions.aggregate(Sum("jama"))["jama__sum"] or 0

        total_kharch = transactions.aggregate(Sum("kharch"))["kharch__sum"] or 0

        balance = total_jama - total_kharch

        context = {
            "transactions": transactions,
            "start_date": start_date,
            "end_date": end_date,
            "total_jama": total_jama,
            "total_kharch": total_kharch,
            "balance" : balance,
        }
    return HttpResponse(template.render(context, request))

@login_required(login_url="login")
def account_ledger(request):
    template = loader.get_template("Accounts-Reports.html")

    accounts = Account.objects.all()
    account = None
    transactions = Transaction.objects.none()

    opening_jama = 0
    opening_kharch = 0

    account_id = request.GET.get("account")

    if account_id:

        account = Account.objects.get(id=account_id)

        transactions = Transaction.objects.filter(
            account=account
        ).order_by("date")

        opening_jama = account.dabit
        opening_kharch = account.credit
        

    total_jama = (transactions.aggregate(Sum("jama"))["jama__sum"] or 0)

    total_kharch = transactions.aggregate(Sum("kharch"))["kharch__sum"] or 0

    total_jama = opening_jama + total_jama
    total_kharch = opening_kharch + total_kharch

    balance = total_jama - total_kharch

    context = {
        "account": account,
        "transactions": transactions,
        "accounts": accounts,
        "transactions": transactions,
        "selected_account": account_id,
        "total_jama": total_jama,
        "total_kharch": total_kharch,
        "balance" : balance,
    }

    return HttpResponse(template.render(context, request))