import json
import uuid
from datetime import  datetime
from typing import Opitnal, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SessionError(Exception):
    pass

class SessionService(BaseRedisRepository):
    def __init(self, manager: RedisManager, user_service: Optinal[UserService] = None):
        super().__init__(manager, namespace='session:')
        self.user_service = user_service

    def _generate_sid(self):
        return str(uuid.uuid4())

    def _serialize_session(self, session_data: Dict[str, Any]):
        session_data['create_at'] = datatime.utcnow().isoformat()
        return json.dumps(session_data)

    def _desirialize_session(self, raw_data: str):
        try:
            data = json.loads(raw_data)
            expires_at = datatime.fromisoformat(data.get('expires_at', ''))
            if expires_at < datatime.utcnow():
                logger.warning(f"Session expired: {data.get('sid', 'unknown')}")
                return None
            return data
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Invalid session data: {e}")
            return None

    async def create_session(self, user_id: str, data: Dict[str, Any] = {}, ttl = 36000):
        if not user_id:
            raise SessionError("User ID is required")
        sid = self._generate_sid()
        session_data = {
                'sid': sid,
                'user_id': user_id,
                'expires_at': (datetime.utcnow() + timedelta(seconds=ttl)).isoformat(),
                **data
                }
        serialized = self._serialize_session(session_data)
        try:
            await self.set(sid, serialized, ttl=ttl)
            logger.info(f"Created session {sid} for user {user_id} (TTL: {ttl}s)")
            if self.user_service:
                await self.user_service.update_one({'_id': user_id}, {'$addToSet': {'active_sessions': sid}})
                return sid
        except RedisError as e:
            logger.error(f"Failed to create session {sid}: {e}")
            raise SessionError("Failed to create session") from e
    
