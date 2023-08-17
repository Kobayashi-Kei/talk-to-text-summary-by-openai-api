# talk-to-text-summary-by-openai-api

OpenAI Whisper を使って mp3 データを文字起こし，ChatGPT で整形，要約するプログラムです．

## requirements

- ffmpeg
  - mac os で homebrew が入っている場合: `brew install ffmpeg`
- pip
  - openai
  - subprocess
  - pydub
  - ffmpeg

## 実行手順

1. OpenAI API Key を 記入した，apikey.txt ファイルを作成．
2. `mkdir data`
3. `mkdir data/voice_data`
4. `data/voice_data` に mp3 または m4a ファイルを設置
5. `transcript.py` の `dirPath=` を "voice_data"，`fileName=`を 3. で設置した音声ファイルの名前にする．（拡張子含む，例 hogehoge.mp3
6. `python3 transcript.py`

## 実装の参考リンク

https://openai.com/blog/introducing-chatgpt-and-whisper-apis

https://www.watch.impress.co.jp/docs/topic/1493886.html

https://zenn.dev/k_kind/articles/chatgpt-api-q-and-a
