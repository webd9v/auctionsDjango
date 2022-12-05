from django.urls import path
from . import views

app_name="auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing",views.addListing,name="add_listing"),
    path("<int:id>",views.displayListing,name="listing"),
    path("add_comment",views.addComment,name="add_comment"),
    path("add_bid",views.addBid,name="add_bid"),
    path("watchlist",views.displayWatchList,name="watchlist"),
    path("categories",views.displayItemsByCategory,name="category"),
    path("addToWatchList/<int:item_id>",views.toggleItemInWatchlist,name="watch_item"),
]
