# Word DateStamp Tool (Python)

指定したWordファイルに YYYYMMDD_ 形式の日付プレフィックスを付けてコピーを作成するPythonスクリプトです。

## Features
- Wordファイル（.doc / .docx）のみ対応
- 既に同名ファイルがある場合は _1, _2 を自動付与
- 元ファイルは保持

## Usage
python datestamp.py report.docx

上記コマンドを実行すると、例えば2026年3月1日の場合、
20260301_report.docx
という名前のコピーが同じフォルダ内に作成されます。
