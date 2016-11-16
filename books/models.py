import pendulum

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


class Tags(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Tags"


class Book(models.Model):
	book_name = models.CharField(max_length=200)
	slug = models.CharField(max_length=255, unique=True)
	author_name = models.CharField(max_length=200)
	isbn = models.IntegerField(verbose_name='ISBN', unique=True)
	status = models.BooleanField(default=True)
	description = models.TextField(null=True, blank=True)
	tags = models.ManyToManyField(Tags, blank=True)
	image = models.ImageField(
			null=True, 
			blank=True, 
			width_field="width_field", 
			height_field="height_field")	
	height_field = models.IntegerField(default=300)
	width_field = models.IntegerField(default=250)
	created = models.DateField(auto_now_add=True)
	updated = models.DateField(auto_now=True)
	number_of_pages = models.IntegerField()
	publish_date = models.DateField(null=True, blank=True)
	publish_place = models.CharField(max_length=200, null=True, blank=True)
	edition = models.CharField(max_length=100, null=True, blank=True)
	nbrOfBooks = models.IntegerField(default=1)
	borrower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='books', blank=True, null=True)


	def __str__(self):
		return self.book_name

	def __unicode__(self):
		return self.book_name

	def get_tags(self):
		tags = ','.join([tag.name for tag in self.tags.all()])
		return tags

	def get_absolute_url(self):
		return reverse("books:detail", kwargs={"id" : self.id})

	class Meta:
		ordering = ["-created"]


def create_slug(instance, new_slug=None):
	book_name_lowered = instance.book_name.lower()
	slug = slugify(book_name_lowered)
	if new_slug is not None:
		slug = new_slug
	qs = Book.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
	

pre_save.connect(pre_save_post_receiver, sender=Book)


class BookBorrow(models.Model):
	date_borrow_start = models.DateField()
	date_borrow_end = models.DateField(blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	note = models.TextField(blank=True, null=True)
	book_borrowed = models.ForeignKey(Book)

	def __str__(self):
		return str(self.date_borrow_start)

	def __unicode__(self):
		return self.date_borrow_start


def post_save_post_receiver(sender, instance, *args, **kwargs):
	book_id = instance.book_borrowed.id
	book = get_object_or_404(Book, id=book_id)
	book.date_borrow_start = pendulum.now()
	book.date_borrow_end = pendulum.now().add(days=7)
	book.borrower = instance.user
	book.nbrOfBooks = F('nbrOfBooks')-1
	if book.nbrOfBooks == 0:
			book.status = False
	book.save()

post_save.connect(post_save_post_receiver, sender=BookBorrow)


class BookSuggestion(models.Model):
	book_name = models.CharField(max_length=200)
	isbn = models.IntegerField(blank=True, null=True)
	author_name = models.CharField(max_length=200, blank=True, null=True)
	comment = models.TextField(blank=True, null=True)
	created = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.book_name

	def __unicode__(self):
		return self.book_name

	class Meta:
		ordering = ['-created']