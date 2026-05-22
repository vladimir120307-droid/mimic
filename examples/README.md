# Examples

Each subfolder contains a reproducible example: notes explaining the input,
and the actual generated output across all three targets (Flutter, HTML, React).
You can browse the generated files directly on GitHub or clone and run them locally.

| Example                              | Screens | Targets shown            |
| ------------------------------------ | ------- | ------------------------ |
| [login](login/notes.md)              | 1       | flutter, html, react     |
| [dashboard](dashboard/notes.md)      | 2       | flutter, html, react     |

## Regenerating the outputs

```bash
# requires mimic-cli installed
for fixture in login dashboard; do
  for target in flutter html react; do
    mimic gen any.png \
      --provider mock:$fixture \
      --target $target \
      --out examples/$fixture/generated/$target
  done
done
```

These outputs are also used as regression fixtures in
`python/tests/test_mock_vision.py`.

## Adding your own example

1. Capture a screenshot of a UI you want to reproduce.
2. Run mimic against it: `mimic gen screen.png --target flutter --out examples/<name>/generated/flutter`.
3. Write a `notes.md` describing what the example demonstrates and any quality observations.
4. Open a PR — examples are how we grow the test corpus and the gallery.
