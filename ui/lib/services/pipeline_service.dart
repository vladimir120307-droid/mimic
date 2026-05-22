import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;

import '../app.dart';

final pipelineServiceProvider = Provider<PipelineService>((_) {
  return PipelineService(endpoint: Uri.parse('http://127.0.0.1:54321'));
});

/// Talks to the Python orchestrator over JSON-RPC.
///
/// The Python side exposes a tiny HTTP server (started by `mimic ui-server`)
/// that accepts `start_recording`, `stop_recording`, and `generate` methods.
class PipelineService {
  PipelineService({required this.endpoint});

  final Uri endpoint;
  final http.Client _client = http.Client();

  Future<void> startRecording({required int durationSeconds}) async {
    await _rpc('start_recording', {'duration_s': durationSeconds});
  }

  Future<List<GeneratedFile>> stopAndGenerate() async {
    final response = await _rpc('stop_and_generate', const {});
    final files = (response['files'] as List<dynamic>? ?? const [])
        .cast<Map<String, dynamic>>()
        .map(
          (m) => GeneratedFile(
            path: m['path'] as String,
            content: m['content'] as String,
            language: (m['language'] as String?) ?? 'plaintext',
          ),
        )
        .toList();
    return files;
  }

  Future<Map<String, dynamic>> _rpc(String method, Map<String, dynamic> params) async {
    final body = jsonEncode({
      'jsonrpc': '2.0',
      'id': DateTime.now().millisecondsSinceEpoch,
      'method': method,
      'params': params,
    });
    final response = await _client.post(
      endpoint,
      headers: const {'content-type': 'application/json'},
      body: body,
    );
    final decoded = jsonDecode(response.body) as Map<String, dynamic>;
    if (decoded['error'] != null) {
      throw Exception('Pipeline error: ${decoded['error']}');
    }
    return (decoded['result'] as Map<String, dynamic>?) ?? const {};
  }
}
