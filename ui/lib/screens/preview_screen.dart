import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter_highlight/flutter_highlight.dart';
import 'package:flutter_highlight/themes/atom-one-dark.dart';

import '../app.dart';

class PreviewScreen extends StatefulWidget {
  const PreviewScreen({super.key, required this.generatedFiles});

  final List<GeneratedFile> generatedFiles;

  @override
  State<PreviewScreen> createState() => _PreviewScreenState();
}

class _PreviewScreenState extends State<PreviewScreen> {
  int _selected = 0;

  Future<void> _export() async {
    final dir = await FilePicker.platform.getDirectoryPath();
    if (dir == null) return;
    // TODO: write each file under dir, preserving relative path
  }

  @override
  Widget build(BuildContext context) {
    if (widget.generatedFiles.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: const Text('Preview')),
        body: const Center(child: Text('No files generated yet.')),
      );
    }
    final file = widget.generatedFiles[_selected];
    return Scaffold(
      appBar: AppBar(
        title: const Text('Preview'),
        actions: [
          IconButton(
            icon: const Icon(Icons.save_alt),
            tooltip: 'Export',
            onPressed: _export,
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: Row(
        children: [
          SizedBox(
            width: 240,
            child: ListView.builder(
              itemCount: widget.generatedFiles.length,
              itemBuilder: (context, i) {
                final f = widget.generatedFiles[i];
                return ListTile(
                  selected: i == _selected,
                  dense: true,
                  title: Text(f.path, overflow: TextOverflow.ellipsis),
                  onTap: () => setState(() => _selected = i),
                );
              },
            ),
          ),
          const VerticalDivider(width: 1),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: HighlightView(
                file.content,
                language: file.language,
                theme: atomOneDarkTheme,
                textStyle: const TextStyle(
                  fontFamily: 'monospace',
                  fontSize: 13,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
