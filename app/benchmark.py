"""OCR benchmark for synthetic or owned local test images only."""
import argparse
import csv
from pathlib import Path
import cv2
import pytesseract

def recognize_fixture(path: str) -> str:
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Cannot read fixture image: {path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return pytesseract.image_to_string(processed, config="--psm 7").strip()

def run_benchmark(csv_path: str) -> dict:
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            image_path = Path(row["image_path"])
            if not image_path.is_absolute():
                image_path = Path(csv_path).parent / image_path
            predicted = recognize_fixture(str(image_path))
            expected = row["expected_text"].strip()
            rows.append(predicted == expected)
    total = len(rows)
    return {"total": total, "correct": sum(rows), "accuracy": sum(rows) / total if total else 0.0}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="CSV of owned/synthetic test fixtures")
    args = parser.parse_args()
    print(run_benchmark(args.csv))
