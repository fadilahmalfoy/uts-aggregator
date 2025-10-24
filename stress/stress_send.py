# stress/stress_send.py
import asyncio
import httpx
import random
import time
from datetime import datetime

async def send_events(n=5000, dup_rate=0.2):
    async with httpx.AsyncClient() as client:
        # buat 80% event unik, 20% duplikat
        unique_ids = [f"id-{i}" for i in range(int(n * (1 - dup_rate)))]
        duplicates = random.choices(unique_ids, k=int(n * dup_rate))
        all_ids = unique_ids + duplicates
        random.shuffle(all_ids)

        start = time.time()
        sent = 0

        for eid in all_ids:
            event = {
                "topic": "stress",
                "event_id": eid,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "stress_test",
                "payload": {"number": eid}
            }
            # kirim event ke aggregator
            await client.post("http://localhost:8000/publish", json=event)
            sent += 1

        duration = round(time.time() - start, 2)
        print(f"Sent {sent} events in {duration} seconds.")

if __name__ == "__main__":
    asyncio.run(send_events())
