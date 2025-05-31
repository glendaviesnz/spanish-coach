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

"""Conjugator sub-agent for Spanish verb conjugations."""

from google.adk import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types as genai_types
from pydantic import BaseModel, Field
from typing import Dict

from spanish_coach.sub_agents.conjugator.prompt import CONJUGATOR_PROMPT

MODEL = "gemini-2.5-flash-preview-04-17"

# Pydantic Models for output_schema
class PronounConjugations(BaseModel):
    yo: str
    tu: str
    el_ella_usted: str = Field(alias="el/ella/usted")
    nosotros: str
    ellos_ellas: str = Field(alias="ellos/ellas")

class PastParticipleConjugation(BaseModel):
    default: str

class ConjugationOutput(BaseModel):
    verb: str
    present: PronounConjugations
    preterite: PronounConjugations
    imperfect: PronounConjugations
    conditional: PronounConjugations
    future: PronounConjugations
    past_participle: PastParticipleConjugation
    present_subjunctive: PronounConjugations

conjugator_agent = Agent(
    model=MODEL,
    name="conjugator_agent",
    description="A specialized agent for Spanish verb conjugations",
    instruction=CONJUGATOR_PROMPT,
    output_key="verb_conjugations",
    output_schema=ConjugationOutput,
    planner=BuiltInPlanner(
        thinking_config=genai_types.ThinkingConfig(
            include_thoughts=False,
        ),
    ),
    generate_content_config=genai_types.GenerateContentConfig(
        response_mime_type="application/json"
    )
) 