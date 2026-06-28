import os
from datetime import datetime

class StorageManager:
    def __init__(self):
        self.archive_dir = "data/reports"
        self.sop_file = "data/sop.txt"
        os.makedirs(self.archive_dir, exist_ok=True)
        
    def save_sop(self, text):
        with open(self.sop_file, "w", encoding="utf-8", errors="replace") as f:
            f.write(text)
        return "✅ SOP Updated Successfully"
            
    def load_sop(self):
        if os.path.exists(self.sop_file):
            with open(self.sop_file, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        return "1. Monitor Conveyor Flow\n2. Report Red Light Alerts"

    def archive_report(self, report_text):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"{self.archive_dir}/report_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8", errors="replace") as f:
            f.write(report_text)
        return filename

    def get_report_list(self):
        if not os.path.exists(self.archive_dir): return []
        files = sorted(os.listdir(self.archive_dir), reverse=True)
        return [[f] for f in files]

    def get_report_content(self, filename):
        path = os.path.join(self.archive_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        return "File not found."

    def get_file_path(self, filename):
        return os.path.join(self.archive_dir, filename)

    def get_history(self, limit=5):
        if limit <= 0:
            return "No history requested."
        if not os.path.exists(self.archive_dir): return "Archive empty."
        
        files = sorted(os.listdir(self.archive_dir), reverse=True)
        history = ""
        # We take the number of files requested by the slider
        for f in files[:limit]:
            try:
                # errors="replace" prevents the crash if an old file exists
                with open(os.path.join(self.archive_dir, f), "r", encoding="utf-8", errors="replace") as content:
                    history += f"📌 {f}\n{content.read()}\n{'-'*30}\n"
            except Exception:
                continue
        return history if history else "No previous reports found."