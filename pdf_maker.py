import os
from fpdf import FPDF

INPUT_DIR = "OPTIMAL_COACH_FRAMES"
OUTPUT_FILE = "12309_coverage_report.pdf"

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

for folder in sorted(os.listdir(INPUT_DIR)):
    folder_path = os.path.join(INPUT_DIR, folder)
    if os.path.isdir(folder_path):
        for img in sorted(os.listdir(folder_path)):
            if img.endswith(".jpg"):
                pdf.add_page()
                pdf.set_font("Arial", "B", 12)
                pdf.cell(200, 10, f"Coach {folder}", ln=True, align="C")
                pdf.image(os.path.join(folder_path, img), x=10, y=30, w=180)

pdf.output(OUTPUT_FILE)
print(f"[INFO] PDF report generated: {OUTPUT_FILE}")
