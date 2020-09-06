from django.urls import path
from myapp.views import HomeView, FaqView, EventView
from . import views

homeView = HomeView()
faq = FaqView()
event = EventView()

urlpatterns= [
    path('', HomeView.as_view()),
    path('faq', FaqView.as_view()),
    path('event', EventView.as_view()),
    path('view/<str:post_name>', views.ViewData, name = 'view_data'),
    path('book/<int:book_id>', views.book_by_id, name = 'book_by_id'),
    path('webhook', views.webhook_endpoint),
]