import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFFFFF),
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(
                backgroundColor: const Color(0xFF6E56CF),
                foregroundColor: const Color(0xFFFFFFFF),
              ),
              Card(
                child: Text(
                  "Good morning, Vladimir",
                  style: TextStyle(fontSize: 22.0, fontWeight: FontWeight.bold),
                ),
                color: const Color(0xFFEEF2FF),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
              ),
              ListView(
                children: [
                  ListTile(
                    title: const Text("Recent activity"),
                    onTap: () => Navigator.pushNamed(context, "/details"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: const Text("Saved projects"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: const Text("Settings"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
              ],
              ),
              FloatingActionButton(
                onPressed: () => Navigator.pushNamed(context, "/details"),
                child: const Icon(Icons.add),
                backgroundColor: const Color(0xFF6E56CF),
              ),
          ],
          ),
      ),
    );
  }
}
