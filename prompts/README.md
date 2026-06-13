# Prompt Library

These prompts are specifications, not magic strings. They are versioned inputs to evaluation and production.

Rules:
- Keep factual generation evidence-constrained.
- Require structured output.
- Separate generator, critic, repair, and validator.
- Do not include secrets or raw provider credentials.
- Do not paste the entire project corpus into every task.
- Record prompt ID, version, model profile, input revisions, and output hash.
