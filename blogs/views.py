from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .forms import BlogCreateForm,BlogsForm
from .models import Blogs
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator


class DisplayPostView(ListView):
    model = Blogs
    template_name = 'blogs/index.html'
    context_object_name = 'posts'

    def get_queryset(self,*args,**kwargs):
        queryset= super(DisplayPostView,self).get_queryset(*args,**kwargs)

        queryset= queryset.order_by('-created')


        return queryset

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(DisplayPostView,self).get_context_data(*args,**kwargs)
        context['featured']= Blogs.objects.order_by('-created')[:2]
        context['authors'] = User.objects.all()
        context['Blogs']= Blogs.objects.all()[:5]

        return context


class DetailPostView(DetailView):
    model = Blogs
    form_class = BlogCreateForm

    context_object_name = 'posts'
    pk_url_kwarg = 'blog_id'
    slug_url_kwarg = 'slug'
    template_name = 'blogs/detail_blog.html'



class UserDetailView(DetailView):
    model = Blogs
    template_name = 'blogs/profile.html'
    context_object_name = 'posts'
    pk_url_kwarg = 'author_id'
    slug_url_kwarg = 'author'





@method_decorator(login_required(login_url='useraccounts/login/'), name ='dispatch')
class CreatePostView(CreateView):
    template_name = 'blogs/create_blog.html'
    form_class = BlogCreateForm
    success_message = "Post was created Successfully"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.save()
        form.save_m2m()
        return super().form_valid(form)

@method_decorator(login_required(login_url='/useraccounts/login/'), name='dispatch')
class UpdatePostView(UpdateView):
    model = Blogs
    form_class = BlogsForm
    pk_url_kwarg = 'id'
    author_url_kwarg = 'author'
    template_name = 'blogs/update_blog.html'
    success_message = "Successfully Updated"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        author = self.kwargs.get(self.author_url_kwarg)
        if pk is not None and author is not None:
            queryset = queryset.filter(author__id=pk).filter(author__username=author)

        if pk is None and author is  None:
            return "Attribute Error"

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            return "model not found"

        return obj

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author= self.request.user
        form.save()
        form.save_m2m()
        return redirect('/blogs/index.html')




@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class DeletePostView(DeleteView):
    def get(self, request, author_id):
        obj = get_object_or_404(Blogs,author__id=author_id)
        obj.delete()
        messages.success(request,"Delete Successfully")
        return redirect('blogs:user_detail',request.user.username,request.user.id)








