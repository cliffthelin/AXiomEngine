#!/usr/bin/env python3
from typing import List, Dict, Optional, Any, Union, Literal
from pydantic import BaseModel, Field
import time
import uuid

# --- Message Types ---

class AgentMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None
    role: str
    content: str
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None # For tool results

# --- Event Types ---

class AgentLoopEvent(BaseModel):
    type: str
    message: Optional[AgentMessage] = None
    delta: Optional[str] = None
    thinking: Optional[str] = None
    # Tool execution
    tool_call_id: Optional[str] = None
    tool_name: Optional[str] = None
    args: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    is_error: Optional[bool] = None
    # Queue updates
    steering: Optional[List[str]] = None
    follow_up: Optional[List[str]] = None
    # Compaction / Retry
    reason: Optional[str] = None
    attempt: Optional[int] = None
    max_attempts: Optional[int] = None
    # General data
    content: Optional[Any] = None
    error: Optional[str] = None
    messages: Optional[List[AgentMessage]] = None

# --- State & Config ---

ThinkingLevel = Literal["off", "minimal", "low", "medium", "high", "xhigh"]

THINKING_BUDGETS = {
    "minimal": 128,
    "low": 512,
    "medium": 1024,
    "high": 2048,
    "xhigh": 4096
}

class AgentState(BaseModel):
    system_prompt: str = ""
    model: str = "qwen3.6"
    thinking_level: ThinkingLevel = "low"
    messages: List[AgentMessage] = Field(default_factory=list)
    is_streaming: bool = False
    pending_tool_calls: List[str] = Field(default_factory=list)
    error_message: Optional[str] = None
    session_id: str = "default_session"

class AgentTool(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] # JSON Schema
    execution_mode: Literal["parallel", "sequential"] = "parallel"
    label: Optional[str] = None

class CompactionDetails(BaseModel):
    read_files: List[str] = Field(default_factory=list)
    modified_files: List[str] = Field(default_factory=list)

class CompactionEntry(BaseModel):
    type: Literal["compaction"] = "compaction"
    id: str
    parent_id: str
    timestamp: float = Field(default_factory=time.time)
    summary: str
    first_kept_entry_id: str
    tokens_before: int
    details: CompactionDetails = Field(default_factory=CompactionDetails)

class BranchSummaryEntry(BaseModel):
    type: Literal["branch_summary"] = "branch_summary"
    id: str
    parent_id: str
    timestamp: float = Field(default_factory=time.time)
    summary: str
    from_id: str
    details: CompactionDetails = Field(default_factory=CompactionDetails)

class AgentLoopConfig(BaseModel):
    tool_execution: Literal["parallel", "sequential"] = "parallel"
    steering_mode: Literal["one-at-a-time", "all"] = "one-at-a-time"
    follow_up_mode: Literal["one-at-a-time", "all"] = "one-at-a-time"
    should_stop_after_turn: Optional[bool] = False
    
    # Compaction settings
    compaction_enabled: bool = True
    reserve_tokens: int = 16384
    keep_recent_tokens: int = 20000
