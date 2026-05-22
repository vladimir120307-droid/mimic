# Security policy

## Reporting vulnerabilities

Please report security vulnerabilities privately via email to `security@mimic.dev`. Do **not** open a public issue or pull request for security problems.

When reporting, include:

1. A description of the issue
2. Steps to reproduce (input files, commands, environment)
3. Impact assessment (what an attacker could do)
4. Any suggested mitigations

You will receive an acknowledgement within 72 hours. We aim to ship a fix within 14 days for high-severity issues, sooner for critical ones.

## Supported versions

| Version  | Supported |
| -------- | --------- |
| 0.x      | ⚠️ Pre-release, best effort |
| 1.x      | ✅ When released, current minor |

## Threat model

mimic processes images of the user's screen. Sensitive content may include:

- API keys, passwords, or tokens visible on screen during recording
- Personal information in browser windows or messaging apps
- Confidential documents

**Mitigations users should know about:**

- Frames are buffered in memory and not written to disk unless the user explicitly saves a recording.
- When using a cloud vision provider (Claude, GPT-4V), frame contents leave the user's machine and are subject to that provider's policies. Use the local-model option for fully offline operation (planned for v0.4).
- The native capture layer requires the OS-level capture permission. mimic respects denials.
