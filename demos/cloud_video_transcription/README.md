# Cloud Video Transcription Demo

This demo is a public-safe simulation of a cloud video-to-transcript workflow.
It uses fake media records and synthetic transcript text to show the processing
pattern without publishing private videos, transcripts, or source metadata.

Run from the repository root:

```bash
python3 demos/cloud_video_transcription/run_demo.py
```

The command above runs every stage. Individual stages are also available:

```bash
python3 demos/cloud_video_transcription/run_demo.py list
python3 demos/cloud_video_transcription/run_demo.py download --match seminar_01
python3 demos/cloud_video_transcription/run_demo.py transcribe
python3 demos/cloud_video_transcription/run_demo.py clean
python3 demos/cloud_video_transcription/run_demo.py prepare-corpus
```

Custom paths:

```bash
python3 demos/cloud_video_transcription/run_demo.py \
  --input demos/cloud_video_transcription/sample_cloud_listing.json \
  --out sample_outputs/cloud_video_transcription
```

Generated outputs:

- `sample_outputs/cloud_video_transcription/manifest.json`
- `sample_outputs/cloud_video_transcription/clean_transcript_excerpt.md`
- `sample_outputs/cloud_video_transcription/workflow_summary.md`
- `sample_outputs/cloud_video_transcription/corpus.json`

The demo does not call Dropbox, OpenAI, ffmpeg, or any network service.
