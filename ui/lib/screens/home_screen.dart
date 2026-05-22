import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../widgets/target_selector.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('mimic')),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 720),
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Turn your screen into code.',
                  style: theme.textTheme.displaySmall?.copyWith(fontWeight: FontWeight.w700),
                ),
                const SizedBox(height: 12),
                Text(
                  'Record a screen, drop a screenshot — get Flutter, HTML, or React.',
                  style: theme.textTheme.bodyLarge?.copyWith(
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                ),
                const SizedBox(height: 32),
                const TargetSelector(),
                const SizedBox(height: 32),
                Row(
                  children: [
                    FilledButton.icon(
                      onPressed: () => context.go('/capture'),
                      icon: const Icon(Icons.fiber_manual_record),
                      label: const Text('Record screen'),
                    ),
                    const SizedBox(width: 12),
                    OutlinedButton.icon(
                      onPressed: () {
                        // TODO: file picker → pipeline.run
                      },
                      icon: const Icon(Icons.image_outlined),
                      label: const Text('Open screenshot'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
