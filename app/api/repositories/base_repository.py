from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import Base, get_db


class BaseRepository:

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def db_add(self, model: Base) -> None:
        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
        except SQLAlchemyError:
            await self.session.rollback()
        finally:
            await self.session.close()

    async def db_update(self, model: Base) -> None:
        try:
            await self.session.commit()
            await self.session.refresh(model)
        except SQLAlchemyError:
            await self.session.rollback()
        finally:
            await self.session.close()

    async def db_delete(self, model: Base) -> None:
        try:
            await self.session.delete(model)
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
        finally:
            await self.session.close()
