from pathlib import Path

from analyzer import generate_summary


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    log_path = project_dir / "app.log"
    report_path = project_dir / "report.txt"

    if not log_path.exists():
        raise FileNotFoundError(
            f"Could not find {log_path}. Place app.log in the project directory and rerun."
        )

    generate_summary(log_path=log_path, report_path=report_path)
    print(f"Report generated: {report_path}")


if __name__ == "__main__":
    main()
