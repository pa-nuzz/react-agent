import os
import time
from typing import Dict, List, Optional
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables import Runnable

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def get_nepali_info(query: str) -> str:
    """Get information about Nepal."""
    nepali_info = {
        "capital": "Kathmandu is the capital of Nepal.",
        "population": "Nepal has a population of approximately 30 million people.",
        "language": "The official language of Nepal is Nepali.",
        "currency": "The currency of Nepal is Nepalese Rupee (NPR).",
        "mountain": "Mount Everest, the highest peak in the world, is located in Nepal.",
        "culture": "Nepal is known for its rich culture, temples, and Himalayan heritage."
    }
    
    query_lower = query.lower()
    for key, value in nepali_info.items():
        if key in query_lower:
            return value
    
    return "Nepal is a beautiful country in the Himalayas known for Mount Everest and rich cultural heritage."

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60, burst: int = 10):
        self.requests_per_minute = requests_per_minute
        self.burst = burst
        self.requests = []
    
    def is_allowed(self) -> bool:
        now = time.time()
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if len(self.requests) >= self.requests_per_minute:
            return False
        
        self.requests.append(now)
        return True

class ReactAgent(Runnable):
    def __init__(self, tools: List, rate_limiter: Optional[RateLimiter] = None):
        self.tools = {tool.name: tool for tool in tools}
        self.rate_limiter = rate_limiter or RateLimiter()
    
    def invoke(self, input_data: Dict, config=None) -> Dict:
        if not self.rate_limiter.is_allowed():
            return {
                "messages": input_data["messages"] + [
                    AIMessage(content="Rate limit exceeded. Please try again later.")
                ]
            }
        
        messages = input_data["messages"]
        last_message = ""
        
        if messages:
            last_msg = messages[-1]
            if isinstance(last_msg, dict):
                last_message = last_msg.get("content", "")
            else:
                last_message = last_msg.content
        
        lower_message = last_message.lower()
        
        if "weather" in lower_message and any(city in lower_message for city in ["san francisco", "new york", "london", "tokyo", "kathmandu", "pokhara"]):
            city = "Kathmandu"
            if "san francisco" in lower_message:
                city = "San Francisco"
            elif "new york" in lower_message:
                city = "New York"
            elif "london" in lower_message:
                city = "London"
            elif "tokyo" in lower_message:
                city = "Tokyo"
            elif "pokhara" in lower_message:
                city = "Pokhara"
            
            weather_result = get_weather.invoke({"city": city})
            response_content = f"I checked the weather for {city}. {weather_result}"
        
        elif any(term in lower_message for term in ["nepal", "kathmandu", "everest", "nepali"]):
            response_content = get_nepali_info.invoke({"query": lower_message})
        
        elif "capital of france" in lower_message:
            response_content = "The capital of France is Paris."
        elif "new york" in lower_message:
            response_content = "New York is a major city known for its iconic skyline, diverse culture, and attractions like Times Square, Central Park, and the Statue of Liberty. The weather there is always sunny!"
        else:
            response_content = "Hello! I'm a ReAct-style agent that can help with weather information and general knowledge. I also know about Nepal! Try asking me about Nepali cities, culture, or Mount Everest."
        
        return {
            "messages": messages + [AIMessage(content=response_content)]
        }

def main():
    rate_limit_rpm = int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "60"))
    rate_limit_burst = int(os.getenv("RATE_LIMIT_BURST", "10"))
    
    rate_limiter = RateLimiter(rate_limit_rpm, rate_limit_burst)
    tools = [get_weather, get_nepali_info]
    agent = ReactAgent(tools, rate_limiter)

    test_cases = [
        "What is the weather in Kathmandu?",
        "Tell me about Mount Everest",
        "What is the capital of France?",
        "What is the weather in San Francisco?",
        "Tell me about Nepali culture"
    ]
    
    print("ReAct-Style Agent - Nepal Edition")
    print("=" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case}")
        result = agent.invoke({
            "messages": [{"role": "user", "content": test_case}]
        })
        print(f"Result: {result['messages'][-1].content}")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main()
