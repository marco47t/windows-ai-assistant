"""Long-term memory system using vector database."""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from core.logger import logger
from core.config import settings


class MemoryStore:
    """Simple file-based memory store (will upgrade to vector DB later)."""
    
    def __init__(self, memory_file: str = "data/memory.json"):
        """Initialize memory store.
        
        Args:
            memory_file: Path to memory file
        """
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(exist_ok=True)
        self.memories: List[Dict] = []
        self._load()
    
    def _load(self):
        """Load memories from file."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memories = json.load(f)
                logger.info(f"Loaded {len(self.memories)} memories")
            except Exception as e:
                logger.error(f"Error loading memories: {e}")
                self.memories = []
        else:
            self.memories = []
    
    def _save(self):
        """Save memories to file."""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memories, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.memories)} memories")
        except Exception as e:
            logger.error(f"Error saving memories: {e}")
    
    def add_memory(
        self,
        content: str,
        memory_type: str = "fact",
        tags: List[str] = None,
        metadata: Dict = None
    ) -> Dict:
        """Add a memory.
        
        Args:
            content: Memory content
            memory_type: Type (fact, preference, conversation, etc.)
            tags: List of tags
            metadata: Additional metadata
            
        Returns:
            The created memory
        """
        memory = {
            "id": len(self.memories) + 1,
            "content": content,
            "type": memory_type,
            "tags": tags or [],
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "accessed_count": 0,
            "last_accessed": None
        }
        
        self.memories.append(memory)
        self._save()
        logger.info(f"Added memory: {content[:50]}...")
        
        return memory
    
    def search_memories(
        self,
        query: str,
        memory_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 5
    ) -> List[Dict]:
        """Search memories (simple keyword search for now).
        
        Args:
            query: Search query
            memory_type: Filter by type
            tags: Filter by tags
            limit: Maximum results
            
        Returns:
            List of matching memories
        """
        query_lower = query.lower()
        results = []
        
        for memory in self.memories:
            # Type filter
            if memory_type and memory["type"] != memory_type:
                continue
            
            # Tag filter
            if tags and not any(tag in memory["tags"] for tag in tags):
                continue
            
            # Keyword search
            if query_lower in memory["content"].lower():
                # Update access stats
                memory["accessed_count"] += 1
                memory["last_accessed"] = datetime.utcnow().isoformat()
                results.append(memory)
        
        # Sort by relevance (accessed count for now)
        results.sort(key=lambda x: x["accessed_count"], reverse=True)
        
        self._save()
        return results[:limit]
    
    def get_recent_memories(self, limit: int = 10) -> List[Dict]:
        """Get most recent memories.
        
        Args:
            limit: Maximum results
            
        Returns:
            List of recent memories
        """
        sorted_memories = sorted(
            self.memories,
            key=lambda x: x["created_at"],
            reverse=True
        )
        return sorted_memories[:limit]
    
    def delete_memory(self, memory_id: int) -> bool:
        """Delete a memory.
        
        Args:
            memory_id: Memory ID
            
        Returns:
            True if deleted
        """
        original_count = len(self.memories)
        self.memories = [m for m in self.memories if m["id"] != memory_id]
        
        if len(self.memories) < original_count:
            self._save()
            logger.info(f"Deleted memory {memory_id}")
            return True
        
        return False
    
    def get_memory_stats(self) -> Dict:
        """Get memory statistics.
        
        Returns:
            Statistics dict
        """
        types = {}
        for memory in self.memories:
            memory_type = memory["type"]
            types[memory_type] = types.get(memory_type, 0) + 1
        
        return {
            "total": len(self.memories),
            "by_type": types,
            "most_accessed": sorted(
                self.memories,
                key=lambda x: x["accessed_count"],
                reverse=True
            )[:5]
        }


# Global memory store
memory_store = MemoryStore()
