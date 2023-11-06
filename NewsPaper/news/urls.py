from django.urls import path
from .views import PostsList, PostDetail, PostSearch, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate, \
   NewsDelete, ArticlesDelete
from appointments.views import AppointmentView, CategoryList, subscribe

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail' ),
   path('search/', PostSearch.as_view()),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('create/', ArticlesCreate.as_view(), name='articles_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('appointment/', AppointmentView.as_view(), name='make_appointment'),
   path('category/<int:pk>/', CategoryList.as_view(), name='category'),
   path('category/<int:pk>/subscribe/', subscribe, name='subscribe'),


]