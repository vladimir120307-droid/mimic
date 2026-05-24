import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class ActivityScreen extends StatelessWidget {
  const ActivityScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFFFFF),
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(
                title: Text("Recent activity"),
                backgroundColor: const Color(0xFF6E56CF),
                foregroundColor: const Color(0xFFFFFFFF),
              ),
              Text(
                "No activity yet — start recording to see something here",
                style: TextStyle(fontSize: 15.0, color: const Color(0xFF94A3B8)),
              ),
          ],
          ),
      ),
    );
  }
}
