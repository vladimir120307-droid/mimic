import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFFFFF),
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(
                title: Text("Settings"),
                backgroundColor: const Color(0xFFFFFFFF),
                foregroundColor: const Color(0xFF0F172A),
              ),
              Card(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Vladimir",
                      style: TextStyle(fontSize: 18.0, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      "vladimir@example.com",
                      style: TextStyle(fontSize: 13.0, color: const Color(0xFF64748B)),
                    ),
                  ],
                ),
                color: const Color(0xFFFFFFFF),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
              ),
              Card(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _Shared1(text: "Push notifications"),
                    _Shared1(text: "Email digest"),
                    _Shared1(text: "Do not disturb"),
                  ],
                ),
                color: const Color(0xFFFFFFFF),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
              ),
              FilledButton(
                onPressed: () {},
                style: FilledButton.styleFrom(backgroundColor: const Color(0xFFE11D48), foregroundColor: const Color(0xFFFFFFFF)),
                child: Text("Sign out"),
              ),
          ],
          ),
      ),
    );
  }
}
