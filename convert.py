import re

# ファイルパス
input_file_path = str(input("file name"))  # 元のファイル
output_file_path = 'running.svg'     # 結果を保存するファイル

# ファイルを読み込んで内容を取得
with open(input_file_path, 'r') as input_file:
    file_content = input_file.read()

# 置換を行う
modified_content = file_content.replace("sodipodi:cx","sodipodicx").replace("sodipodi:cy","sodipodicy").replace("sodipodi:rx","sodipodirx").replace("sodipodi:ry","sodipodiry").replace("sodipodi:start","sodipodistart").replace("sodipodi:end","sodipodiend").replace("sodipodi:arc-type","sodipodiarctype")

# 結果を新しいファイルに保存
with open(output_file_path, 'w') as output_file:
    output_file.write(modified_content)

print(f'"{input_file_path}" が置換され、結果が"{output_file_path}"に保存されました。')