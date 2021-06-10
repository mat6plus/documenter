from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from documenter.models import Searcher
from documenter.forms import SearchForm, DocumentForm
from taggit.models import Tag


# Solution Author Information

# def get_author(user):
#     qs = Author.objects.filter(user=user)
#     if qs.exists():
#         return qs[0]
#     return None


@login_required
def homeView(request):
    if not request.user.is_authenticated:
        return render(request, 'documenter/_partial/home.html')
    elif not request.user.is_authenticated:
        return redirect('accounts:register')
###################################################################
# def document_search():
#     form = SearchForm()
#     query = None
#     result = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Searcher.objects.annotate(search=SearchVector('title', 'description', 'tags'),).filter(search=query) 


# def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list = Searcher.objects.annotate(
#             search=SearchVector('title', 'description', 'tags'),
#         ).filter(search=query)
#         return object_list







##################################################################

# @login_required
# class searchView(View):
#     def get(self, request, *args, **kwargs):
#         queryset = Searcher.objects.all()
#         query = request.GET.get('q')
#         if query:
#             queryset = queryset.filter(
#                 Q(title__icontains=query) |
#                 Q(description__icontains=query)
#             ).distinct()
#         context = {'queryset': queryset}
#         return render(request, 'documenter/_partials/searchResult.html', context) 

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
####################################################################################
@login_required
class SearchView(ListView):
    model = Searcher
    context_object_name = 'searches'
    paginate_by = 10
    template_name = 'documenter/_partials/searchResult.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            result = Searcher.objects.annotate(search=SearchVector('title', 'description', 'tags'),).filter(search=query)
            if not result:
                messages.INFO(self.request, 'There was no result for the "{}".'.format(query))
            else:
                messages.SUCCESS(self.request, 'Search result for "{}".'.format(query))
            return result




###################################################################################

# @login_required
# class SearchResultView(ListView):
#     model = Searcher
#     context_object_name = 'searches'
#     paginate_by = 10
#     template_name = 'documenter/_partials/searchResult.html'

# def get_queryset(self, tag_slug=None):
#     query = self.request.GET.get('q')
#     tag = None

#     if tag_slug:
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         object_list = Searcher.filter(tags__in=[tag])

#     paginator = Paginator(object_list, 10) # 10 search result in each page
#     page = self.request.GET.get('page')

#     if query:
#         searchResult = Searcher.objects.all()

#     try:
#         searchResult = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         searchResult = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         searchResult = paginator.page(paginator.num_pages)
#     return render(request,
#                  'documenter/_partials/searchResult.html',
#                  {'page': page,
#                   'searchResult': searchResult,
#                   'tag': tag})


@login_required

class SearchDetails(DetailView):
    model = Searcher
    template_name = 'documenter/_partials/landing.html'

@login_required
class DocumenterView(CreateView):
    model = Searcher
    template_name = "documenter/_partials/documenter.html"