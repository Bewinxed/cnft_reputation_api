# from __future__ import annotations

from fastapi import HTTPException
from pydantic import BaseModel
from app.constants import HELIUS_API_KEY, HELIUS_RPC

from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_incrementing
import httpx
from typing import Literal, Optional, Type, TypeVar

from app.models.helius.DAS import GetAssetRequest, GetAssetRequestParams, GetAssetResponse
from app.models.RPC import JsonRpcResponse, PaginatedItems
from app.models.helius.assets.balances import GetAssetsByOwnerRequest, GetAssetsByOwnerRequestParams
from app.models.helius.transactions.EnrichedTransaction import Commitment, EnrichedTransaction

T = TypeVar("T", bound=BaseModel)

class HeliusClient(httpx.AsyncClient):
    api_key: Optional[str]

    def __init__(
        self,
        *,
        api_key: Optional[str] = HELIUS_API_KEY,
        verify: bool = False,
        follow_redirects: bool = True,
        base_url: Literal["https://api.helius.xyz/v0/"] = "https://api.helius.xyz/v0/",
        timeout: httpx.Timeout = httpx.Timeout(10.0, connect=10.0, read=10.0),
    ):
        super().__init__(
            # headers={'api-key': api_key},
            headers={"Authorization": f"Bearer {api_key}"},
            # params={"api-key": api_key},
            verify=verify,
            follow_redirects=follow_redirects,
            base_url=base_url,
            timeout=timeout,
        )
        self.api_key = api_key

    @classmethod
    def get_client(cls, api_key: Optional[str] = None) -> "HeliusClient":
        # put the client in globals
        
        return cls(api_key=api_key)

    def __call__(self, *args, **kwargs):
        return self.call_and_parse(*args, **kwargs)


    @retry(
        stop=stop_after_attempt(3),
        wait=wait_incrementing(1, 1, 1),
        reraise=True,
    )
    async def call_and_parse[T: BaseModel](
        self,
        url: str,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        parser: Type[T],
        json={},
        **kwargs,
    ) -> JsonRpcResponse[T]:
        response = await self.request(
            method=method,
            url=url,
            json=json,
            # headers={"content-type": "application/json"},
            params={k: v for k, v in kwargs.items() if v} | {"api-key": self.api_key},
        )
        if response.status_code == 200 and parser:
            result = response.json()
            res = JsonRpcResponse[T].model_validate(result if isinstance(result, dict) else {"items": [parser.model_validate(r) for r in result]})
            if res.error:
                raise HTTPException(status_code=res.error.code, detail=res.error.model_dump(exclude={"code"}))
            return res
        response.raise_for_status()
        raise httpx.HTTPError(message=response.text)

    async def get_asset(self, args: GetAssetRequestParams):
        return await self.call_and_parse(
            url=f"{HELIUS_RPC}?api-key={self.api_key}",
            method="POST",
            parser=GetAssetResponse,
            json=GetAssetRequest(method="getAssetsByOwner", params=args).model_dump(by_alias=True),
        )
        
    async def get_assets_by_owner(self, args: GetAssetsByOwnerRequestParams):
        all_assets = []
        assets = []
        before = args.before or ""
        while True:
            if len(all_assets) < (args.limit or 0):
                assets = await self.call_and_parse(
                    f"{HELIUS_RPC}?api-key={self.api_key}",
                    method='POST',
                    parser=PaginatedItems[dict],
                    json=GetAssetsByOwnerRequest(params=args).model_dump(by_alias=True),
                )
                if assets.result:
                    all_assets.extend(assets.result)
                    before = assets.result[-1].signature
                    print(f'last signature {before}')
                else:
                    break
            else:
                break
        return all_assets[:args.limit]

    async def enriched_transaction_history(
        self,
        address: str,
        before: Optional[str] = None,
        until: Optional[str] = None,
        commitment: Optional[Commitment] = None,
        source: Optional[str] = None,
        type: Optional[str] = None,
        limit=100
    ) -> list[EnrichedTransaction]:
        all_txs = []
        txs = []
        before = before or ""
        while True:
            if len(all_txs) < limit:
                txs = await self.call_and_parse(
                    f"{self.base_url}addresses/{address}/transactions",
                    method='GET',
                    parser=EnrichedTransaction,
                    before=before,
                    until=until,
                    commitment=commitment,
                    source=source,
                    type=type,
                )
                if txs.result:
                    all_txs.extend(txs.result)
                    before = txs.result[-1].signature
                    print(f'last signature {before}')
                else:
                    break
            else:
                break
        return all_txs[:limit]

helius_client = HeliusClient(api_key=HELIUS_API_KEY)
