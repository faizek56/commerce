from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('creat',views.creat,name="creat"),
    path("displayC",views.displayC,name="displayC"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("addwatchlist/<int:id>",views.addwatchlist,name="addwatchlist"),
    path("removewatchlist/<int:id>",views.removewatchlist,name="removewatchlist"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("addcomment/<int:id>",views.addcomment,name="addcomment"),
    path("addbid/<int:id>",views.addbid,name="addbid"),
    path("closeAuction/<int:id>",views.closeAuction,name="closeAuction"),
] 
