from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import HomePageView, AboutPageView, item_identify, ImportItemListPageView, parse_item_file, item_identify_save, item_skip

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("item_skip/", login_required(item_skip), name="item_skip"),
    path("item_identify/", login_required(item_identify),
         name="item_identify"),
    path("item_identify/save",
         login_required(item_identify_save),
         name="item_identify_save"),
    path("import_item_list/",
         login_required(ImportItemListPageView.as_view()),
         name="import_item_list"),
    path("parse_item_file",
         login_required(parse_item_file),
         name='parse_item_file'),
    path("about/", AboutPageView.as_view(), name="about"),
]
