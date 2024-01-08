from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView,CreateView,ListView,UpdateView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from store.decorators import login_required

from api.models import Category
from store.forms import LoginForm,CategoryForm

# Create your views here.
decs=[login_required,never_cache]

class SignInView(FormView):
    template_name="signin.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=uname,password=pwd)
            if user_obj:
                login(request,user_obj)
                return redirect("index")
        return render (request,"signin.html",{"form":form})

class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(decs,name="dispatch")
class CategoryAddView(CreateView):
    template_name="category-add.html"
    form_class=CategoryForm
    def get_success_url(self):
        return reverse ("index")
    
@method_decorator(decs,name="dispatch")
class CategoryListView(ListView):
    template_name="index.html"
    model=Category
    context_object_name="data"

@method_decorator(decs,name="dispatch")
class CategoryUpdateView(UpdateView):
    template_name="category-update.html"
    form_class=CategoryForm
    model=Category
    def get_success_url(self):
        return reverse("index")
