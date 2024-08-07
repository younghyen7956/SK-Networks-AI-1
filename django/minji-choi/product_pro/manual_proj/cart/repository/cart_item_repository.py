from abc import ABC, abstractmethod

class CartItemRepository(ABC):

    @abstractmethod
    def register(self, cartData, cart, product):
         pass
    @abstractmethod
    def findByProductId(self, productId):
        pass
    @abstractmethod
    def findAllByProduct(self, product):
        pass
    @abstractmethod
    def findByCart(self, cart):
        pass
    @abstractmethod
    def update(self, cartItem):
        pass
    @abstractmethod
    def findById(self, id):
        pass
