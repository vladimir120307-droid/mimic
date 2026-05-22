# Examples

This folder will hold reference inputs and the code mimic generates for them. Each example is a self-contained subfolder:

```
examples/
  login_screen/
    input.png
    flutter/
      lib/main.dart
      lib/screens/login_screen.dart
    notes.md
```

`notes.md` describes:

- Source of the screenshot / recording (must be either original or with clear rights to redistribute)
- What the example demonstrates (specific widget kinds, layouts, edge cases)
- Quality assessment (what looks good, what needs improvement)

Examples double as regression fixtures — see `python/tests/test_examples.py` (planned for v0.2).
