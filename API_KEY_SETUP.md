# API Key Setup Instructions

To use the Spanish Coach agent, you need to set up your Google API key.

## Steps:

1. Create a `.env` file in the `spanish-coach` directory
2. Add your Google API key to the file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
3. The python-dotenv package will be installed automatically through Poetry:
   ```
   poetry install
   ```

## Alternative Method:

If you prefer not to use a .env file, you can set the API key directly as an environment variable:

```bash
# On Linux/macOS
export GOOGLE_API_KEY=your_api_key_here

# On Windows PowerShell
$env:GOOGLE_API_KEY="your_api_key_here"

# On Windows Command Prompt
set GOOGLE_API_KEY=your_api_key_here
```
