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

# Import necessary classes for the callback
import json # For serializing the example_sentences if they are complex
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest

from spanish_coach.sub_agents.grammar_checker.prompt import GRAMMAR_CHECKER_PROMPT

MODEL = "gemini-2.5-flash-preview-04-17"

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

grammar_checker_agent = Agent(
    model=MODEL,
    name="grammar_checker_agent",
    description="A specialized agent for validating and correcting Spanish sentences and translations",
    instruction=GRAMMAR_CHECKER_PROMPT,
    output_key="corrected_sentences",
    before_model_callback=append_sentences_to_prompt,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
        ),
    )
) 