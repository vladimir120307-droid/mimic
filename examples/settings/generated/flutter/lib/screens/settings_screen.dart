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
                title: const Text("Settings"),
                backgroundColor: const Color(0xFFFFFFFF),
                foregroundColor: const Color(0xFF0F172A),
              ),
              Card(
                child: Text(
                  "Vladimir",
                  style: TextStyle(fontSize: 18.0, fontWeight: FontWeight.bold),
                ),
                color: const Color(0xFFFFFFFF),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
              ),
              Card(
                child: Row(
                  children: [
                    Text(
                      "Push notifications",
                      style: TextStyle(fontSize: 15.0),
                    ),
                    Switch(
                      value: true,
                      onChanged: (_) {},
                    ),
                ],
                ),
                color: const Color(0xFFFFFFFF),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
              ),
              FilledButton(
                onPressed: () {},
                style: FilledButton.styleFrom(backgroundColor: const Color(0xFFE11D48), foregroundColor: const Color(0xFFFFFFFF)),
                child: const Text("Sign out"),
              ),
          ],
          ),
      ),
    );
  }
}
