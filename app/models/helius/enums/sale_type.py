from enum import Enum


class SaleType(str, Enum):
    auction = 'AUCTION'
    instant_sale = 'INSTANT_SALE'
    offer = 'OFFER'
    global_offer = 'GLOBAL_OFFER'
    mint = 'MINT'
    unknown = 'UNKNOWN'
    
    @classmethod
    def _missing_(cls, number):
        return cls(cls.unknown)