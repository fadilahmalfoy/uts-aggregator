import asyncio, logging, json
from src.metrics import metrics

async def consumer_loop(queue, dedup_store):
    while True:
        event = await queue.get()
        metrics.received += 1
        metrics.topics.add(event.topic)

        is_new = await dedup_store.mark_processed(event.topic, event.event_id)
        if is_new:
            metrics.unique_processed += 1
            logging.info(f"Processed: {event.topic}/{event.event_id}")
        else:
            metrics.duplicate_dropped += 1
            logging.warning(f"Duplicate dropped: {event.topic}/{event.event_id}")
        queue.task_done()
