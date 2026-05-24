import 'package:flutter/material.dart';

class _Shared1 extends StatelessWidget {
  _Shared1({super.key, required this.image, required this.text, required this.text2});

  final String image;
  final String text;
  final String text2;

  @override
  Widget build(BuildContext context) {
    return
      Card(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Image.network(
              image,
            ),
            Text(
              text,
              style: TextStyle(fontSize: 14.0, fontWeight: FontWeight.w600),
            ),
            Text(
              text2,
              style: TextStyle(fontSize: 15.0, fontWeight: FontWeight.bold, color: const Color(0xFFE11D48)),
            ),
          ],
        ),
        color: const Color(0xFFFFFFFF),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12.0)),
      );
  }
}
