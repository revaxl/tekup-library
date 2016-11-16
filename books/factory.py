import factory
from .models import Book, Tags

class BookFactory(factory.Django.DjangoModelFactory):
	class Meta:
		model = Book
