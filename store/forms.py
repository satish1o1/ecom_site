from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields

class RegisForm(UserCreationForm):
      class Meta:
            model = User
            fields = ['username','email','password1','password2']