from fastapi.routing import APIRouter
from app.models.helius.DAS import GetAssetRequestParams, GetAssetResponse
from app.models.RPC import JsonRpcResponse
from app.utils.helius import helius_client


route = APIRouter(prefix='/das', tags=['das'])

@route.post('/get_asset', response_model=JsonRpcResponse[GetAssetResponse])
async def get_asset_post(args: GetAssetRequestParams):
    return await helius_client.get_asset(args)

# @route.get('/scan_asset', response_model=None)
# async def scan_asset_get(asset_id: str):
#     return helius_client.scan_asset(asset_id)