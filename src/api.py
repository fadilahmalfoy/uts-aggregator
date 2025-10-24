from fastapi import APIRouter, BackgroundTasks, Query, Request
from typing import List, Union
from src.models import Event, Stats
from src.metrics import metrics

router = APIRouter()

_events = []  # daftar event unik yang sudah diproses
_event_keys = set()

@router.get("/stats", response_model=Stats)
async def get_stats():
    uptime = metrics.uptime()
    if not isinstance(uptime, (int, float)):
        try:
            uptime = float(uptime)
        except:
            uptime = 0.0

    return {
        "received": metrics.received,
        "unique_processed": metrics.unique_processed,
        "duplicate_dropped": metrics.duplicate_dropped,
        "topics": list(metrics.topics),
        "uptime": metrics.uptime()
    }

@router.get("/events")
async def get_events(topic: str = Query(None)):
    if topic:
        return [e for e in _events if e["topic"] == topic]
    return _events

async def publish_to_queue(events, queue):
    for e in events:
        key = (e.topic, e.event_id)
        metrics.received += 1

        if key not in _event_keys:
            _event_keys.add(key)
            _events.append(e.dict())
            metrics.unique_processed += 1
            metrics.topics.add(e.topic)
            await queue.put(e)
        else:
            metrics.duplicate_dropped += 1

@router.post("/publish")
async def publish(events: Union[Event, List[Event]], background_tasks: BackgroundTasks, request: Request):
    queue = request.app.state.queue  
    if isinstance(events, Event):
        events = [events]
    background_tasks.add_task(publish_to_queue, events, queue)
    return {"accepted": len(events)}
