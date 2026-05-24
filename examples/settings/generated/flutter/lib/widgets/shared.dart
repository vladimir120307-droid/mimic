import 'package:flutter/material.dart';

class _Shared1 extends StatelessWidget {
  _Shared1({super.key, required this.text});

  final String text;

  @override
  Widget build(BuildContext context) {
    return
      Row(
        children: [
          Text(
            text,
            style: TextStyle(fontSize: 15.0),
          ),
          Switch(
            value: true,
            onChanged: (_) {},
          ),
      ],
      );
  }
}
