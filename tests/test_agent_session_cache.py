import unittest
import time
from core.session.agent_session import AgentSession
from core.cache.response_state_cache import ResponseStateCache

class TestAgentSessionCache(unittest.TestCase):
    def test_session_survival(self):
        cache = ResponseStateCache()
        session = cache.create_session("test_session")
        session.conversation_state_cache.append({"role": "user", "content": "Hello"})
        
        # Retrieve session
        retrieved = cache.get_session("test_session")
        self.assertIsNotNone(retrieved)
        self.assertEqual(len(retrieved.conversation_state_cache), 1)

    def test_session_expiration(self):
        # Create cache with 1 second TTL
        cache = ResponseStateCache(ttl_seconds=1)
        session = cache.create_session("expire_me")
        
        # Wait for expiration
        time.sleep(1.5)
        
        retrieved = cache.get_session("expire_me")
        self.assertIsNone(retrieved)

    def test_cache_invalidation(self):
        session = AgentSession(session_id="invalidate_test")
        session.conversation_state_cache = [{"role": "system", "content": "Init"}]
        
        session.invalidate_cache("Tool definitions changed")
        self.assertEqual(len(session.conversation_state_cache), 0)
        self.assertIsNone(session.previous_response_id)

if __name__ == "__main__":
    unittest.main()
