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
                  Card(
                    child: Image.network(
                      "https://picsum.photos/seed/linen/400/400",
                    ),
                    color: const Color(0xFFFFFFFF),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12.0)),
                  ),
                  Card(
                    child: Image.network(
                      "https://picsum.photos/seed/sweater/400/400",
                    ),
                    color: const Color(0xFFFFFFFF),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12.0)),
                  ),
                  Card(
                    child: Image.network(
                      "https://picsum.photos/seed/coat/400/400",
                    ),
                    color: const Color(0xFFFFFFFF),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12.0)),
                  ),
                  Card(
                    child: Image.network(
                      "https://picsum.photos/seed/trousers/400/400",
                    ),
                    color: const Color(0xFFFFFFFF),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12.0)),
                  ),
              ],
              ),
          ],
          ),
      ),
    );
  }
}
