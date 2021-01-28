from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from .models import Customers, CheckService, PayService
from django.contrib import messages
import pyodbc
from django.core.mail import EmailMessage

cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=10.10.1.2;'
    'DATABASE=Database;'
    'UID=dbadm;PWD=********')  # Строка подключения

user_id = 3819
username = '****'
message_send_list = ['*****@changan.kg', 'n.berdiev@changan.kg']


def debet_account_no(pay_id):  # Возвращает номер счета нужного контрагента
    if pay_id == 1:  # Pay24
        return 1061153100001931
    elif pay_id == 2:  # ЗАО "Финка Банк"
        return 1061153100002638
    elif pay_id == 3:  # QuickPay
        return 1061153100001729
    elif pay_id == 4:  # QIWI
        return 1061153100000214
    elif pay_id == 5:  # ЗАО "Банк Компаньон"
        return 1061153100001729


def pay_type(pay_id):  # Возвращает наименование нужного контрагента
    if pay_id == 1:
        return 'Pay24'
    elif pay_id == 2:
        return 'ЗАО "Финка Банк"'
    elif pay_id == 3:
        return 'QuickPay'
    elif pay_id == 4:
        return 'QIWI'
    elif pay_id == 5:
        return 'ЗАО "Банк Компаньон"'


def comment_customer(accountno):  # Возвращает ФИО клиента
    qs = Customers.objects.filter(accountno=accountno)
    if qs.exists():
        customer = qs[0]
        p = ' '
        return customer.surname + p + customer.customername + p + customer.otchestvo


class CustomerList(ListView):
    model = Customers
    template_name = 'terminal/customers.html'
    context_object_name = 'customers'
    ordering = ['surname']
    paginate_by = 30


def update_customers(request):  # Обновляет список клиентов с АБС базы
    cursor = cnxn.cursor()
    cursor.execute("{CALL Credits.GetAccountNoNew}")
    customers = cursor.fetchall()
    Customers.objects.all().delete()
    for row in customers:
        c = Customers(customerid=row.CustomerID, surname=row.SurName, customername=row.CustomerName,
                      otchestvo=row.Otchestvo, accountno=row.AccountNo, sex=row.Sex, creditsum=row.Approved_sum)
        c.save()
    cursor.close()
    messages.info(request, "Список клиентов успешно обновлен!")
    return redirect('customers')


class PaymentList(ListView):
    model = PayService
    template_name = 'terminal/payments.html'
    context_object_name = 'payments'
    ordering = ['pay_date']
    paginate_by = 30


class CheckList(ListView):
    model = CheckService
    template_name = 'terminal/check.html'
    context_object_name = 'check'
    ordering = ['create_date']
    paginate_by = 30


def message_text(pay_type, customer, accountno, date, sum, comment, user):  # Текст сообщения для отправки на почту
    msg = 'Тип платежа: %s<br>%s<br>%s<br>Дата погашения: %s<br>%s сом<br>%s<br>%s<br>' % (
        pay_type, customer, accountno, date, sum, comment, user)
    return msg


def make_income_operation(request, pk):  # Проведение проводки
    pay_qs = PayService.objects.filter(status=0, pk=pk)
    if pay_qs.exists():
        pay = pay_qs[0]
        cursor = cnxn.cursor()
        customer = comment_customer(pay.accountno)
        pay_name = pay_type(pay.service_id)
        comment = "Пополнение счета на погашение кредита {} через {} (ID {})".format(customer, pay_name, pay.pay_id)
        debet_account = debet_account_no(pay.service_id)
        cursor.execute(
            "{ CALL Deposits.MakeIncomeOperation(%d,417,%d,%d,0,'%s',NULL,'%s',%d, NULL)}" % (int(pay.accountno),
                                                                                              int(debet_account),
                                                                                              int(pay.sum),
                                                                                              comment,
                                                                                              username,
                                                                                              user_id))
        cnxn.commit()
        cursor.close()
        pay.status = 1
        pay.save()
        messages.info(request, "Успешная проводка!")  # Выведение сообщения о проводке в интерфейс
        msg = EmailMessage(
            customer,
            message_text(pay_name, customer, pay.accountno, pay.pay_date, pay.sum, comment, username),
            'abs@changan.kg',
            message_send_list
        )  # Отправка сообщения на почту
        msg.content_subtype = "html"
        msg.send()
        messages.info(request, "Сообщения отправлены!")  # Выведение сообщения об отправке на почту в интерфейс
    return redirect('payment')
