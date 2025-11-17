class GeminiClient:
    def generate_text(self, prompt: str) -> str:
        # Simple stub for AI command suggestion — replace with real model/service later
        # If prompt refers to opening Edge, return start msedge
        user_task = prompt.lower()
        if "edge" in user_task:
            return "start msedge"
        if "chrome" in user_task:
            return "start chrome"
        if "notepad" in user_task:
            return "start notepad"
        if "calculator" in user_task or "calc" in user_task:
            return "start calc"
        return "N/A"
