import subprocess


def main() -> None:
    if subprocess.call(["mypy", "."]) != 0:
        exit(1)


if __name__ == "__main__":
    main()
