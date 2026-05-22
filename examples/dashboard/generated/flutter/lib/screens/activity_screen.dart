import 'package:flutter/material.dart';

class ActivityScreen extends StatelessWidget {
  const ActivityScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(),
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
