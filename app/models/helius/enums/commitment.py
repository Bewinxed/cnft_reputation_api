from enum import Enum


class Commitment(str, Enum):
    finalized = 'finalized'
    confirmed = 'confirmed'