"""Multi-agent system with specialized AI agents."""

from typing import Dict, List, Optional, Any
from enum import Enum
from core.logger import logger
from services.router import AIRouter


class AgentRole(Enum):
    """Agent roles."""
    RESEARCHER = "researcher"
    CODER = "coder"
    PLANNER = "planner"
    CRITIC = "critic"
    EXECUTOR = "executor"


class Agent:
    """Individual AI agent with specialized role."""
    
    def __init__(self, role: AgentRole, router: AIRouter):
        """Initialize agent.
        
        Args:
            role: Agent role
            router: AI router
        """
        self.role = role
        self.router = router
        self.system_prompts = {
            AgentRole.RESEARCHER: """You are a research specialist. Your job is to:
- Search for information on the web
- Read and analyze multiple sources
- Extract key facts and insights
- Provide comprehensive research summaries with citations
- Identify knowledge gaps that need more research""",
            
            AgentRole.CODER: """You are a coding expert. Your job is to:
- Write clean, efficient Python code
- Debug and fix code errors
- Explain code functionality
- Suggest optimizations and best practices
- Generate code examples and solutions""",
            
            AgentRole.PLANNER: """You are a task planning specialist. Your job is to:
- Break down complex tasks into clear steps
- Create actionable plans
- Identify dependencies and prerequisites
- Estimate time and resources needed
- Prioritize tasks effectively""",
            
            AgentRole.CRITIC: """You are a quality critic. Your job is to:
- Review answers for accuracy and completeness
- Identify potential errors or inconsistencies
- Suggest improvements
- Verify facts and claims
- Ensure high-quality outputs""",
            
            AgentRole.EXECUTOR: """You are an execution specialist. Your job is to:
- Coordinate between other agents
- Execute plans step-by-step
- Track progress and results
- Handle errors and fallbacks
- Deliver final results to the user"""
        }
    
    def think(self, task: str, context: Optional[Dict] = None) -> str:
        """Agent thinks about a task.
        
        Args:
            task: Task description
            context: Optional context
            
        Returns:
            Agent's response
        """
        # Build messages with role-specific system prompt
        messages = [
            {"role": "system", "content": self.system_prompts[self.role]},
            {"role": "user", "content": task}
        ]
        
        # Add context if provided
        if context:
            context_str = f"\n\n**Context:**\n{context}"
            messages[-1]["content"] += context_str
        
        logger.info(f"{self.role.value.upper()} agent thinking...")
        response, _ = self.router.chat(messages)
        
        return response


class AgentSystem:
    """Multi-agent system coordinator."""
    
    def __init__(self, router: AIRouter):
        """Initialize agent system.
        
        Args:
            router: AI router
        """
        self.router = router
        self.agents = {
            role: Agent(role, router)
            for role in AgentRole
        }
        logger.info("Multi-agent system initialized")
    
    def research(self, query: str, use_web: bool = True) -> str:
        """Use researcher agent.
        
        Args:
            query: Research query
            use_web: Whether to use web search
            
        Returns:
            Research results
        """
        context = {"use_web_search": use_web}
        return self.agents[AgentRole.RESEARCHER].think(query, context)
    
    def write_code(self, task: str, language: str = "python") -> str:
        """Use coder agent.
        
        Args:
            task: Coding task
            language: Programming language
            
        Returns:
            Code solution
        """
        context = {"language": language}
        return self.agents[AgentRole.CODER].think(task, context)
    
    def create_plan(self, goal: str) -> str:
        """Use planner agent.
        
        Args:
            goal: Goal description
            
        Returns:
            Detailed plan
        """
        return self.agents[AgentRole.PLANNER].think(goal)
    
    def review(self, content: str, content_type: str = "answer") -> str:
        """Use critic agent.
        
        Args:
            content: Content to review
            content_type: Type of content
            
        Returns:
            Review and suggestions
        """
        task = f"Review this {content_type}:\n\n{content}"
        return self.agents[AgentRole.CRITIC].think(task)
    
    def execute_task(
        self,
        task: str,
        use_planner: bool = True,
        use_researcher: bool = True,
        use_critic: bool = True
    ) -> Dict[str, Any]:
        """Execute complex task using multiple agents.
        
        Args:
            task: Task description
            use_planner: Use planner agent
            use_researcher: Use researcher agent
            use_critic: Use critic agent
            
        Returns:
            Execution results
        """
        results = {
            'task': task,
            'plan': None,
            'research': None,
            'answer': None,
            'review': None,
            'final': None
        }
        
        # Step 1: Create plan
        if use_planner:
            logger.info("Creating plan...")
            results['plan'] = self.create_plan(task)
        
        # Step 2: Research if needed
        if use_researcher:
            logger.info("Conducting research...")
            results['research'] = self.research(task)
        
        # Step 3: Generate answer (using executor)
        logger.info("Generating answer...")
        context = {
            'plan': results.get('plan'),
            'research': results.get('research')
        }
        results['answer'] = self.agents[AgentRole.EXECUTOR].think(task, context)
        
        # Step 4: Review answer
        if use_critic:
            logger.info("Reviewing answer...")
            results['review'] = self.review(results['answer'])
        
        # Step 5: Final output
        results['final'] = self._compile_final_answer(results)
        
        return results
    
    def _compile_final_answer(self, results: Dict) -> str:
        """Compile final answer from all agent outputs.
        
        Args:
            results: Results from all agents
            
        Returns:
            Final compiled answer
        """
        output = []
        
        if results.get('plan'):
            output.append("## 📋 Plan")
            output.append(results['plan'])
            output.append("")
        
        if results.get('research'):
            output.append("## 🔍 Research")
            output.append(results['research'])
            output.append("")
        
        output.append("## ✅ Answer")
        output.append(results['answer'])
        
        if results.get('review'):
            output.append("")
            output.append("## 👁️ Quality Review")
            output.append(results['review'])
        
        return "\n".join(output)


# Global agent system (will be initialized later)
agent_system: Optional[AgentSystem] = None


def initialize_agent_system(router: AIRouter):
    """Initialize the global agent system.
    
    Args:
        router: AI router
    """
    global agent_system
    agent_system = AgentSystem(router)
    logger.info("Global agent system initialized")
