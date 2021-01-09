from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils import timezone


from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView,UpdateView,CreateView,DeleteView,DetailView,ListView

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.models import Group

from blog.decorators import unauthenticated_user,admin_only,allowed_users
# Create your views here.

from blog.models import Post,Comment


from .forms import CreateUserForm,PostForm,CommentForm


class PostListView(LoginRequiredMixin,ListView):
   model = Post 

   def get_queryset(self):
       return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class DraftListView(LoginRequiredMixin,ListView):
    redirect_field_name ='post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
    
class CreatePost(LoginRequiredMixin,CreateView):
    
    redirect_field_name='blog/post_detail.html'
    template_name="blog/post_form.html"
    form_class = PostForm

class PostUpdateView(LoginRequiredMixin,UpdateView):
    redirect_field_name='blog/post_detail.html'

    form_class = PostForm
    model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url= reverse_lazy('blog:post_list')


def indexpage(request):
    return render(request,'blog/post_form.html')


def loginpage(request):
        if request.method == 'POST':
            usr=request.POST.get('usr')
            pwd=request.POST.get('pwd')

            user = authenticate(request,username=usr,password=pwd)

            if user is not None:
                login(request,user)
                return redirect('blog:post_list')

            else:
                messages.info(request,"Username or Password is Incorrect")

        context ={}
        return render(request,'registration/login.html',context)

@login_required
def logoutuser(request):
    logout(request)
    return redirect('blog:login')

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect ('blog:post_detail',pk=pk)

@unauthenticated_user
def registerpage(request):
   
  
        form = CreateUserForm()

        if request.method=='POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username = form.cleaned_data.get('username')
                messages.success(request,'Account was created for ' +username)

                group = Group.objects.get(name='Normal')
                user.groups.add(group)

                return redirect('blog:login')

        context={'form':form}
        return render(request,'registration/register.html',context)


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method =='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('blog:post_detail',pk=post.pk)
    else:
        form = CommentForm()

    return render(request,'blog/comment_form.html',{'form':form})


@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)