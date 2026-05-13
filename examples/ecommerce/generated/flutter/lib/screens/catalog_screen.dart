import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class CatalogScreen extends StatelessWidget {
  const CatalogScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFFFFF),
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(
                title: const Text("Shop"),
                backgroundColor: const Color(0xFFFFFFFF),
                foregroundColor: const Color(0xFF0F172A),
              ),
              TextField(
                decoration: const InputDecoration(hintText: "Search products", border: OutlineInputBorder()),
              ),
              Stack(
                children: [
                  const _Shared1(),
                  const _Shared1(),
                  const _Shared1(),
                  const _Shared1(),
              ],
              ),
          ],
          ),
      ),
    );
  }
}
