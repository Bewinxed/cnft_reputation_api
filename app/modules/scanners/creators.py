from models.helius.transactions.EnrichedTransaction import TokenBalanceChange
from modules.scanners.base_scanner import Scanner


class CreatorReputation(Scanner):
    creator: str
    balances: TokenBalanceChange
    transaction_history: list
    
    async def scan(self):
        