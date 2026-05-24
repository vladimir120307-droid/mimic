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
                title: Text("Shop"),
                backgroundColor: const Color(0xFFFFFFFF),
                foregroundColor: const Color(0xFF0F172A),
              ),
              TextField(
                decoration: const InputDecoration(hintText: "Search products", border: OutlineInputBorder()),
              ),
              Stack(
                children: [
                  _Shared1(image: "https://picsum.photos/seed/linen/400/400", text: "Linen shirt", text2: "$48"),
                  _Shared1(image: "https://picsum.photos/seed/sweater/400/400", text: "Knit sweater", text2: "$72"),
                  _Shared1(image: "https://picsum.photos/seed/coat/400/400", text: "Wool coat", text2: "$195"),
                  _Shared1(image: "https://picsum.photos/seed/trousers/400/400", text: "Cotton trousers", text2: "$56"),
              ],
              ),
          ],
          ),
      ),
    );
  }
}
