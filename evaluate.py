import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def analyze_answer(correct_answer, user_answer):
    prompt = f"""You are a technical interviewer evaluating a candidate's answer.

Reference answer: {correct_answer}
Candidate's answer: {user_answer}

Judge correctness and completeness of meaning, not exact wording or exact
keyword overlap. Give credit for correct ideas expressed in different words.

Respond ONLY with valid JSON, no extra text, in exactly this format:

{{
  "score": <integer 0-100>,
  "key_points_covered": [<short list of correct concepts the candidate's answer demonstrates>],
  "feedback": "<one short sentence summarizing the evaluation>"
}}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=90,
        )

        result = json.loads(response.json()["response"])

        score = int(result.get("score", 0))
        matched = result.get("key_points_covered", [])
        feedback = result.get("feedback", f"Answer matches {score}%.")

    except Exception:
        score = 0
        matched = []
        feedback = "AI evaluation unavailable — check that Ollama is running."

    return {
        "match_score": score,
        "matched_keywords": matched,
        "summary": feedback,
    }