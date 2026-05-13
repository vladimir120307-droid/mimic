import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      body: SafeArea(
        child:
          Column(
            children: [
              Icon(
                Icons.bolt,
                size: 48.0,
                color: const Color(0xFF6E56CF),
              ),
              Text(
                "Welcome back",
                style: TextStyle(fontSize: 28.0, fontWeight: FontWeight.bold),
              ),
              Text(
                "Sign in to continue to your dashboard",
                style: TextStyle(fontSize: 14.0, color: const Color(0xFF64748B)),
              ),
              TextField(
                decoration: const InputDecoration(hintText: "Email address", border: OutlineInputBorder()),
              ),
              TextField(
                decoration: const InputDecoration(hintText: "Password", border: OutlineInputBorder()),
              ),
              FilledButton(
                onPressed: () {},
                style: FilledButton.styleFrom(backgroundColor: const Color(0xFF6E56CF), foregroundColor: const Color(0xFFFFFFFF)),
                child: const Text("Sign in"),
              ),
              Text(
                "Don't have an account? Create one",
                style: TextStyle(fontSize: 13.0, color: const Color(0xFF6E56CF)),
              ),
          ],
          ),
      ),
    );
  }
}
