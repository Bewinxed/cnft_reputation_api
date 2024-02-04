
from fastapi import FastAPI
from app.utils.helius import HeliusClient
from app.routes import das
import uvicorn

helius_client = HeliusClient()
app = FastAPI()
app.include_router(das.route)

@app.get('/')
def read_root():
    return {'Hello': 'World'}

# if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=3000)
    
helius_client.enriched_transaction_history(address="D29ujqwLnWony5RpKm811GrWYf8G9xpTJBami6GKFyYd")