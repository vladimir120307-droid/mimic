import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'screens/capture_screen.dart';
import 'screens/home_screen.dart';
import 'screens/preview_screen.dart';
import 'theme/app_theme.dart';

final _router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
    GoRoute(path: '/capture', builder: (_, __) => const CaptureScreen()),
    GoRoute(
      path: '/preview',
      builder: (context, state) {
        final extra = state.extra as Map<String, dynamic>? ?? const {};
        return PreviewScreen(
          generatedFiles: extra['files'] as List<GeneratedFile>? ?? const [],
        );
      },
    ),
  ],
);

class MimicApp extends ConsumerWidget {
  const MimicApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp.router(
      title: 'mimic',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light(),
      darkTheme: AppTheme.dark(),
      themeMode: ThemeMode.system,
      routerConfig: _router,
    );
  }
}

class GeneratedFile {
  const GeneratedFile({required this.path, required this.content, required this.language});

  final String path;
  final String content;
  final String language;
}
