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

from spanish_coach.sub_agents.grammar_checker.prompt import GRAMMAR_CHECKER_PROMPT

MODEL = "gemini-2.5-flash-preview-04-17"

grammar_checker_agent = Agent(
    model=MODEL,
    name="grammar_checker_agent",
    description="A specialized agent for validating and correcting Spanish sentences and translations",
    instruction=GRAMMAR_CHECKER_PROMPT,
    output_key="corrected_sentences",
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
        ),
    )
) 