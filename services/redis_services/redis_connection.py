from redis.asyncio import Redis
import asyncio
import datetime
#from config import settings
from typing import Optional
from  redis.exceptions import ConnectionError as RedisConnectionError, AuthenticationError
import logging

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self, host='localhost', port=6379):
        self._client = None
        self._host = host 
        self._port = port
        self.connected = False
    
    async def get_client(self):
        if self._client is None:
            try:
                self._client = Redis(host= self._host, port=self._port, decode_responses=True)
                logger.debug(f"Redis client initialized for {self._host}:{self._port}")
            except Exception as e:
                logger.error(f"Failed to initialize Redis client: {e}")
                raise RedisConnectionError("Unable to create Redis client")
        return self._client

    async def get_connection(self):
        if self.connected:
            return True
        client = await self.get_client()
        try:
            for attempt in range(3):
                try:
                    await client.ping()
                    self.connected = True
                    logger.info(f"Connected to Redis at {self._host}:{self._port}")
                    return True
                except (RedisConnectionError, AuthenticationError) as e:
                    if attempt == 2:
                        logger.error(f"Failed to connect to Redis after 3 attempts: {e}")
                        raise RedisConnectionError(f"Redis server not accessible: {e}")
                    await asyncio.sleep(2 ** attempt)
        except Exception as e:
            logger.error(f"Unexpected error connecting to Redis: {e}")
            raise RedisConnectionError("Redis connection failed unexpectedly")

    async def close(self):
        if self._client:
            await self._client.aclose()
        self.connected = False
        logger.info(f"connection closed  at {datetime.datetime.now()}")
