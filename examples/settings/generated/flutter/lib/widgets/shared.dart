import 'package:flutter/material.dart';

class _Shared1 extends StatelessWidget {
  const _Shared1({super.key});

  @override
  Widget build(BuildContext context) {
    return
      Row(
        children: [
          Text(
            "Push notifications",
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
