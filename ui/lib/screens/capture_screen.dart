import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../services/capture_service.dart';

class CaptureScreen extends ConsumerStatefulWidget {
  const CaptureScreen({super.key});

  @override
  ConsumerState<CaptureScreen> createState() => _CaptureScreenState();
}

class _CaptureScreenState extends ConsumerState<CaptureScreen> {
  bool _recording = false;
  int _remaining = 15;
  Timer? _ticker;

  @override
  void dispose() {
    _ticker?.cancel();
    super.dispose();
  }

  Future<void> _start() async {
    setState(() {
      _recording = true;
      _remaining = 15;
    });
    _ticker = Timer.periodic(const Duration(seconds: 1), (t) {
      if (!mounted) return;
      setState(() => _remaining = (_remaining - 1).clamp(0, 60));
      if (_remaining == 0) {
        t.cancel();
        _finish();
      }
    });
    await ref.read(captureServiceProvider).start(durationSeconds: 15);
  }

  Future<void> _finish() async {
    final files = await ref.read(captureServiceProvider).stopAndGenerate();
    if (!mounted) return;
    setState(() => _recording = false);
    context.go('/preview', extra: {'files': files});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Recording')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              _recording ? Icons.fiber_manual_record : Icons.radio_button_unchecked,
              size: 80,
              color: _recording ? Colors.redAccent : Theme.of(context).colorScheme.outline,
            ),
            const SizedBox(height: 24),
            Text(
              _recording ? '$_remaining s remaining' : 'Press start to record your screen',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 32),
            FilledButton.icon(
              onPressed: _recording ? null : _start,
              icon: const Icon(Icons.play_arrow),
              label: const Text('Start (15 s)'),
            ),
          ],
        ),
      ),
    );
  }
}
