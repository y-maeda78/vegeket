from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.conf import settings
# from stripe.api_resources import tax_rate
from base.models import Item
import stripe

stripe.api_key = settings.STRIPE_API_SECRET_KEY

# 決済完了の場合の処理
class PaySuccessView(TemplateView):
  template_name = 'pages/success.html'

  # 最新のOrderオブジェクトを取得し、注文確定に変更
  def get(self, request, *args, **kwargs):
    # 購入済みなのでカート情報を削除する
    del request.session['cart']
    return super().get(request, *args, **kwargs)


# 処理がうまくいかなかった場合の処理
class PayCancelView(TemplateView):
  template_name = 'pages/cancel.html'
  # 最新のOrderオブジェクトを取得
  def get(self, request, *args, **kwargs):
      
    # 在庫数と販売数を元の状態に戻す
    # is_confirmedがFalseであれば削除（仮オーダー削除）

    return super().get(request, *args, **kwargs)


# 消費税と通貨（円）の設定
tax_rate = stripe.TaxRate.create(
    display_name='消費税',
    description='消費税',
    country='JP',
    jurisdiction='JP',
    percentage=settings.TAX_RATE * 100,
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)

def create_line_item(unit_amount, name, quantity):
  return {
    'price_data': {
      'currency': 'JPY',
      'unit_amount': unit_amount,
      'product_data': {'name': name, }
    },
    'quantity': quantity,
    'tax_rates': [tax_rate.id]
  }
 
 

# カートに入れた商品の代金を支払う処理
# Stripeの用意した安全な支払い画面へユーザーを自動的に移動（リダイレクト）させる
class PayWithStripe(View):

  def post(self, request, *args, **kwargs):
    cart = request.session.get('cart', None)
    if cart is None or len(cart) == 0:
      return redirect('/')

    line_items = []     # Stripeに渡すための空のリストを準備
    for item_pk, quantity in cart['items'].items():     # カートに入っている全ての商品を一つずつ取り出す
      item = Item.objects.get(pk=item_pk)               # データベースから商品の詳細（名前や価格）を取得
      line_item = create_line_item(                     # 定義した関数を使って、Stripeが読み取れる形式の商品情報を作成
          item.price, item.name, quantity)
      line_items.append(line_item)                      # 作成した商品情報をリストに追加

    checkout_session = stripe.checkout.Session.create(
      # customer_email=request.user.email,
      payment_method_types=['paypay', 'card', 'konbini'],   # 支払方法の指定（'konbini','paypay'など）
      line_items=line_items,                            # 左側の line_items はStripeの設定項目名、右側の line_items はfor文で作成した商品リストの変数
      mode='payment',
      success_url=f'{settings.MY_URL}/pay/success/',    # 決済が成功したときに戻すurl
      cancel_url=f'{settings.MY_URL}/pay/cancel/',      # 決済に失敗したときに戻すurl
    )
    return redirect(checkout_session.url)               # Stripeが作った決済セッションのページへのURL
