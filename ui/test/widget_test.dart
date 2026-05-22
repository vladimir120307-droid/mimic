import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mimic_ui/widgets/target_selector.dart';

void main() {
  testWidgets('TargetSelector renders three options', (tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: Scaffold(body: TargetSelector()),
        ),
      ),
    );
    expect(find.text('Flutter'), findsOneWidget);
    expect(find.text('HTML'),    findsOneWidget);
    expect(find.text('React'),   findsOneWidget);
  });
}
