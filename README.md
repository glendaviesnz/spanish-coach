# Spanish Coach

A Spanish language learning agent built with Google ADK that helps users learn and practice Spanish.

## Features

- **Spanish Coach**: Main agent that handles general Spanish language learning questions
- **Conjugator**: Sub-agent specialized in providing complete Spanish verb conjugation tables

## Installation

1. Make sure you have Python 3.10+ installed
2. Install Poetry if you don't have it yet:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Clone the repository
4. Navigate to the project directory:
   ```
   cd spanish-coach
   ```
5. Install dependencies with Poetry:
   ```
   poetry install
   ```
6. Set your Google API key in a `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Running the agent

From the spanish-coach directory:

```bash
# Activate the Poetry environment
poetry shell

# Run the agent
adk web
```

Then open your browser to http://localhost:8000 to interact with the agent.

## Usage examples

- "How do I conjugate the verb 'hablar'?"
- "What are the basic Spanish greetings?"
- "Can you help me practice Spanish numbers?"
