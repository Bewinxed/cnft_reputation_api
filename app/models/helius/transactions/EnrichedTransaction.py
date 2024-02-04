from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.models.helius.enums.sale_type import SaleType

from app.models.helius.transactions.transaction_source import TransactionSource
from app.models.helius.transactions.transaction_type import TransactionType
from app.models.helius.enums.commitment import Commitment
from app.models.root_classes import to_lower_camel
from app.models.helius.transactions.instructions import Instruction


class EnrichedTransactionHistoryRequestParams(BaseModel):
    before: Optional[str] = None
    until: Optional[str] = None
    commitment: Optional[Commitment] = None
    source: Optional[str] = None
    type: Optional[str] = None


class RawTokenAmount(BaseModel):
    token_amount: Optional[str] = None
    decimals: Optional[int] = None


class TokenBalanceChange(BaseModel):
    user_account: Optional[str] = None
    token_account: Optional[str] = None
    mint: Optional[str] = None
    raw_token_amount: Optional["RawTokenAmount"] = None


class AccountData(BaseModel):
    account: Optional[str] = None
    native_balance_change: Optional[float] = None
    token_balance_changes: Optional[List["TokenBalanceChange"]] = None


class NativeTransfer(BaseModel):
    from_user_account: Optional[str] = None
    to_user_account: Optional[str] = None
    amount: Optional[int] = None


class TokenTransfer(BaseModel):
    from_user_account: Optional[str] = None
    to_user_account: Optional[str] = None
    from_token_account: Optional[str] = None
    to_token_account: Optional[str] = None
    token_amount: Optional[float] = None
    mint: Optional[str] = None


class TokenStandard(Enum):
    NONFUNGIBLE = "NonFungible"
    FUNGIBLEASSET = "FungibleAsset"
    FUNGIBLE = "Fungible"
    NONFUNGIBLEEDITION = "NonFungibleEdition"
    UNKNOWN = "UnknownStandard"
    PROGRAMMABLENONFUNGIBLE = "ProgrammableNonFungible"

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)


class Token(BaseModel):
    """
    Attributes:
        mint (Optional[Unset, str]): The mint account of the token. Example: DsfCsbbPH77p6yeLS1i4ag9UA5gP9xWSvdCx72FJjLsx.
        token_standard (Optional[Unset, TokenStandard]):
    """

    mint: Optional[str] = None
    token_standard: Optional[str] = None


class NFTEvent(BaseModel):
    description: Optional[str] = None
    type: Optional[TransactionType] = None
    source: Optional[TransactionSource] = None
    amount: Optional[int] = None
    fee: Optional[int] = None
    fee_payer: Optional[str] = None
    signature: Optional[str] = None
    slot: Optional[int] = None
    timestamp: Optional[int] = None
    sale_type: Optional[SaleType] = None
    buyer: Optional[str] = None
    seller: Optional[str] = None
    staker: Optional[str] = None
    nfts: Optional[List["Token"]] = None


class ProgramInfo(BaseModel):
    """
    Attributes:
        source (Optional[str]):  Example: ORCANone
        account (Optional[str]): The account of the program Example: whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCcNone
        program_name (Optional[str]): The name of the program Example: ORCA_WHIRLPOOLSNone
        instruction_name (Optional[str]): The name of the instruction creating this swap. It is the value None
            instruction name from the Anchor IDL, if it is available. Example: whirlpoolSwap.
    """

    source: Optional[TransactionSource] = None
    account: Optional[str] = None
    program_name: Optional[str] = None
    instruction_name: Optional[str] = None


class NativeBalanceChange(BaseModel):
    account: Optional[str] = None
    amount: Optional[str] = None


class TokenSwap(BaseModel):
    token_inputs: Optional[List["TokenTransfer"]] = None
    token_outputs: Optional[List["TokenTransfer"]] = None
    token_fees: Optional[List["TokenTransfer"]] = None
    native_fees: Optional[List["NativeTransfer"]] = None
    program_info: Optional["ProgramInfo"] = None


class SwapEvent(BaseModel):
    """
    Attributes:
        native_input (Optional[NativeBalanceChangeNone
        native_output (Optional[NativeBalanceChangeNone
        token_inputs (Optional[List['TokenBalanceChange']]): The token inputs to the swapNone
        token_outputs (Optional[List['TokenBalanceChange']]): The token outputs of the swapNone
        token_fees (Optional[List['TokenBalanceChange']]): The token fees paid by an accountNone
        native_fees (Optional[List['NativeBalanceChange']]): The native fees paid by an accountNone
        inner_swaps (Optional[List['TokenSwap']]): The inner swaps occuring to make this swap happen. Eg. a swap None
            wSOL <-> USDC may be make of multiple swaps from wSOL <-> DUST, DUST <-> USDC
    """

    native_input: Optional["NativeBalanceChange"] = None
    native_output: Optional["NativeBalanceChange"] = None
    token_inputs: Optional[List["TokenBalanceChange"]] = None
    token_outputs: Optional[List["TokenBalanceChange"]] = None
    token_fees: Optional[List["TokenBalanceChange"]] = None
    native_fees: Optional[List["NativeBalanceChange"]] = None
    inner_swaps: Optional[List["TokenSwap"]] = None


class EnrichedTransactionEvents(BaseModel):
    nft: Optional["NFTEvent"] = None
    swap: Optional["SwapEvent"] = None


class EnrichedTransaction(BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=to_lower_camel)
    instructions: Optional[List[Instruction]] = None
    description: Optional[str] = None
    type: Optional[TransactionType] = None
    source: Optional[TransactionSource] = None
    fee: Optional[int] = None
    fee_payer: Optional[str] = None
    signature: str = ""
    slot: Optional[int] = None
    timestamp: Optional[int] = None
    native_transfers: Optional[List["NativeTransfer"]] = None
    token_transfers: Optional[List["TokenTransfer"]] = None
    account_data: Optional[List["AccountData"]] = None
    events: Optional["EnrichedTransactionEvents"] = None
    transaction_error: Optional[str] = None
