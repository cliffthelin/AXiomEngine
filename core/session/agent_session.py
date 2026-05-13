import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AgentSession:
    """
    AXIOMENGINE SESSION LAYER
    Tracks persistent state for a single agentic workflow connection.
    """
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    connection_id: Optional[str] = None
    previous_response_id: Optional[str] = None
    
    # State Caches
    conversation_state_cache: List[Dict[str, Any]] = field(default_factory=list)
    tool_registry_cache: Dict[str, Any] = field(default_factory=dict)
    rendered_context_cache: Dict[str, Any] = field(default_factory=dict)
    model_routing_cache: Optional[str] = None
    safety_validation_cache: Dict[str, Any] = field(default_factory=dict)
    
    # Metrics
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    turn_count: int = 0

    def update_activity(self):
        self.last_active = datetime.now()
        self.turn_count += 1

    def invalidate_cache(self, reason: str):
        print(f"Session {self.session_id}: Cache invalidated due to {reason}")
        self.conversation_state_cache = []
        self.tool_registry_cache = {}
        self.rendered_context_cache = {}
        self.previous_response_id = None

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "connection_id": self.connection_id,
            "previous_response_id": self.previous_response_id,
            "turn_count": self.turn_count,
            "last_active": self.last_active.isoformat()
        }
