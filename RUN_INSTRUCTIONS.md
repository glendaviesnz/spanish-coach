# Running the Spanish Coach Agent

Follow these steps to run the Spanish Coach agent using Google ADK's web interface.

## Prerequisites

- Python 3.10 or higher
- Poetry installed (https://python-poetry.org/docs/#installation)
- Google API key configured (see API_KEY_SETUP.md)

## Running the Agent

1. Navigate to the spanish-coach directory:

   ```
   cd spanish-coach
   ```

2. Use Poetry to install dependencies:

   ```
   poetry install
   ```

3. Activate the Poetry environment:

   ```
   poetry shell
   ```

4. Run the ADK web interface:

   ```
   adk web
   ```

5. Open your browser and go to http://localhost:8000

6. You can now interact with the Spanish Coach agent!

## Example Interactions

Try asking the agent:

- "Can you help me learn Spanish verb conjugations?"
- "How do I conjugate the verb 'hablar'?"
- "What are some common Spanish greetings?"
- "How do I count from 1 to 10 in Spanish?"

## Troubleshooting

If you encounter errors:

1. Make sure your Google API key is correctly set up
2. Check that you've installed Poetry correctly
3. Try running `poetry update` to update dependencies
4. Ensure the virtual environment is activated with `poetry shell`
