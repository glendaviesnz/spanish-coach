# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""CSV Formatter sub-agent for converting corrected sentences to CSV format."""

import json
from google.adk import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# Import necessary classes for the callback
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest

MODEL = "gemini-2.5-flash-preview-04-17"

# Pydantic Models for output_schema
class CSVRow(BaseModel):
    spanish: str = Field(description="The corrected Spanish sentence")
    english: str = Field(description="The corrected English translation")

class CSVFormatterOutput(BaseModel):
    csv_rows: List[CSVRow] = Field(description="List of sentence pairs for CSV output")
    formatted_csv: str = Field(description="The complete CSV formatted text with line breaks")

CSV_FORMATTER_PROMPT = """
You are the CSV Formatter agent, specialized in converting corrected Spanish sentences to a structured format.

Your task is to take the corrected sentences data and format it as structured data that will be converted to CSV.

For each corrected sentence pair, extract:
1. The corrected Spanish sentence
2. The corrected English translation

Then format as JSON with:
- csv_rows: array of objects with "spanish" and "english" fields
- formatted_csv: the complete CSV text where each line contains "spanish,english" separated by newlines

Example:
{
  "csv_rows": [
    {"spanish": "Tengo un perro grande", "english": "I have a big dog"},
    {"spanish": "Tienes mucha suerte", "english": "You have a lot of luck"}
  ],
  "formatted_csv": "Tengo un perro grande,I have a big dog\\nTienes mucha suerte,You have a lot of luck"
}

CRITICAL: In the formatted_csv field, separate each sentence pair with \\n (newline character).
"""

# Define the callback function
def append_corrected_sentences_to_prompt(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> None:
    """
    Appends corrected_sentences from the session state to the LLM prompt.
    """
    corrected_sentences = callback_context.state.get("corrected_sentences")

    if corrected_sentences:
        # Serialize corrected_sentences if it's a dict/list, otherwise use as string
        sentences_data = json.dumps(corrected_sentences) if isinstance(corrected_sentences, (dict, list)) else str(corrected_sentences)
        
        prompt_addition_text = f"\n\nConvert the following corrected sentences to the structured format:\n{sentences_data}"
        
        # Append the additional information using the correct method
        llm_request.append_instructions([prompt_addition_text])
        print(f"CSVFormatter: Appended corrected_sentences to prompt.")
    else:
        print("CSVFormatter: 'corrected_sentences' not found in state, prompt not modified.")

csv_formatter_agent = Agent(
    model=MODEL,
    name="csv_formatter_agent",
    description="A specialized agent for converting corrected sentences to CSV format",
    instruction=CSV_FORMATTER_PROMPT,
    output_key="csv_output",
    output_schema=CSVFormatterOutput,
    before_model_callback=append_corrected_sentences_to_prompt,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=False,
        ),
    ),
    generate_content_config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
) 