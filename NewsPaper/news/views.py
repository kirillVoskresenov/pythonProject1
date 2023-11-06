from django.views.generic import ListView, DetailView, CreateView,\
    UpdateView, DeleteView
from .models import Post, Category, PostCategory
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .tasks import new_post_task

class PostsList(ListView):
    model = Post
    ordering = '-article_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    queryset = Post.objects.order_by('-article_date')
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'

class NewsCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
    # Указываем нашу разработанную форму
    form_class = PostsForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'
    permission_required = ('news.create_post')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.post_type = 'NE'
            post.save()
            new_post_task.delay(post.pk)
        return super().form_valid(form)

class ArticlesCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
    # Указываем нашу разработанную форму
    form_class = PostsForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'articles_edit.html'
    permission_required = ('news.create_post')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.post_type = 'NE'
            post.save()
            new_post_task.delay(post.pk)
            
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    form_class = PostsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.update_post')

    def get_queryset(self):
        return super().get_queryset().filter(post_type='NE')

class ArticlesUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    form_class = PostsForm
    model = Post
    template_name = 'articles_edit.html'
    permission_required = ('news.update_post')

    def get_queryset(self):
        return super().get_queryset().filter(post_type='AR')

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')

    def get_queryset(self):
        return super().get_queryset().filter(post_type='NE')

class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('news')

    def get_queryset(self):
        return super().get_queryset().filter(post_type='AR')

