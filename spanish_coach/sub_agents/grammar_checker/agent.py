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

"""Grammar Checker sub-agent for validating Spanish sentences and translations."""

from google.adk import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional, Any

# Import necessary classes for the callback
import json # For serializing the example_sentences if they are complex
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

from spanish_coach.sub_agents.grammar_checker.prompt import GRAMMAR_CHECKER_PROMPT
from spanish_coach.utils import convert_corrected_sentences_to_csv

MODEL = "gemini-2.5-flash-preview-04-17"

# Pydantic Models for output_schema
class CorrectedSentence(BaseModel):
    original_spanish: str = Field(description="The original Spanish sentence")
    corrected_spanish: str = Field(description="The corrected Spanish sentence")
    original_english: str = Field(description="The original English translation")
    corrected_english: str = Field(description="The corrected English translation")
    corrections_made: List[str] = Field(description="List of corrections made to the sentence")
    grammar_notes: Optional[str] = Field(description="Additional grammar notes or explanations")

class GrammarCheckerOutput(BaseModel):
    corrected_sentences: List[CorrectedSentence] = Field(description="List of corrected sentences with explanations")
    total_corrections: int = Field(description="Total number of corrections made")
    summary: Optional[str] = Field(description="Summary of common issues found")

# Define the callback function
def append_sentences_to_prompt(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> None:
    """
    Appends example_sentences from the session state to the LLM prompt.
    """
    example_sentences = callback_context.state.get("example_sentences")

    if example_sentences:
        # Serialize example_sentences if it's a dict/list, otherwise use as string
        sentences_data = json.dumps(example_sentences) if isinstance(example_sentences, (dict, list)) else str(example_sentences)
        
        prompt_addition_text = f"\n\nPlease check and correct the following Spanish sentences and their English translations:\n{sentences_data}"
        
        # Append the additional information using the correct method
        llm_request.append_instructions([prompt_addition_text])
        print(f"GrammarChecker: Appended example_sentences to prompt.")
    else:
        print("GrammarChecker: 'example_sentences' not found in state, prompt not modified.")

def convert_to_csv_callback(
    callback_context: CallbackContext, llm_response: LlmResponse, **kwargs
) -> None:
    """
    After the grammar checker completes, convert its output to CSV format.
    Get the data from the LLM response since state isn't updated yet.
    IMPORTANT: Don't return anything to avoid overriding the normal response.
    """
    print(f"GrammarChecker: convert_to_csv_callback called")
    
    # Get the response content
    if llm_response and llm_response.content and llm_response.content.parts:
        response_text = llm_response.content.parts[0].text
        print(f"GrammarChecker: Got response text ({len(response_text)} chars)")
        
        try:
            # Parse the JSON response
            response_data = json.loads(response_text)
            print(f"GrammarChecker: Parsed JSON response: {type(response_data)}")
            
            # Convert to CSV using our utility function
            csv_output = convert_corrected_sentences_to_csv(response_data)
            
            if csv_output:
                # Store CSV in state
                callback_context.state["csv_output"] = csv_output
                print(f"GrammarChecker: Added CSV output to state ({len(csv_output)} characters)")
                print(f"GrammarChecker: CSV preview: {csv_output[:200]}...")
                
                # Print the full CSV to console so you can see it
                print("=== FULL CSV OUTPUT ===")
                print(csv_output)
                print("=== END CSV OUTPUT ===")
            else:
                print("GrammarChecker: CSV output was empty")
                
        except json.JSONDecodeError as e:
            print(f"GrammarChecker: Failed to parse JSON response: {e}")
        except Exception as e:
            print(f"GrammarChecker: Error in CSV conversion: {e}")
    else:
        print("GrammarChecker: No response content found")
    
    # Don't return anything - this avoids overriding the normal JSON response

grammar_checker_agent = Agent(
    model=MODEL,
    name="grammar_checker_agent",
    description="A specialized agent for validating and correcting Spanish sentences and translations",
    instruction=GRAMMAR_CHECKER_PROMPT,
    output_key="corrected_sentences",
    output_schema=GrammarCheckerOutput,
    before_model_callback=append_sentences_to_prompt,
    after_model_callback=convert_to_csv_callback,  # Re-enabled with fix
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=False,
        ),
    ),
    generate_content_config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
) 