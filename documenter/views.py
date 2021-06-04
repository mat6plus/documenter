from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from documenter.models import Searcher
from documenter.forms import SearchForm, DocumentForm
from taggit.models import Tag


# Solution Author Information

# def get_author(user):
#     qs = Author.objects.filter(user=user)
#     if qs.exists():
#         return qs[0]
#     return None

# Create your views here
# class homeView(View):

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(homeView, self).dispatch(*args, **kwargs)

#     def get(self, request):
#         return render(request, 'home.html')

@login_required
def homeView(request):
    if not request.user.is_authenticated:
        return render(request, 'documenter/_partial/home.html')
    elif not request.user.is_authenticated:
        return redirect('accounts:register')


@login_required
class searchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Searcher.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        context = {'queryset': queryset}
        return render(request, 'documenter/_partials/searchResult.html', context) 

# def search(request):
#     queryset = Searcher.objects.all()
#     query = request.GET.get('q')
#     if query:
#         queryset = queryset.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query)
#         ).distinct()
#     context = {
#         'queryset': queryset
#     }
#     return render(request, '_partials/searchResult.html', context)

@login_required
class SearchResultView(ListView):
    queryset = Searcher.objects.all()
    context_object_name = 'searches'
    paginate_by = 10
    template_name = 'documenter/_partials/searchResult.html'

def searchResult(request, tag_slug=None):
    object_list = Searcher.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 10) # 10 search result in each page
    page = request.GET.get('page')
    try:
        searchResult = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        searchResult = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        searchResult = paginator.page(paginator.num_pages)
    return render(request,
                 'documenter/_partials/searchResult.html',
                 {'page': page,
                  'searchResult': searchResult,
                  'tag': tag})


@login_required

class SearchDetails(DetailView):
    model = Searcher
    template_name = 'documenter/_partials/landing.html'

@login_required
class DocumenterView(CreateView):
    model = Searcher
    template_name = "documenter/_partials/documenter.html"