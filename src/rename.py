from pathlib import Path

folder = Path("../data/dataset/labels/train")

for file in folder.glob("*.txt"):
    prefix, sep, suffix = file.name.partition("-")

    if sep == "":
        continue

    file.rename(file.with_name(suffix))