import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from src.main import app

@pytest.mark.asyncio
async def test_uptime_field_exists():
    """Pastikan uptime bertambah setelah beberapa detik"""

    if hasattr(app, "startup_event"):
        await app.startup_event()
    else:
        # Jalankan semua handler startup yang terdaftar (untuk kompatibilitas FastAPI versi lama)
        for handler in app.router.on_startup or []:
            await handler()

    # Gunakan ASGITransport agar bisa test langsung tanpa server eksternal
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response1 = await client.get("/stats")
        assert response1.status_code == 200
        data1 = response1.json()
        assert "uptime" in data1

        uptime1 = data1["uptime"]

        # Tunggu 2 detik untuk memastikan uptime meningkat
        await asyncio.sleep(2)

        response2 = await client.get("/stats")
        data2 = response2.json()
        uptime2 = data2["uptime"]

        # Parsing aman (baik string "5s" atau angka 5.0)
        def parse(val):
            try:
                return float(val)
            except ValueError:
                return float(str(val).replace("s", ""))

        assert parse(uptime2) > parse(uptime1)
