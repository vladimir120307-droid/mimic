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
              Container(
                decoration: BoxDecoration(color: const Color(0xFFE2E8F0)),
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
                child: const Text("Add to cart"),
              ),
          ],
          ),
      ),
    );
  }
}
