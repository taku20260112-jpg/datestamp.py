import sys
# 標準モジュールsysを読み込む
 # モジュールとは、関数や変数・クラスを入れる入れ物
  # クラスとは、どのようなデータと機能を持つかを定義した設計書
 # sysは、「今動いているPythonそのものの状態」を教えてくれるモジュール
  #たとえば、どんな命令（引数）でこのプログラムが起動されたか（sys.argv）
import shutil
# shutilとは、ファイルのコピーや移動を行う標準モジュール
from datetime import datetime
# datetime モジュールの中から datetime クラスだけを取り出し、読み込む
from pathlib import Path
# pathlibとは、ファイルやディレクトリのパスを扱うための標準モジュール
 # Pathクラスは、ファイルやディレクトリのパスを文字列ではなくオブジェクトとして扱うためのクラス
  #オブジェクトとは、データと機能を持つもの（機能付きの値）
WORD_EXTENSIONS = {".doc", ".docx"}
# WORD_EXTENSIONSは、Wordファイルの拡張子を定義
# このプログラムで引数をWordに限定するための布石

def next_available_path(path: Path) -> Path:
# defは、関数を定義するためのキーワード
 # define（定義する）
# next_available_pathは関数名
# path: Path は「path には Pathオブジェクトが入る」
 # path は変数名
 # Path は型（クラス）
# -> Path は戻り値の型ヒントです。
 #「この関数は最終的に Path 型を返します」
    if not path.exists():
        return path
    # 「これから作る予定のファイル名が既存ファイルと重複していないか」を確認
    # まず元の候補名が空いていれば、そのまま使う
    for i in range(1, 10000):
    # range(1, 10000)は、1以上10000未満の整数列
    # 1〜9999 の番号を使って候補名を作る
        candidate = path.with_name(f"{path.stem}_{i}{path.suffix}")
        # 同じフォルダのまま、連番付きの候補ファイル名を作る
        # 例: 20260301_議事録.docx -> 20260301_議事録_1.docx
        if not candidate.exists():
            return candidate
            # その候補名のファイルがまだ存在しなければ
            # 空いている候補が見つかったら返す

    raise FileExistsError("作成可能なファイル名が見つかりませんでした")
    #raiseは、例外を発生させるためのキーワード
    # FileExistsErrorは、ファイルが既に存在していることを示す例外クラス
    # もし10000個の候補を試しても空いているファイル名が見つからなかった場合に、この例外を発生させる


def create_dated_word_copy(file_path: Path) -> Path:
    #def:関数を定義するキーワード
    #create_dated_word_copy:関数名（意味: 日付付きWordコピーを作る）
    #(file_path: Path):入力引数は file_path。Path 型を想定
    #-> Path:戻り値も Path 型（作成したコピー先パス）
    # 入力チェック1: 指定されたパスが実在するか
    if not file_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
    # 入力チェック2: パスが「ファイル」か（フォルダは不可）
    if not file_path.is_file():
        raise ValueError(f"ファイルではありません: {file_path}")
    # 入力チェック3: 拡張子が Word(.doc / .docx) か
    # lower() にしているので .DOCX のような大文字拡張子も許可される
    if file_path.suffix.lower() not in WORD_EXTENSIONS:
        raise ValueError("Wordファイル（.doc / .docx）を指定してください")

    stamp = datetime.now().strftime("%Y%m%d")
    #　メソッドはデータ付き関数
    # datetimeクラスの now() メソッドで「今の日時」を datetime型で取得する
    # 取得した日時を strftime("%Y%m%d") メソッドで「YYYYMMDD」形式の文字列に変換する
    # 例: 2026-03-01 なら "20260301"
    prefix = f"{stamp}_"
    # 日付文字列(stamp)の後ろに "_" を付けて、ファイル名先頭用の文字列を作る
    
    if file_path.name.startswith(prefix):
        target_name = file_path.name
    else:
        target_name = prefix + file_path.name
    # 日付プレフィックスの二重付けを防ぐための分岐
    # すでに YYYYMMDD_ で始まっていればそのまま使い、
    # まだ付いていなければ先頭に付ける
     # Pathの標準属性 .name で「ファイル名だけ」を取り出す
     # 取り出した文字列に対して、strの標準メソッド startswith(prefix) を使い、
     # ファイル名が日付プレフィックス（例: 20260301_）で始まっているかを判定する

    target_path = next_available_path(file_path.with_name(target_name))
     # 1) with_name()※標準メソッド: 同じフォルダのまま、ファイル名だけ target_name に差し替えて
     #    「コピー先の候補パス」を作る
     # 2) next_available_path()※自作関数: その候補が重複していれば _1, _2 ... を付けて
     #    「実際に使える最終パス」を返す
    shutil.copy2(file_path, target_path)
    return target_path
    # 標準モジュール shutil の copy2() を使って、
    # 元ファイル(file_path)を、決定したコピー先(target_path)へコピーする
    # file_path = コピー元のパス / target_path = 新しく作るコピー先のパス
    # （原本は残したまま、日付付きファイルを新規作成する）

if len(sys.argv) < 2:
    print("使い方: python datestamp.py <Wordファイルのパス>")
    sys.exit(1)
    # sys.argv は実行時引数の配列で、先頭(sys.argv[0])にはスクリプト名が入る
    # そのため len(sys.argv) < 2 は「ファイルパス引数(sys.argv[1])が渡されていない」状態

path = Path(sys.argv[1]).expanduser()
# コマンドライン引数の2番目(sys.argv[1])には、ユーザーが渡したファイルパス文字列が入る
# その文字列を Path(...) で Pathオブジェクトに変換し、
# exists() / is_file() などの Path標準機能を使える形にする
# さらに expanduser() で "~"  を使った省略を、実際のフルパスに直す

# ここから実処理を実行する
# try: コピー作成を試し、成功したら作成先パス(result)を表示する
try:
    result = create_dated_word_copy(path)
    print(f"完了: コピーを作成しました -> {result}")
# except: 実行中にエラーが起きた場合は、エラー内容を表示して異常終了する
except Exception as e:
    print(f"エラー: {e}")
    sys.exit(1)
