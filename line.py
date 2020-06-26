import os


lines = 0


def compute_lines(path_dir):
    global lines
    for path in os.listdir(path_dir):
        path = os.path.join(path_dir, path)
        if os.path.isfile(path):
            if path.endswith(".py"):
                with open(path, "r", encoding="utf-8") as f:
                    lines += len(f.readlines())
        if os.path.isdir(path):
            if "test" not in path and ".venv" not in path:
                compute_lines(path)


if __name__ == "__main__":
    compute_lines(".")
    print("源代码共有：", lines, "行")
