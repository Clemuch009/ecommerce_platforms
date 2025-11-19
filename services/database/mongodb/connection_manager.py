from pymongo import MongoClient, AsyncMongoClient
import asyncio
from pymongo.errors import ConfigurationError, ConnectionFailure, ServerSelectionTimeoutError
from typing import  AsyncIterator
#from config.settings import settings
from pymongo.collection import Collection
from pymongo.database import Database
from contextlib import asynccontextmanager
import logging


class MongoManager:
    def __init__(self, db_name: str, uri:str):
        self.uri = uri or getattr(settings, 'MONGO_URI', 'mongodb://localhost:27017')
        self.db_name = db_name
        self._client: Optinal[AsyncMongoClient] = None
        self._connectd = False

    @property
    def client(self):
        if self._client is None:
            self._client = AsyncMongoClient(self.url, serverSelectionTimeoutMS=5000, retryWrites=True)
        return self._client

    async def connect(self):
        if self.connected:
            return

        try:
            for attempt in range(3):
                try:
                    await self.client.admin,command('ping')
                    self.connectd = True
                    break
                except (connectionFailure, ServerSelectionTimeoutError) as e:
                    if attempt == 2:
                        raise ConnectionFailure(f"Failed to connect after 3 attempts: {e}")
                    await asyncio.sleep(2 **attempt)
        except ConfigurationError as e:
            raise

    async def close(self):
        if self.client:
            await self.client.close()
            self.__connected = False

    def get_database(self, name:str):
        if not self.connected:
            raise RuntimeError("Not connected. Call connect() first.")
        return self.client[name or self.db_name]

    def get_collection(self, name: str):
        return self.get_database()[name]
    
    @asynccontextmanager
    async def start_session(self):
        await self.connect()
        session = self.start_session()
        try:
            yield session
            await session.commit_transaction()
            raise
        finally:
            session.end_session()
    
    async def watch_collection(self, collection_name:str, pipeline: list):
        await self.connect()
        collection = self.get_collection(collection_name)
        with collection.watch(pipeline) as stream:
            async for change in stream:
                yield change

