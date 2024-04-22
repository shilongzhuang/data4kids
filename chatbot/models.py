from dataclasses import dataclass, field
from typing import List, Dict, Any, Union


@dataclass
class Message:
    role: str
    content: Any
    content_type: str = None
