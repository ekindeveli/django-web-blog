from django.shortcuts import render, reverse, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import CommentForm
from django.contrib import messages

# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class UserCommentListView(ListView):
    model = Comment
    template_name = 'blog/user_comments.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Comment.objects.filter(name=user).order_by('-created_on')


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        if self.request.user.username == comment.name:
            return True
        return False

    def get_success_url(self):
        comment_author = self.get_object().name
        return reverse_lazy('user-comments', kwargs={'username': comment_author})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body']

    def form_valid(self, form):
        form.instance.name = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user.username == comment.name:
            return True
        return False


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.object)
        context['comments'] = comments
        comment_author_profiles = {}
        for comment in comments:
            if User.objects.filter(username=comment.name).first():
                comment_author_profiles[f'{comment.name}'] = True
            else:
                comment_author_profiles[f'{comment.name}'] = False
        context['author_profiles'] = comment_author_profiles
        context['form'] = CommentForm
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            if request.POST.get('parent-comment-none') == "none":
                pass
            else:
                try:
                    comment.parent_comment = Comment.objects.filter(pk=int(request.POST.get('parent-comment-pk'))).first()
                except TypeError:
                    comment.parent_comment = Comment.objects.filter(pk=int(request.POST.get('child-parent-comment-pk'))).first()

            if User.objects.filter(username=comment.name):
                if request.user.is_authenticated and request.user == User.objects.filter(username=comment.name).first():
                    comment.save()
                    self.object = self.get_object()
                    context = super().get_context_data(**kwargs)
                    context['comments'] = Comment.objects.filter(post=self.object)
                    context['form'] = CommentForm()
                    return HttpResponseRedirect(reverse("post-detail", kwargs={'pk': self.object.pk}))
                else:
                    messages.error(request, f"To post a comment as {comment.name}, please log in as {comment.name}.")
                    self.object = self.get_object()
                    return HttpResponseRedirect(reverse("post-detail", kwargs={'pk': self.object.pk}))
            else:
                comment.save()
                self.object = self.get_object()
                context = super().get_context_data(**kwargs)
                context['comments'] = Comment.objects.filter(post=self.object)
                context['form'] = CommentForm()
                return HttpResponseRedirect(reverse("post-detail", kwargs={'pk': self.object.pk}))
        else:
            self.object = self.get_object()
            context = super().get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context=context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


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
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
