from django.db import models


class PayService(models.Model):
    id = models.IntegerField(primary_key=True)
    accountno = models.CharField(max_length=50, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    service_id = models.IntegerField(blank=True, null=True)
    pay_id = models.IntegerField(blank=True, null=True)
    pay_date = models.DateField(blank=True, null=True)
    sum = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    position = models.BigIntegerField(blank=True, null=True)
    positionn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'pay_service'

    def __str__(self):
        return self.accountno


class Customers(models.Model):
    customerid = models.IntegerField(blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    customername = models.CharField(max_length=50, blank=True, null=True)
    otchestvo = models.CharField(max_length=50, blank=True, null=True)
    accountno = models.CharField(max_length=50, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    creditsum = models.BigIntegerField(blank=True, null=True)
    creditpurpose = models.CharField(max_length=20, blank=True, null=True)
    companyname = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        p = ' '
        fio = self.surname + p + self.customername + p + self.otchestvo
        return fio


class CheckService(models.Model):
    id = models.IntegerField(primary_key=True)
    accountno = models.CharField(max_length=50, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    service_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'check_service'

    def __str__(self):
        return self.id
