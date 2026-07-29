from django.contrib import admin
from .models import Account , Transaction

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
  list_display = ("name", "category", "dabit", "credit",)
  
admin.site.register(Account,MemberAdmin)

class AppAdmin(admin.ModelAdmin):
  list_display = ("account", "description", "jama", "kharch",)

admin.site.register(Transaction,AppAdmin)