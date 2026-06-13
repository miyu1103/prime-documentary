# LLM Output Validation

- Structured LLM output must validate against a versioned schema.
- Invalid output is repaired within bounded attempts or fails explicitly.
- Never loosen a schema only to accept one bad output.
- Confidence must include basis and threshold action.
- Critical claims require independent review.
