# cnft_reputation_api

# In response to this tweet by [@0xMert](https://twitter.com/0xMert_/status/1753890669611917608)

# NFT Reputation API

I'm currently building out an API that can respond to a mint address with a "reputation" response that vendors can use to filter out spam.

**The idea is to provide the wallet providers with info about the cNFT**

**Response would contain something like:**
cNFT -> is a verified nft on tensor/magic eden?
cNFT Creator (list) -> are they known spammer wallet? activity? suspicious activity?
cNFT Metadata -> the api can scan the nft's image/metadata and browse to the website and check if there's any wallet draining code, and if so, that is also provided.

# Current Progress

[x] Scaffold Done
[x] Integration with Helius DAS Api
[~] Pydantic Models for different DAS API Response/Requests being written
[x] Write Scanners:
_ Scanner for creator transaction history.
_ Scanner for creator age.
_ Scanner for creator balances.
[x] Write Scoring Algo:
_ NFT Collection Reputation. \* NFT Creator Reputation.
[x] Add Endpoints for providers to call.
