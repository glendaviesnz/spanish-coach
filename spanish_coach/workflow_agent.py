"""Spanish Coach Workflow: A sequential workflow approach to Spanish language learning."""

import os
from dotenv import load_dotenv
from google.adk import SequentialAgent
from google.adk.agents import LlmAgent

from .sub_agents.conjugator.agent import conjugator_agent
from .sub_agents.sentence_constructor.agent import sentence_constructor_agent
from .sub_agents.grammar_checker.agent import grammar_checker_agent

# Load environment variables from .env file
load_dotenv()

# Set API key from environment variable
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

MODEL = "gemini-2.5-flash-preview-04-17"

# Create the sequential agent with sub-agents in the desired order
spanish_coach_workflow = SequentialAgent(
    name="spanish_coach_workflow",
    description="A sequential workflow for Spanish language learning",
    sub_agents=[
        conjugator_agent,  # First step: conjugate verbs
        sentence_constructor_agent,  # Second step: construct sentences
        grammar_checker_agent  # Final step: check grammar
    ]
)

# The workflow will automatically execute sub-agents in sequence,
# passing results from one agent to the next via state
workflow_agent = spanish_coach_workflow 