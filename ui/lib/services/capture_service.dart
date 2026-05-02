import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../app.dart';
import 'pipeline_service.dart';

final captureServiceProvider = Provider<CaptureService>((ref) {
  return CaptureService(ref.watch(pipelineServiceProvider));
});

class CaptureService {
  CaptureService(this._pipeline);

  final PipelineService _pipeline;
  bool _running = false;

  Future<void> start({required int durationSeconds}) async {
    if (_running) return;
    _running = true;
    await _pipeline.startRecording(durationSeconds: durationSeconds);
  }

  Future<List<GeneratedFile>> stopAndGenerate() async {
    if (!_running) return const [];
    _running = false;
    return _pipeline.stopAndGenerate();
  }
}
