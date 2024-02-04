# import HELIUS_API_KEY from local env
import os
from dotenv import load_dotenv

load_dotenv()

HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
HELIUS_RPC = os.getenv("HELIUS_RPC")