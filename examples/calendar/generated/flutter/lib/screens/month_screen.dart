import 'package:flutter/material.dart';

import '../widgets/shared.dart';

class MonthScreen extends StatelessWidget {
  const MonthScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF64748B),
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(
                title: Text("May 2026"),
                backgroundColor: const Color(0xFF10B981),
                foregroundColor: const Color(0xFFFFFFFF),
              ),
              Row(
                children: [
                  Text(
                    "Mon",
                    style: TextStyle(fontSize: 12.0, color: const Color(0xFF64748B)),
                  ),
                  Text(
                    "Tue",
                    style: TextStyle(fontSize: 12.0, color: const Color(0xFF64748B)),
                  ),
                  Text(
                    "Wed",
                    style: TextStyle(fontSize: 12.0, color: const Color(0xFF64748B)),
                  ),
                  Text(
                    "Thu",
                    style: TextStyle(fontSize: 12.0, color: const Color(0xFF64748B)),
                  ),
                  Text(
                    "Fri",
                    style: TextStyle(fontSize: 12.0, color: const Color(0xFF64748B)),
                  ),
                  Text(
                    "Sat",
                    style: TextStyle(fontSize: 12.0, color: const Color(0xFF64748B)),
                  ),
                  Text(
                    "Sun",
                    style: TextStyle(fontSize: 12.0, color: const Color(0xFF64748B)),
                  ),
              ],
              ),
              ListView(
                children: [
                  ListTile(
                    title: Text("1"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("2"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("3"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("4"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("5"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("6"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("7"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("8"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("9"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("10"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("11"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("12"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("13"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("14"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("15"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("16"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("17"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("18"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("19"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("20"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("21"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("22"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("23"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("24"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("25"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("26"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("27"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                  ListTile(
                    title: Text("28"),
                    trailing: const Icon(Icons.chevron_right),
                  ),
              ],
              ),
              Card(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Next: Design review",
                      style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      "Tomorrow, 10:00",
                      style: TextStyle(fontSize: 13.0, color: const Color(0xFF64748B)),
                    ),
                  ],
                ),
                color: const Color(0xFFECFDF5),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
              ),
          ],
          ),
      ),
    );
  }
}
