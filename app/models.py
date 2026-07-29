from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=100,null=False)
    category = models.CharField(max_length=20)
    dabit = models.IntegerField(null=True, default=0)
    credit = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)

    jama = models.IntegerField(default=0)
    kharch = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.account} - {self.date}"