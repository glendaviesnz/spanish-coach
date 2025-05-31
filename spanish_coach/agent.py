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

"""Spanish Coach: An agent to help with learning Spanish language."""

import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.conjugator.agent import conjugator_agent
from .sub_agents.sentence_constructor.agent import sentence_constructor_agent
from .sub_agents.grammar_checker.agent import grammar_checker_agent

# Load environment variables from .env file
load_dotenv()

# Set API key from environment variable
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

MODEL = "gemini-2.5-flash-preview-04-17"

# Original tool-based agent implementation (kept for reference)
spanish_coach = Agent(
    model=MODEL,
    name="spanish_coach",
    description="An agent to help with learning Spanish language",
    instruction=prompt.SPANISH_COACH_PROMPT,
    tools=[
        AgentTool(agent=conjugator_agent),
        AgentTool(agent=sentence_constructor_agent),
        AgentTool(agent=grammar_checker_agent),
    ],
)

# New workflow-based sequential agent
spanish_coach_workflow = SequentialAgent(
    name="spanish_coach_workflow",
    description="A sequential workflow for Spanish language learning",
    sub_agents=[
        conjugator_agent,  # First step: conjugate verbs
        sentence_constructor_agent,  # Second step: construct sentences
        grammar_checker_agent  # Final step: check grammar
    ]
)

# Use the workflow agent as the root agent
root_agent = spanish_coach_workflow 