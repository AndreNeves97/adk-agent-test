# Multi-Tool Weather Agent 🌤️

A Python-based weather agent that demonstrates the integration of multiple APIs and tools to provide comprehensive weather information and location services. This project showcases API integration and error handling in a real-world application.

## 🌟 Features

- **Weather Information**: Get detailed weather reports for any location using OpenWeatherMap API
- **Geocoding Services**: Convert location names to coordinates and vice versa using Nominatim API
- **Temperature Analysis**: Calculate average temperatures with support for both Celsius and Fahrenheit
- **Error Handling**: Robust error handling and informative error messages
- **Environment Management**: Secure API key management using environment variables

## 🛠️ Technologies Used

- Python 3.x
- Google ADK (Agent Development Kit)
- OpenWeatherMap API
- Nominatim Geocoding API
- python-dotenv for environment management
- requests for HTTP operations

## 📋 Prerequisites

- Python 3.x installed
- OpenWeatherMap API key
- Internet connection for API access

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AndreNeves97/adk-agent-test.git
   cd multi-tool-agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=gemini-studio-api-key
   OPENWEATHER_API_KEY=your_api_key_here
   ```

## 💻 Usage

There are multiple ways to interact with the agent:

### 1. Dev UI (Interactive Development Interface)

Start the development UI with:
```bash
adk web
```

Then:
1. Open the URL provided (usually `http://localhost:8000` or `http://127.0.0.1:8000`) in your browser
2. Select "multi_tool_agent" from the dropdown menu in the top-left corner
3. Start chatting with your agent using the textbox
4. Use the UI to inspect function calls, responses, and model outputs

### 2. Terminal Interface

Chat with your agent directly in the terminal:
```bash
adk run multi_tool_agent
```

To exit, use Ctrl+C (Cmd+C on macOS).

### 3. API Server

Start a local FastAPI server for testing API endpoints:
```bash
adk api_server
```

This creates a local server that you can use to test API requests before deployment.

### Example Prompts to Try

- "What's the weather in New York?"
- "Get the coordinates for Tokyo"
- "What's the temperature in London?"
- "Calculate the average temperature for [20, 22, 25] degrees"

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- OpenWeatherMap for weather data
- OpenStreetMap and Nominatim for geocoding services
- Google ADK team for the agent development framework 