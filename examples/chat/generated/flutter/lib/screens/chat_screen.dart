import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class ChatScreen extends StatelessWidget {
  const ChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFFFFF),
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(
                title: Text("Anna"),
                backgroundColor: const Color(0xFF0EA5E9),
                foregroundColor: const Color(0xFFFFFFFF),
              ),
              Card(
                color: const Color(0xFFFFFFFF),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
              ),
              Card(
                color: const Color(0xFF0EA5E9),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
              ),
              Card(
                color: const Color(0xFFFFFFFF),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
              ),
              TextField(
                decoration: const InputDecoration(hintText: "Type a message", border: OutlineInputBorder()),
              ),
              FloatingActionButton(
                onPressed: () {},
                child: const Icon(Icons.send),
                backgroundColor: const Color(0xFF0EA5E9),
              ),
          ],
          ),
      ),
    );
  }
}
