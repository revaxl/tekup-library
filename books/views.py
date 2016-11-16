from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from stronghold.views import StrongholdPublicMixin

from .forms import BookBorrowForm, BookForm, SuggestBookForm
from .models import Book, BookBorrow, Tags


class BookListView(StrongholdPublicMixin, ListView):
	def get(self, request):
		books = Book.objects.all()
		tags = Tags.objects.all()
		query = request.GET.get("q")
		if query:
			books = books.filter(
			Q(book_name__icontains=query)|
			Q(author_name__icontains=query)|
			Q(tags__name__icontains=query)
			).distinct()

		paginator = Paginator(books, 3) # Show 3 books per page

		page = request.GET.get('page')
		try:
			books = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			books = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			books = paginator.page(paginator.num_pages)
		
		context = {
			'books' : books,
			'tags' : tags
			}
		return render(request, 'book_list.html', context)


class BookDetailView(StrongholdPublicMixin, DetailView):
	model = Book
	pk_url_kwarg = 'id'
	template_name = "book_detail.html"
	form = BookBorrowForm()

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(BookDetailView, self).get_context_data(**kwargs)
		# Add in the publisher
		context['form'] = self.form
		return context


def bookborrow(request, id):
	book_id = get_object_or_404(Book, id=id)
	form = BookBorrowForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			date_borrow_start = form.cleaned_data.get("date_borrow_start")
			date_borrow_end = form.cleaned_data.get("date_borrow_end")
			instance = form.save(commit=False)
			instance.book_borrowed = book_id
			instance.user = User.objects.get(id=request.user.id)
			instance.save()
		return redirect(reverse('books:detail', kwargs={'id': book_id.id}))
	context = {
		'form' : form
	}
	return render(request, 'book_borrow.html', context)



class SuggestBookView(StrongholdPublicMixin,SuccessMessageMixin, FormView):
	template_name = 'suggestbook.html'
	form_class = SuggestBookForm
	success_url = reverse_lazy('index')
	success_message = "Thank you!"

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.save()
		return super(SuggestBookView, self).form_valid(form)
