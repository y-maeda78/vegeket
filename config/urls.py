"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.IndexListViews.as_view()),       # トップページ

    # admin
    path('admin/', admin.site.urls),  

    # Account
    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),          # ただログアウトさせるだけなのでDjangoの標準機能を実装し、viewsの指定はなし
    path('signup/', views.SignUpView.as_view()),
    path('account/', views.AccountUpdateView.as_view()),
    path('profile/', views.ProfileUpdateView.as_view()),

    # Items
    path('items/<str:pk>/', views.ItemDetailView.as_view()),    # 商品詳細ページ

    # Cart
    path('cart/', views.CartListView.as_view()),    # カートページ
    path('cart/add/', views.AddCartView.as_view()), # カートに追加する
    path('cart/update/', views.UpdateCartView.as_view()), # カートを更新する
    path('cart/remove/<str:pk>/', views.remove_from_cart), # カート内の商品削除 (関数ビューなので.as_view()不要)

    # Pay
    path('pay/checkout/', views.PayWithStripe.as_view()),   # 決済ページへリダイレクトする
    path('pay/success/', views.PaySuccessView.as_view()),   # 決済成功ページへ移動する
    path('pay/cancel/', views.PayCancelView.as_view()),     # 決済失敗ページへ移動する

    # Order
    path('orders/<str:pk>/', views.OrderDetailView.as_view()),
    path('orders/', views.OrderIndexView.as_view()),
]
