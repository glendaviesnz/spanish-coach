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

"""Sentence Constructor sub-agent for generating Spanish example sentences."""

import os
import json
from pathlib import Path
from google.adk import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types

# Import necessary classes for the callback
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest

from spanish_coach.sub_agents.sentence_constructor.prompt import SENTENCE_CONSTRUCTOR_PROMPT

MODEL = "gemini-2.5-flash-preview-04-17"

# Load the top 1000 Spanish words
current_dir = Path(__file__).parent
words_file_path = current_dir / "top-1000-spanish-words.txt"

# Read the words from the file
with open(words_file_path, 'r', encoding='utf-8') as file:
    top_spanish_words = [word.strip() for word in file.readlines()]

# Create a comma-separated string of the words
top_words_list = ", ".join(top_spanish_words)

# Create an instruction with the words list appended
instruction = SENTENCE_CONSTRUCTOR_PROMPT + f"\n\nHere is the list of the top 1000 Spanish words you should use:\n{top_words_list}"

# Define the callback function
def append_conjugations_to_prompt(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> None:
    """
    Appends verb_conjugations from the session state to the LLM prompt.
    """
    verb_conjugations = callback_context.state.get("verb_conjugations")

    if verb_conjugations:
        # Create the text to append.
        # Ensure verb_conjugations is a string, if it's a dict/object, serialize it appropriately.
        conjugation_data = json.dumps(verb_conjugations) if isinstance(verb_conjugations, (dict, list)) else str(verb_conjugations)
        conjugation_info_for_prompt = f"\n\nOnly create sentences for the following conjugations: {conjugation_data}"

        # Append the additional information using the correct method
        llm_request.append_instructions([conjugation_info_for_prompt])
        print(f"SentenceConstructor: Appended verb_conjugations to prompt.")
    else:
        print("SentenceConstructor: 'verb_conjugations' not found in state, prompt not modified.")


sentence_constructor_agent = Agent(
    model=MODEL,
    name="sentence_constructor_agent",
    description="A specialized agent for creating simple Spanish sentences using conjugated verbs",
    instruction=instruction,
    output_key="example_sentences",
    before_model_callback=append_conjugations_to_prompt,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
        ),
    )
) 