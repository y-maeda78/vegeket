from django.shortcuts import render
from django.views.generic import ListView
from base.models import Item

class IndexListViews(ListView):
  model = Item
  template_name = 'pages/index.html'



"""
関数で書く場合
---


"""
"""
  render() について
  render = レンダリングの略でブラウザが表示できるHTMLを生成する
  例えば
  Pythonコードで用意した具体的な情報であるデータ（コンテキスト）「{'name': '太郎'}」を
  レンダリングしHTMLコード「<p>ユーザー名：太郎</p>」に変換することができる。

"""