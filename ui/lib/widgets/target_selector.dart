import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

enum TargetFramework { flutter, html, react }

final targetProvider = StateProvider<TargetFramework>((_) => TargetFramework.flutter);

class TargetSelector extends ConsumerWidget {
  const TargetSelector({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final current = ref.watch(targetProvider);
    return SegmentedButton<TargetFramework>(
      segments: const [
        ButtonSegment(
          value: TargetFramework.flutter,
          label: Text('Flutter'),
          icon: Icon(Icons.flutter_dash),
        ),
        ButtonSegment(
          value: TargetFramework.html,
          label: Text('HTML'),
          icon: Icon(Icons.code),
        ),
        ButtonSegment(
          value: TargetFramework.react,
          label: Text('React'),
          icon: Icon(Icons.bolt),
        ),
      ],
      selected: {current},
      onSelectionChanged: (s) => ref.read(targetProvider.notifier).state = s.first,
    );
  }
}
