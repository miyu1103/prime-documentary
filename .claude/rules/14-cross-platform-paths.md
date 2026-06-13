# Cross-platform Paths

- Store logical artifact URIs, not Windows or macOS absolute paths.
- Use pathlib or equivalent path-safe APIs.
- Atomic writes use temporary suffix then rename.
- Transfer completion requires checksum validation.
- Code and tests must account for case sensitivity and path separator differences.
