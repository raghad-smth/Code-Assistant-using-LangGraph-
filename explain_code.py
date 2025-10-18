"""
Code explanation chain.

Given user-provided code (or extracted code), produce:
  - Short, plain-language overall summary (1-3 sentences)
  - A line-by-line or small-block explanation (concise steps)
Keep language simple and accessible (aim at average reader).
"""

from typing import Dict, Any
from loading import get_llm

EXPLAIN_PROMPT = """
You are a helpful assistant that explains code simply and clearly.
Requirements:
- First: give a short overall summary (1-3 sentences).
- Then: provide a line-by-line explanation (or block-wise explanation if functions are large).
- Keep explanations simple and avoid jargon. Use small steps and examples where helpful.
- Do NOT produce code corrections unless asked.

Code to explain:
---
{code}
---
"""

def explain_code(code: str, llm: Any = None) -> Dict[str, Any]:
    llm = llm or get_llm(model_name="gpt-4o-mini")
    prompt = EXPLAIN_PROMPT.format(code=code)
    
    # Run LLM and get text output
    response = llm.invoke(prompt)
    explanation_text = response.content if hasattr(response, "content") else str(response)

    return {"explanation": explanation_text, "raw": response}

# --- Test ---
# if __name__ == "__main__":
#     test_code = """
# def factorial(n):
#     if n == 0:
#         return 1
#     return n * factorial(n - 1)
# """
#     result = explain_code(test_code)
#     print("\n--- Explanation ---\n")
#     print(result["explanation"])
