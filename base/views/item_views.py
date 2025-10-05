from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Item

class IndexListViews(ListView):
  model = Item
  template_name = 'pages/index.html'


"""
関数で書く場合
---
def indexViews(request):
  object_list = Item.objects.all()
  # Webページに表示したいデータを用意
  context = {
    'object_list' : object_list,
  }
  # 'index.html'に、contextのデータをレンダリングして表示させる
  return render(request, 'pages/index.html', context)
"""
"""
  render() について
  render = レンダリングの略でブラウザが表示できるHTMLを生成する
  例えば
  Pythonコードで用意した具体的な情報であるデータ（コンテキスト）「{'name': '太郎'}」を
  レンダリングしHTMLコード「<p>ユーザー名：太郎</p>」に変換することができる。

"""

# 詳細ページ
class ItemDetailView(DetailView):
  model = Item
  template_name = 'pages/item.html'