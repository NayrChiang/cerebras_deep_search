# Cerebras Deep Search 🔍

A Perplexity-style deep research assistant that can automatically search the web, analyze multiple sources, and provide structured insights using Cerebras LLM and Exa search engine.

## Features ✨

- 🔍 **Intelligent Web Search**: Uses Exa's neural search for relevant content
- 🧠 **AI-Powered Analysis**: Leverages Cerebras fast inference for insights
- 📊 **Two-Layer Research**: Deep research with follow-up queries for comprehensive analysis
- 💾 **Result Export**: Save research results to JSON files
- 🔒 **Secure Configuration**: Environment variable-based API key management

## Project Structure 📁

```
cerebras_deep_search/
├── src/
│   └── deep_research.py          # Main application
├── tests/                        # Test files
├── resources/                    # Original notebook
├── output/                       # Research results (auto-created)
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## Installation and Setup 🚀

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Keys

You need the following API keys:

- **Cerebras**: [Get API Key](https://cloud.cerebras.ai) - For LLM inference
- **Exa**: [Get API Key](https://exa.ai) - For web search

### 3. Configure API Keys

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit the `.env` file with your actual API keys:

```bash
EXA_API_KEY=your_actual_exa_api_key
CEREBRAS_API_KEY=your_actual_cerebras_api_key
```

## Usage 💻

### Run the Application

```bash
python src/deep_research.py
```

### Research Options

1. **Basic Research**: Single-layer search and analysis
2. **Deep Research**: Two-layer research with follow-up queries for comprehensive insights

### Example Queries

- "What are the latest AI breakthroughs in 2024?"
- "Climate change solutions for 2025"
- "Quantum computing advances"
- "Space exploration news"

## How It Works 🔧

### Basic Research Flow
```
Query → Web Search → Content Analysis → AI Synthesis → Results
```

### Deep Research Flow
```
Query → Initial Search → AI Analysis → Follow-up Query → 
Additional Search → Comprehensive Synthesis → Enhanced Results
```

## API Integration

### Exa Search Engine
- **Neural Search**: Finds semantically relevant content
- **Content Extraction**: Automatically scrapes and extracts text
- **Auto Search**: Blends keyword and semantic search

### Cerebras LLM
- **Model**: llama-4-scout-17b-16e-instruct
- **Fast Inference**: Optimized for research analysis
- **Structured Output**: Generates formatted insights

## Output Format 📄

Research results include:

- **Query**: Original research question
- **Sources**: Number of sources analyzed
- **Summary**: Comprehensive overview
- **Insights**: Key findings as bullet points
- **Source Details**: Full source information with URLs

## Development 🛠️

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
flake8 src/
```

## Security 🔒

- API keys are stored in environment variables
- `.env` files are excluded from version control
- No sensitive data is committed to the repository

## Troubleshooting 🔧

### Common Issues

1. **API Key Errors**: Ensure your API keys are correctly configured in `.env`
2. **Import Errors**: Run `pip install -r requirements.txt`
3. **Search Failures**: Check your Exa API key and quota
4. **AI Response Errors**: Verify your Cerebras API key

### Environment Check

```bash
python -c "import exa_py; print('Exa OK')"
python -c "import cerebras.cloud.sdk; print('Cerebras OK')"
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License 📄

This project is open source. Please see the LICENSE file for details.

## Support 💬

If you have questions:
- [Cerebras Discord](https://cerebras.ai/discord)
- [Exa Documentation](https://docs.exa.ai)

## Changelog 📝

### v1.0.0
- Initial release
- Basic and deep research functionality
- Environment variable configuration
- Result export capabilities
