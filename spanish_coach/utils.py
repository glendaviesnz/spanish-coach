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

"""Utility functions for Spanish Coach."""

from typing import Dict, List, Any


def convert_corrected_sentences_to_csv(corrected_sentences_data: Any) -> str:
    """
    Convert the grammar checker output to CSV format.
    
    Args:
        corrected_sentences_data: The corrected sentences data from the grammar checker agent
        
    Returns:
        CSV formatted string with corrected_spanish,corrected_english on each line
    """
    print(f"Utils: convert_corrected_sentences_to_csv called with type: {type(corrected_sentences_data)}")
    
    # Handle different input formats
    if isinstance(corrected_sentences_data, dict):
        # If it's a dict with 'corrected_sentences' key
        if "corrected_sentences" in corrected_sentences_data:
            sentences_list = corrected_sentences_data["corrected_sentences"]
        else:
            # Maybe it's already the sentences list
            sentences_list = corrected_sentences_data
    elif isinstance(corrected_sentences_data, list):
        # Direct list of sentences
        sentences_list = corrected_sentences_data
    else:
        print(f"Utils: Unexpected data type: {type(corrected_sentences_data)}")
        return ""
    
    print(f"Utils: Processing {len(sentences_list)} sentences")
    
    csv_lines = []
    
    for i, sentence in enumerate(sentences_list):
        print(f"Utils: Processing sentence {i}: {type(sentence)}")
        
        # Handle different sentence formats
        if isinstance(sentence, dict):
            spanish = sentence.get("corrected_spanish", "").strip()
            english = sentence.get("corrected_english", "").strip()
        else:
            print(f"Utils: Unexpected sentence type: {type(sentence)}")
            continue
        
        # Handle commas in text by wrapping in quotes if needed
        if "," in spanish:
            spanish = f'"{spanish}"'
        if "," in english:
            english = f'"{english}"'
            
        csv_lines.append(f"{spanish},{english}")
        print(f"Utils: Added CSV line: {spanish},{english}")
    
    result = "\n".join(csv_lines)
    print(f"Utils: Final CSV output ({len(result)} characters): {result[:100]}...")
    return result


def add_csv_to_state(state: Dict[str, Any]) -> None:
    """
    Add CSV formatted output to the state based on corrected_sentences.
    
    Args:
        state: The agent state dictionary to modify
    """
    print(f"Utils: add_csv_to_state called. State type: {type(state)}")
    print(f"Utils: State keys: {list(state.keys())}")
    
    corrected_sentences = state.get("corrected_sentences")
    if corrected_sentences:
        print(f"Utils: Found corrected_sentences: {type(corrected_sentences)}")
        print(f"Utils: corrected_sentences structure: {corrected_sentences}")
        csv_output = convert_corrected_sentences_to_csv(corrected_sentences)
        state["csv_output"] = csv_output
        print(f"Utils: Added CSV output to state ({len(csv_output)} characters)")
        print(f"Utils: CSV preview: {csv_output[:200]}...")
    else:
        print("Utils: No corrected_sentences found in state") 