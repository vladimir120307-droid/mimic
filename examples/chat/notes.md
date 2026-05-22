# Example: Chat / messaging app

A two-screen messaging flow.

- **Inbox** — sticky branded app bar, search field, list of conversations
- **Chat** — branded app bar, alternating sender bubbles, composer text field + send FAB

## Reproduce

```bash
mimic gen any.png --provider mock:chat --target flutter --out ./out
```

## What to look at

- Inbox `list_item` rows tap-navigate to the Chat screen
- The message bubbles use `card` widgets with bidirectional alignment (left for inbound, right with brand color for outbound)
- Send FAB uses an icon name (`send`) that maps to `Icons.send` in Flutter

## Limitations

- All three conversation rows tap to the same destination (`chat`) — mimic doesn't yet differentiate per-row navigation targets in fixtures
- Message timestamps not rendered (intentionally omitted from the fixture)
