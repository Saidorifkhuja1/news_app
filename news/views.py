from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticleForm
from django.views.generic import DetailView, UpdateView, DeleteView



def news_home(request):
    news = Articles.objects.order_by('-data')
    return render(request, 'news/news_home.html', {'news':news})



class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticleForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this article.")
        return obj


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/delete_news.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this article.")
        return obj




@login_required
def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            # Set the author of the article to the current user
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('home')
        else:
            error = 'Form validation error'

    form = ArticleForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html', data)

