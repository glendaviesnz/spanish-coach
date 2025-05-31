#!/usr/bin/env python3

"""Test script to verify CSV conversion works with the actual data structure."""

import json
from spanish_coach.utils import convert_corrected_sentences_to_csv

# Sample data structure from the grammar checker output
sample_data = {
    "corrected_sentences": [
        {
            "original_spanish": "Tengo un coche nuevo.",
            "corrected_spanish": "Tengo un coche nuevo.",
            "original_english": "I have a new car.",
            "corrected_english": "I have a new car.",
            "corrections_made": [],
            "grammar_notes": None
        },
        {
            "original_spanish": "Tienes mucha suerte.",
            "corrected_spanish": "Tienes mucha suerte.",
            "original_english": "You have a lot of luck.",
            "corrected_english": "You have a lot of luck.",
            "corrections_made": [],
            "grammar_notes": None
        },
        {
            "original_spanish": "Ella tiene un perro.",
            "corrected_spanish": "Ella tiene un perro.",
            "original_english": "She has a dog.",
            "corrected_english": "She has a dog.",
            "corrections_made": [],
            "grammar_notes": None
        }
    ],
    "total_corrections": 0,
    "summary": None
}

if __name__ == "__main__":
    print("Testing CSV conversion...")
    csv_output = convert_corrected_sentences_to_csv(sample_data)
    print("CSV Output:")
    print(csv_output)
    print("\nWith line breaks visible:")
    print(repr(csv_output)) 