from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Tweet


# Create your views here.
# CRUD: Create, Retrieve, Update, Delete


# Create
class TweetCreateView(FormUserNeededMixin, CreateView):
    # queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'
    # success_url = reverse_lazy("tweets:detail")
    # login_url = '/admin/'

    # def form_valid(self, form):
    #     if self.request.user.is_authenticated:
    #         form.instance.user = self.request.user
    #         return super(TweetCreateView, self).form_valid(form)
    #     else:
    #         form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue"])
    #         return self.form_invalid(form)


# Update
class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'
    # success_url = '/tweets/'


# Retrieve
class TweetDetailView(DetailView):
    # template_name = "tweets/detail_view.html"
    queryset = Tweet.objects.all()

    def get_object(self):
        print(self.kwargs)
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(Tweet, pk=pk)
        return obj


class TweetListView(ListView):
    def get_queryset(self, *args, **kwargs):
        queryset = Tweet.objects.all()
        print(self.request.GET)
        query = self.request.GET.get("q", None)
        if query is not None:
            queryset = queryset.filter(
                                    Q(content__icontains=query) | Q(user__username__icontains=query))

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TweetListView, self).get_context_data()
        context["create_form"] = TweetModelForm
        context["create_url"] = reverse_lazy("tweets:create")
        print(context)
        return context


# Delete
class TweetDeleteView(DeleteView):
    model = Tweet
    template_name = "tweets/delete_confirm.html"
    success_url = reverse_lazy("tweets:list")  # tweets/list


# def tweet_detail_view(request, id=1):
#     obj = Tweet.objects.get(id=id) # GET from database
#     print(obj)
#     context = {
#         "object": obj
#     }
#     return render(request, "tweets/detail_view.html", context)
#
#

