from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Member
from .forms import RegisterForm, LoginForm
 

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','first_name','last_name')
    class Meta:
        ordering = ('id','username')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['password'].disabled = True 
        return form
        


    
