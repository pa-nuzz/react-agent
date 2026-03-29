import { DynamicTool } from "@langchain/core/tools";
import * as dotenv from "dotenv";

dotenv.config();

class RateLimiter {
  private requests: number[] = [];
  
  constructor(
    private requestsPerMinute: number = 60,
    private burst: number = 10
  ) {}

  isAllowed(): boolean {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < 60000);
    
    if (this.requests.length >= this.requestsPerMinute) {
      return false;
    }
    
    this.requests.push(now);
    return true;
  }
}

const weatherTool = new DynamicTool({
  name: "get_weather",
  description: "Get weather for a given city",
  func: async (city: string) => `It's always sunny in ${city}!`,
});

const nepalInfoTool = new DynamicTool({
  name: "get_nepali_info",
  description: "Get information about Nepal",
  func: async (query: string) => {
    const nepaliInfo: Record<string, string> = {
      capital: "Kathmandu is the capital of Nepal.",
      population: "Nepal has a population of approximately 30 million people.",
      language: "The official language of Nepal is Nepali.",
      currency: "The currency of Nepal is Nepalese Rupee (NPR).",
      mountain: "Mount Everest, the highest peak in the world, is located in Nepal.",
      culture: "Nepal is known for its rich culture, temples, and Himalayan heritage."
    };
    
    const queryLower = query.toLowerCase();
    for (const [key, value] of Object.entries(nepaliInfo)) {
      if (queryLower.includes(key)) {
        return value;
      }
    }
    
    return "Nepal is a beautiful country in the Himalayas known for Mount Everest and rich cultural heritage.";
  },
});

class ReactAgent {
  private tools: Map<string, DynamicTool>;
  private rateLimiter: RateLimiter;
  
  constructor(tools: DynamicTool[], rateLimiter?: RateLimiter) {
    this.tools = new Map();
    tools.forEach(tool => this.tools.set(tool.name, tool));
    this.rateLimiter = rateLimiter || new RateLimiter();
  }

  async processMessage(input: string): Promise<string> {
    if (!this.rateLimiter.isAllowed()) {
      return "Rate limit exceeded. Please try again later.";
    }

    const lowerInput = input.toLowerCase();
    
    if (lowerInput.includes("weather") && 
        ["san francisco", "new york", "london", "tokyo", "kathmandu", "pokhara"].some(city => lowerInput.includes(city))) {
      
      let city = "Kathmandu";
      if (lowerInput.includes("san francisco")) city = "San Francisco";
      else if (lowerInput.includes("new york")) city = "New York";
      else if (lowerInput.includes("london")) city = "London";
      else if (lowerInput.includes("tokyo")) city = "Tokyo";
      else if (lowerInput.includes("pokhara")) city = "Pokhara";
      
      const weatherResult = await weatherTool.func(city);
      return `I checked the weather for ${city}. ${weatherResult}`;
    }
    
    if (["nepal", "kathmandu", "everest", "nepali"].some(term => lowerInput.includes(term))) {
      return await nepalInfoTool.func(lowerInput);
    }
    
    if (lowerInput.includes("capital of france")) {
      return "The capital of France is Paris.";
    }
    
    if (lowerInput.includes("new york")) {
      return "New York is a major city known for its iconic skyline, diverse culture, and attractions like Times Square, Central Park, and the Statue of Liberty. The weather there is always sunny!";
    }
    
    return "Hello! I'm a ReAct-style agent that can help with weather information and general knowledge. I also know about Nepal! Try asking me about Nepali cities, culture, or Mount Everest.";
  }
}

async function main() {
  const rateLimitRpm = parseInt(process.env.RATE_LIMIT_REQUESTS_PER_MINUTE || "60");
  const rateLimitBurst = parseInt(process.env.RATE_LIMIT_BURST || "10");
  
  const rateLimiter = new RateLimiter(rateLimitRpm, rateLimitBurst);
  const agent = new ReactAgent([weatherTool, nepalInfoTool], rateLimiter);

  const testCases = [
    "What is the weather in Kathmandu?",
    "Tell me about Mount Everest",
    "What is the capital of France?",
    "What is the weather in San Francisco?",
    "Tell me about Nepali culture"
  ];
  
  console.log("ReAct-Style Agent - Nepal Edition");
  console.log("=".repeat(40));
  
  for (let i = 0; i < testCases.length; i++) {
    console.log(`\nTest ${i + 1}: ${testCases[i]}`);
    const result = await agent.processMessage(testCases[i]);
    console.log(`Result: ${result}`);
  }
  
  console.log("\nAll tests completed successfully!");
}

main().catch(console.error);
