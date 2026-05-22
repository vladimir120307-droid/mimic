import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child:
          Column(
            children: [
              AppBar(),
              Card(
                child: Text(
                  "Good morning, Vladimir",
                  style: TextStyle(fontSize: 22.0, fontWeight: FontWeight.bold),
                ),
              ),
              ListView(
                children: [
                  ListTile(),
                  ListTile(),
                  ListTile(),
              ],
              ),
              FloatingActionButton(),
          ],
          ),
      ),
    );
  }
}
