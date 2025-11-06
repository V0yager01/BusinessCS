
from src.database.config import Base
import src.team.models
import src.user.models
import src.task.models

# async def main():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# if __name__ == "__main__":
#     asyncio.run(main())
