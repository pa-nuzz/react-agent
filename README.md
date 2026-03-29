# 🇳🇵 ReAct-Style Agent - Nepal Edition 🇳🇵

A secure ReAct-style agent implementation with weather tool, Nepal information, and general query capabilities in both Python and TypeScript.

## 🌟 Features

- **🔒 Security First**: Rate limiting, no hardcoded API keys, environment variables only
- **🇳🇵 Nepal Context**: Specialized knowledge about Nepal, Kathmandu, Mount Everest, and Nepali culture
- **⚡ Rate Limiting**: Built-in protection against abuse (60 requests/minute by default)
- **🛠️ Dual Implementation**: Both Python and TypeScript versions
- **🔧 ReAct Pattern**: Reasoning and Acting agent architecture
- **🌍 Weather Tool**: Mock weather functionality (easily replaceable with real API)
- **📚 General Knowledge**: Handles non-weather queries independently

## 🏗️ Architecture

```
lang/
├── agent.py              # Python implementation with Nepal context
├── requirements.txt       # Python dependencies
├── package.json          # TypeScript dependencies
├── tsconfig.json         # TypeScript configuration
├── src/
│   └── index.ts          # TypeScript implementation with Nepal context
├── .env.example          # Environment variables template
├── .gitignore           # Security & cleanup rules
└── README.md            # This file
```

## 🚀 Quick Start

### Python Implementation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment**:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

3. **Run the agent**:
```bash
python agent.py
```

### TypeScript Implementation

1. **Install dependencies**:
```bash
npm install
```

2. **Set up environment**:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

3. **Build and run**:
```bash
npm run build
npm start
```

## 🔧 Tools Available

### 🌤️ Weather Tool
- **Cities**: Kathmandu, Pokhara, San Francisco, New York, London, Tokyo
- **Response**: Mock weather data (replaceable with real API)

### 🇳🇵 Nepal Information Tool
- **Topics**: Capital, population, language, currency, Mount Everest, culture
- **Context**: Specialized knowledge about Nepal

### 🧠 General Knowledge
- **Capabilities**: Geography, general facts
- **Fallback**: Friendly help message

## 🛡️ Security Features

### Rate Limiting
- **Default**: 60 requests per minute
- **Burst**: 10 concurrent requests
- **Configuration**: Via environment variables

### API Key Safety
- ✅ No hardcoded keys in source code
- ✅ Environment variables only
- ✅ `.env` in `.gitignore`
- ✅ Template provided (`.env.example`)

### Input Validation
- ✅ Message content filtering
- ✅ Tool usage validation
- ✅ Error handling

## 🧪 Test Cases

Both implementations include Nepal-focused test cases:

1. **🇳🇵 Nepal Weather**: "What is the weather in Kathmandu?"
2. **🏔️ Mount Everest**: "Tell me about Mount Everest"
3. **🌍 General Knowledge**: "What is the capital of France?"
4. **🌤️ International Weather**: "What is the weather in San Francisco?"
5. **🎭 Nepali Culture**: "Tell me about Nepali culture"

## 📝 Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# LangSmith Configuration
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=react-agent-nepal

# Model API Keys (choose one)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST=10
```

## 💡 Usage Examples

### Python
```python
from agent import ReactAgent, get_weather, get_nepali_info, RateLimiter

# Create agent with rate limiting
rate_limiter = RateLimiter(requests_per_minute=60, burst=10)
agent = ReactAgent([get_weather, get_nepali_info], rate_limiter)

# Process message
result = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in Kathmandu?"}]
})
```

### TypeScript
```typescript
import { ReactAgent, weatherTool, nepalInfoTool, RateLimiter } from './src';

// Create agent with rate limiting
const rateLimiter = new RateLimiter(60, 10);
const agent = new ReactAgent([weatherTool, nepalInfoTool], rateLimiter);

// Process message
const result = await agent.processMessage("What's the weather in Kathmandu?");
```

## 🔮 Future Enhancements

1. **🌐 Real Weather API**: Integrate with OpenWeatherMap or similar
2. **🤖 Real LLM Integration**: Replace mock agents with actual models
3. **📱 Web Interface**: Add React/Vue frontend
4. **🗺️ More Locations**: Expand city coverage
5. **🔍 Advanced Search**: Add web search capabilities
6. **📊 Analytics**: Usage tracking and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- LangChain for the excellent framework
- The Nepali community for inspiration
- Open source contributors worldwide

---

**Made with ❤️ in Nepal** 🇳🇵
