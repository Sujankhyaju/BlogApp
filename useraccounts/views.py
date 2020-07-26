from django.shortcuts import render, redirect,get_object_or_404

# Create your views here.
from django.views.generic import View,DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserSignUpForm,UserLoginForm,UserProfileUpdateForm
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from .tokens import account_activation_token
# from django.core.mail import EmailMessage
# from django.utils.encoding import force_bytes, force_text
from django.contrib import messages
from blogs.models import Blogs
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class SignUpView(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect('useraccounts:edit')

        register_form = UserSignUpForm()
        return render(request,'useraccounts/register.html',{'register_form': register_form})

    def post(self,request):
        register_form = UserSignUpForm(request.POST)
        try:
            registered_user= User.objects.all().filter(email= register_form['email'].value())[0]
        except:
            registered_user = None

        if registered_user is None:
            if register_form.is_valid():
                # new_user = register_form.save(commit=False)
                new_user = register_form.save()
                # new_user.set_password(register_form.cleaned_data['password1'])
                # new_user.is_active = False
                new_user.is_active = True
                new_user.save()
                # current_site = get_current_site(request)
                # mail_subject = 'Activate Your T-Blog account.'
                # message = render_to_string('useraccounts/activate_email.html',{
                #     'user':new_user,
                #     'domain': current_site.domain,
                #     'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                #     'token':account_activation_token.make_token(new_user),
                # })
                # to_email = register_form.cleaned_data.get('email')
                # email = EmailMessage(
                #     mail_subject,message,to=[to_email]
                # )
                # email.send()
                # user = new_user.cleaned_data.get('first_name')
                messages.success(request,"Successfully SignUp! Please activate your account mail has been send to your mail box")
                print('success')
                return redirect('useraccounts:login')

            else:
                print('registered')
                messages.error(request,"Email has been registered already!!")
                return redirect('useraccounts:login')

        return render(request, 'useraccounts/register.html', {'register_form': register_form})


# class ActivateView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.success(request, "  Thank you for your email confirmation. Now you can login to your account.")
#             return redirect('useraccounts:login')
#
#         else:
#             messages.error(request, "   Activation link is invalid!.", fail_silently=True)
#             return redirect('useraccounts:login')

class LoginView(View):
    template_name = 'useraccounts/login.html'
    def get(self,request,*args,**kwargs):
        form = UserLoginForm()
        if request.user.is_authenticated:
            print('hello')
            return redirect('blogs:userdetail')
        return render(request,'useraccounts/login.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            # print(clean_data)
            username = User.objects.all().filter(email=clean_data['email'])
            if username:
                user = authenticate(request,username=username[0],password=clean_data['password'])
                print(user)

                if user is not None:
                    if user.is_active:
                        print(user.is_active)
                        login(request,user)
                        messages.success(request,'Authentication Succeed')
                        return redirect('blogs:profile',request.user.username,request.user.id)

                else:
                    messages.error(request,"Incorrect Password")
                    return redirect("useraccounts:signup")
            else:
                messages.error(request, 'Incorrect Mail ID')
                return redirect('useraccounts:login')
        return render(request,'useraccounts/login.html',{'form':form})

class ProfileView(View):

    def get(self,request,pk,*args,**kwargs):
        user = get_object_or_404(User,pk=pk)
        return render(request,'useraccounts/profile.html',{'user':user})


class UserBlogListView(DetailView):
    def get(self,request,author,author_id,*args,**kwargs):
        blogs= Blogs.objects.all().filter(author_id=author_id)
        return render(request,'useraccounts/user_blogs.html',{'blogs':blogs})








@method_decorator(login_required,name='dispatch')
class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,'Successfully Logout')
        return redirect('useraccounts:login')

@method_decorator(login_required,name='dispatch')
class ProfileUpdateView(View):
    model = User

    def get(self,request,author_id,*args,**kwargs):
        # if bool(Profile.objects.filter(user=request.user)) is False:
        #     obj = Profile(user=request.user)
        #     obj.save()
        profile_update_form = UserProfileUpdateForm()
        # profile_form = EditProfileForm(instance=request.user.profile)
        return render(request,'useraccounts/profile_edit.html',{'profile_update_form':profile_update_form})


    def post(self,request,author_id,*args,**kwargs):
        user = User.objects.get(id=author_id)


        profile_update_form = UserProfileUpdateForm(request.FILES,request.POST)
        print(profile_update_form.is_valid())

        if profile_update_form.is_valid():
            # user.avatar = profile_update_form.cleaned_data['avatar']
            user = profile_update_form.save()
            # user.bio = profile_update_form.cleaned_data['bio']
            user.first_name = profile_update_form.cleaned_data['first_name']
            # user.username= profile_update_form.cleaned_data['username']
            print('error')
            user.save()
            messages.success(request,'Update Succeed')
            return redirect('blogs:profile')
        else:
            messages.error(request, 'Error Occurred, Try again')

        return render(request,'useraccounts/profile_edit.html',{'profile_update_form':profile_update_form}
                      )

