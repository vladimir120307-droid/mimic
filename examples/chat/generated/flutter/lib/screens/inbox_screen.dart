import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class InboxScreen extends StatelessWidget {
  const InboxScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFFFFF),
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(
                title: const Text("Messages"),
                backgroundColor: const Color(0xFF0EA5E9),
                foregroundColor: const Color(0xFFFFFFFF),
              ),
              TextField(
                decoration: const InputDecoration(hintText: "Search conversations", border: OutlineInputBorder()),
              ),
              ListView(
                children: [
                  ListTile(
                    title: const Text("Anna"),
                    onTap: () => Navigator.pushNamed(context, "/chat"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: const Text("Boris"),
                    onTap: () => Navigator.pushNamed(context, "/chat"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: const Text("Team"),
                    onTap: () => Navigator.pushNamed(context, "/chat"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: const Text("Mike"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: const Text("Family"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
              ],
              ),
          ],
          ),
      ),
    );
  }
}
