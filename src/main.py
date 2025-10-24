import asyncio, logging
from fastapi import FastAPI
from src.api import router
from src.consumer import consumer_loop
from src.dedup_store import DedupStore

app = FastAPI(title="UTS Aggregator")
app.include_router(router)

if not hasattr(app.state, "queue"):
    app.state.queue = asyncio.Queue()

if not hasattr(app.state, "dedup_store"):
    app.state.dedup_store = DedupStore("dedup_store.db")

@app.on_event("startup")
async def startup_event():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )   
    app.state.queue = asyncio.Queue()
    app.state.dedup_store = DedupStore("dedup_store.db")
    await app.state.dedup_store.init()
    asyncio.create_task(consumer_loop(app.state.queue, app.state.dedup_store))

@app.middleware("http")
async def inject_queue(request, call_next):
    if "state" not in request.scope:
        request.scope["state"] = {}
    request.scope["state"]["queue"] = app.state.queue
    response = await call_next(request)
    return response

@app.get("/")
def root():
    return {"message": "Aggregator running"}
