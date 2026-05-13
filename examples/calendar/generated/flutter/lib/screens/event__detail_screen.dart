import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class Event DetailScreen extends StatelessWidget {
  const Event DetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF64748B),
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(
                title: const Text("Design review"),
                backgroundColor: const Color(0xFF10B981),
                foregroundColor: const Color(0xFFFFFFFF),
              ),
              Text(
                "Friday May 22, 10:00 — 11:00",
                style: TextStyle(fontSize: 16.0),
              ),
              Text(
                "Conference room B / Zoom",
                style: TextStyle(fontSize: 14.0, color: const Color(0xFF64748B)),
              ),
              FilledButton(
                onPressed: () {},
                style: FilledButton.styleFrom(backgroundColor: const Color(0xFF10B981), foregroundColor: const Color(0xFFFFFFFF)),
                child: const Text("Join meeting"),
              ),
          ],
          ),
      ),
    );
  }
}
