from django.contrib import admin

# Register your models here.

from .models import Book
from .models import Post
from .models import Faq, Event

admin.site.register(Book)
admin.site.register(Post)
admin.site.register(Faq)
admin.site.register(Event)