from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.cart import Cart
from cart.serializers import ItemSSerializer

from orders.utils import fetch_delivery_price


class CartViewSet(viewsets.ViewSet):
    """
    ViewSet для корзины товаров.
    """

    @action(detail=False, methods=['get'])
    def cart(self, request):
        """
        Получаем информацию о корзине пользователя.
        """
        cart = Cart(request)
        return Response({'amount': cart.get_total_price() or 0})

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        """
        Добавляем товар в корзину.
        """
        serializer = ItemSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = dict(serializer.validated_data)
        cart = Cart(request)
        if cart.add_offer(**item) == -1:
            return Response({'error': 'limit'}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def update_cart(self, request):
        """
        Обновляем кол-во товара в корзине.
        """
        serializer = ItemSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = dict(serializer.validated_data)
        cart = Cart(request)
        if cart.add_offer(**item, update_quantity=True) == -1:
            return Response({'error': 'limit'}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove_from_cart(self, request):
        """
        Удаляем товар из корзины.
        """
        serializer = ItemSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = dict(serializer.validated_data)
        cart = Cart(request)
        cart.remove_offer(item['offer_id'])
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def clear_cart(self, request):
        """
        Очищаем корзину.
        """
        cart = Cart(request)
        cart.clear()
        return Response({'success': 'cart clear'})

    @action(detail=False, methods=['post'])
    def delivery_price(self, request):
        """
        Получаем цену доставки.
        """
        data = request.data
        cart = Cart(self.request)
        price = fetch_delivery_price(
            data.get('delivery_type'),
            '142200',
            data.get('zip_code'),
            cart.get_total_weight())
        return Response({'price': price}, status=status.HTTP_200_OK)
