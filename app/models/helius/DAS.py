from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict

from app.models.root_classes import to_lower_camel
from app.models.RPC import JsonRpcRequest
from app.models.helius.common.grouping import Grouping

class MetadataAttributesItem(BaseModel):
    trait_type: str
    value: Optional[str] = None

class Metadata(BaseModel):
    attributes: List[MetadataAttributesItem]
    description: str
    name: str
    symbol: str

class Links(BaseModel):
    image: Optional[str]
    external_url: str

class GetAssetRequestParamsDisplayOptions(BaseModel):
    model_config = ConfigDict(alias_generator=to_lower_camel)

    show_unverified_collections: bool = True
    show_collection_metadata: bool = True
    show_fungible: bool = True
    show_inscription: bool = True

class GetAssetRequestParams(BaseModel):
    model_config = ConfigDict(alias_generator=to_lower_camel)

    id: str
    display_options: Optional[GetAssetRequestParamsDisplayOptions] = None

class GetAssetRequest(JsonRpcRequest[GetAssetRequestParams]):
    pass

class File(BaseModel):
    uri: str
    cdn_uri: Optional[str] = None
    mime: Optional[str]

class Content(BaseModel):
    schema: str = Field(alias='$schema')
    json_uri: str
    files: List[Dict] = Field(default_factory=list)
    items: Optional[Dict] = None
    metadata: Metadata
    links: Links

class Authorities(BaseModel):
    address: str
    scopes: List[str]

class Compression(BaseModel):
    eligible: bool
    compressed: bool
    data_hash: str
    creator_hash: str
    asset_hash: str
    tree: str
    seq: int
    leaf_id: int

class Royalty(BaseModel):
    royalty_model: str
    target: Optional[str]
    percent: float
    basis_points: int
    primary_sale_happened: bool
    locked: bool

class Creators(BaseModel):
    address: str
    share: int
    verified: bool

class Ownership(BaseModel):
    frozen: bool
    delegated: bool
    delegate: Optional[str]
    ownership_model: str
    owner: str
    supply: Optional[int] = None
    mutable: Optional[bool] = False
    burnt: Optional[bool] = False

class ConfidentialTransferMint(BaseModel):
    authority: str
    auto_approve_new_accounts: bool
    auditor_elgamal_pubkey: str

class ConfidentialTransferFeeConfig(BaseModel):
    authority: str
    withdraw_withheld_authority_elgamal_pubkey: str
    harvest_to_mint_enabled: bool
    withheld_amount: str

class TransferFeeConfigOlder(BaseModel):
    epoch: str
    maximum_fee: str
    transfer_fee_basis_points: str

class TransferFeeConfigNewer(BaseModel):
    epoch: str

class TransferFeeConfig(BaseModel):
    transfer_fee_config_authority: str
    withdraw_withheld_authority: str
    withheld_amount: int
    older_transfer_fee: TransferFeeConfigOlder
    newer_transfer_fee: TransferFeeConfigNewer

class MetadataPointer(BaseModel):
    authority: str
    metadata_address: str

class MintCloseAuthority(BaseModel):
    close_authority: str

class PermanentDelegate(BaseModel):
    delegate: str

class TransferHook(BaseModel):
    authority: str
    program_id: str

class InterestBearingConfig(BaseModel):
    rate_authority: str
    initialization_timestamp: int
    pre_update_average_rate: int
    last_update_timestamp: int
    current_rate: int

class ConfidentialTransferAccount(BaseModel):
    approved: bool
    elgamal_pubkey: str
    pending_balance_lo: str
    pending_balance_hi: str
    available_balance: str
    decryptable_available_balance: str
    allow_confidential_credits: bool
    allow_non_confidential_credits: bool
    pending_balance_credit_counter: int
    maximum_pending_balance_credit_counter: int
    expected_pending_balance_credit_counter: int
    actual_pending_balance_credit_counter: int

class MetadataMintExtensions(BaseModel):
    update_authority: str
    mint: str
    name: str
    symbol: str
    uri: str
    additional_metadata: List[Dict[str, str]]

class MintExtensions(BaseModel):
    confidential_transfer_mint: ConfidentialTransferMint
    confidential_transfer_fee_config: ConfidentialTransferFeeConfig
    transfer_fee_config: TransferFeeConfig
    metadata_pointer: MetadataPointer
    mint_close_authority: MintCloseAuthority
    permanent_delegate: PermanentDelegate
    transfer_hook: TransferHook
    interest_bearing_config: InterestBearingConfig
    default_account_state: str
    confidential_transfer_account: ConfidentialTransferAccount
    metadata: MetadataMintExtensions

class PriceInfo(BaseModel):
    price_per_token: int
    currency: str

class TokenInfo(BaseModel):
    symbol: Optional[str] = None
    supply: int
    decimals: int
    token_program: str
    price_info: Optional[PriceInfo] = None

class Inscription(BaseModel):
    order: int
    size: int
    contentType: str
    encoding: str
    validationHash: str
    inscriptionDataAccount: str
    authority: str

class Spl20(BaseModel):
    p: str
    op: str
    tick: str
    amit: int

class GetAssetResponse(BaseModel):
    interface: str
    id: str
    content: Content
    authorities: list[Authorities]
    compression: Compression
    grouping: list[Grouping]
    royalty: Royalty
    creators: list[Creators]
    ownership: Ownership
    mint_extensions: Optional[MintExtensions] = None
    token_info: TokenInfo
    inscription: Optional[Inscription]
    spl20: Optional[Spl20]
