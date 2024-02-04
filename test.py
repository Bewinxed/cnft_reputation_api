
import asyncio
from app.utils.helius import helius_client
from app.models.helius.assets.balances import GetAssetsByOwnerRequestParams

async def main():
    await helius_client.get_assets_by_owner(GetAssetsByOwnerRequestParams.model_construct(owner_address="33n3LYYPsSwuLX9grTXGw7xWhJ1nBCsBg4y35QSABVa9", page=1, limit=10))
    
if __name__ == '__main__':
    asyncio.run(main())