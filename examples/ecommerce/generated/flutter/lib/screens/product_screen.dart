import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class ProductScreen extends StatelessWidget {
  const ProductScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFFFFF),
      body: SafeArea(
        child:
          Column(
            children: [
              Image.network(
                "https://picsum.photos/seed/linen/1200/800",
              ),
              Text(
                "Linen shirt",
                style: TextStyle(fontSize: 22.0, fontWeight: FontWeight.bold),
              ),
              Text(
                "$48",
                style: TextStyle(fontSize: 18.0, color: const Color(0xFFE11D48)),
              ),
              Text(
                "Soft, breathable linen with a relaxed cut. Ethically sourced.",
                style: TextStyle(fontSize: 14.0, color: const Color(0xFF64748B)),
              ),
              FilledButton(
                onPressed: () {},
                style: FilledButton.styleFrom(backgroundColor: const Color(0xFF0F172A), foregroundColor: const Color(0xFFFFFFFF)),
                child: Text("Add to cart"),
              ),
          ],
          ),
      ),
    );
  }
}
