import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
print("Using URL:", DATABASE_URL)


async def test():
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: None)
        print("✅ Connection OK")
    except Exception as e:
        print("❌ Connection failed:", e)


asyncio.run(test())
