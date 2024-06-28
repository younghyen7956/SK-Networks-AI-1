from account.repository.account_repository_impl import AccountRepositoryImpl

from cart.repository.cart_item_repository_impl import CartItemRepositoryImpl
from cart.repository.cart_repository_impl import CartRepositoryImpl
from cart.service.cart_service import CartService
from product.repository.product_repository_impl import ProductRepositoryImpl


class CartServiceImpl(CartService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
            cls.__instance.__cartRepository = CartRepositoryImpl.getInstance()
            cls.__instance.__productRepository = ProductRepositoryImpl.getInstance()
            cls.__instance.__cartItemRepository = CartItemRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def cartRegister(self, cartData, accountId):
        account = self.__accountRepository.findById(accountId) # 사용자 계정을 찾는다.
        cart = self.__cartRepository.findByAccount(account)

        if cart is None: # 사용자 계정과 관련하여 cart가 존재하는지 찾는다
            print("장바구니 새롭게 생성")
            cart = self.__cartRepository.register(account) # 존재하지 않는다면 새로 cart를 생성한다.

        print("기존 장바구니 사용")

        productId = cartData.get('productId')
        cartItemList = self.__cartItemRepository.findAllByProductId(productId)

        cartItem = None
        for item in cartItemList:
            cartFromCartItem = item.cart
            accountFromCart = cartFromCartItem.account
            if accountFromCart.id == account.id:
                cartItem = item
                break

        if cartItem is None:
            print("신규 상품 추가")
            product = self.__productRepository.findByProductId(productId)
            self.__cartItemRepository.register(cartData, cart, product)
        else:
            print("기존 상품 추가")

            cartItem.quantity += 1
            self.__cartItemRepository.update(cartItem)

    def cartList(self, accountId):
        account = self.__accountRepository.findById(accountId)
        cart = self.__cartRepository.findByAccount(account)
        print(f"cartList -> cart: {cart}")
        cartItemList = self.__cartItemRepository.findByCart(cart)
        print(f"cartList -> cartItemList: {cartItemList}")
        cartItemListResponseForm = []

        for cartItem in cartItemList:
            cartItemResponseForm = {
                'cartItemId': cartItem.cartItemId,
                'productName': cartItem.product.productName,
                'productPrice': cartItem.product.productPrice,
                'productId': cartItem.product.productId,
                'quantity': cartItem.quantity
            }
            cartItemListResponseForm.append(cartItemResponseForm)

        return cartItemListResponseForm
        # form을 따로 안만들었을 때 이렇게 지저분한 코드가 만들어진다.





