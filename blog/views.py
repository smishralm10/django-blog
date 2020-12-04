from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.http import JsonResponse, HttpResponseForbidden
from django.core import serializers
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserPostListView, self).get_context_data()
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        try:
            context['image'] = Post.objects.filter(author=user)[0].author.profile.image.url 
        except Exception:
            pass
        return context

class PostDisplay(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDisplay, self).get_context_data()
        context['comments'] = Post.objects.get(pk=self.kwargs['pk']).comments.all()
        context['form'] = CommentForm
        return context

class PostComment(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'blog/post_detail.html'
    form_class = CommentForm
    model = Post

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        form = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={"pk": self.object.pk})
    


class PostDetailView(View):
    
    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author



def about(request):
    return render(request, 'blog/about.html')