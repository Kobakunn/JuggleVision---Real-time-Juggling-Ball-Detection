from pathlib import Path

name = "train"

folder = Path(f"../data/dataset/labels/{name}")

for file in folder.glob("*.txt"):
    new_name = file.name.split("-", 1)[1]
    new_path = file.with_name(new_name)

    file.rename(new_path)

print("ファイル名の変更が完了しました")