import 'package:flutter/material.dart';

class _Shared1 extends StatelessWidget {
  const _Shared1({super.key});

  @override
  Widget build(BuildContext context) {
    return
      Card(
        child: Container(
          decoration: BoxDecoration(color: const Color(0xFFE2E8F0), borderRadius: BorderRadius.circular(8.0)),
        ),
        color: const Color(0xFFFFFFFF),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12.0)),
      );
  }
}
