#Configure templates, static dirs

#start app core

#base,index,navbar,footer .html files

#Configure static url, media url in project urls.py

    from django.conf import settings
    from django.conf.urls.static import static

    if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

#start app userauth
    
    #customUser
        from django.contrib.auth.models import AbstractUser
        class customUser(AbstractUser):
    AUTH_USER_MODEL in settings

    #registration and login
        templates- login, register .html
        forms.py - registerform from UserCreationForm
            reference for form fields:
            username = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control my-2 p-3 rounded rounded-3 w-75',
            }))
    #handle form submition in views via authenticate,login,logout
        from django.contrib.auth import authenticate, login, logout

#define models
    #pip install django-shortuuidfield for shorter uuids
    #from shortuuid.django_fields import ShortUUIDField
        category_id = ShortUUIDField(unique=True, prefix='CAT', length=10,) additional max_length=20 and alphabets are optional

    #Tags




