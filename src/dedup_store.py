import aiosqlite, datetime

class DedupStore:
    def __init__(self, path="dedup_store.db"):
        self.path = path
        self.db = None

    async def init(self):
        self.db = await aiosqlite.connect(self.path)
        await self.db.execute("PRAGMA journal_mode=WAL;")
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS processed_events (
                topic TEXT,
                event_id TEXT,
                processed_at TEXT,
                PRIMARY KEY (topic, event_id)
            )
        """)
        await self.db.commit()

    async def mark_processed(self, topic, event_id):
        ts = datetime.datetime.utcnow().isoformat()
        try:
            await self.db.execute(
                "INSERT INTO processed_events VALUES (?, ?, ?)",
                (topic, event_id, ts)
            )
            await self.db.commit()
            return True  # baru pertama
        except aiosqlite.IntegrityError:
            return False  # duplikat