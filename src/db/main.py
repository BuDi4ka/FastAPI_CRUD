from sqlmodel import text
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import Config

engine = create_async_engine(Config.DATABASE_URL, echo=True)


async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'hello';")

        result = await conn.execute(statement)

        print(result.all())