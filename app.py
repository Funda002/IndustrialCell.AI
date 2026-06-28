import gradio as gr
from agent_engine import SupervisorAgent
from storage_manager import StorageManager
import os

# Init Backend
API_KEY = "sk-ai-v1-e9f9699c9972ac853cb745efad87a9df244b24837205ff38d012bcf8c24c2b3e"
agent = SupervisorAgent(API_KEY)
db = StorageManager()

# Professional Enterprise CSS
CSS = """
.header-bar {
    background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
    padding: 25px;
    border-bottom: 2px solid #22d3ee;
    margin-bottom: 20px;
    border-radius: 8px;
}
.sidebar { 
    background-color: #111827; 
    border-right: 1px solid #374151; 
    min-height: 80vh;
    padding: 20px;
}
.nav-btn { margin-bottom: 8px !important; text-align: left !important; }
.main-content { padding: 20px; background-color: #0b0f19; }
.viewer-box textarea { 
    background-color: #1f2937 !important; 
    color: #22d3ee !important; 
    font-family: 'Courier New', monospace; 
    height: 450px !important; 
}
.download-red { background-color: #dc2626 !important; color: white !important; font-weight: bold !important; }
"""

# Header HTML content
HEADER_HTML = """
<div class="header-bar">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="color: #22d3ee; margin: 0; font-size: 28px;">IndustrialCell.AI</h1>
            <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 14px;">
                Autonomous Video-Native Reasoning for the American Industrial Revolution
            </p>
        </div>
        <div style="text-align: right;">
            <div style="color: #22d3ee; font-weight: bold; font-size: 12px;">● SYSTEM ONLINE</div>
            <div style="color: #64748b; font-size: 11px;">NEURAL ENGINE v1.2.5 | REGION: US-AUSTIN</div>
            <div style="color: #64748b; font-size: 11px;">WORKFLOW: WATCH → REASON → ACT</div>
        </div>
    </div>
</div>
"""

def process_shift(video, memory_limit):
    if not video: return "Error: No video detected."
    sop = db.load_sop()
    history = db.get_history(limit=int(memory_limit))
    report = agent.analyze(video, sop, history)
    db.archive_report(report)
    return report

def load_selected_report(evt: gr.SelectData):
    filename = evt.value
    content = db.get_report_content(filename)
    path = db.get_file_path(filename)
    return content, path

with gr.Blocks(css=CSS, theme=gr.themes.Soft(primary_hue="cyan", neutral_hue="slate")) as demo:
    # Top Header Section
    gr.HTML(HEADER_HTML)
    
    with gr.Row():
        # LEFT SIDEBAR
        with gr.Column(scale=1, elem_classes="sidebar"):
            gr.Markdown("### 🛠️ NAVIGATION")
            nav_cmd = gr.Button("🚀 Command Center", elem_classes="nav-btn", variant="primary")
            nav_sop = gr.Button("🧠 Intelligence Setup", elem_classes="nav-btn", variant="secondary")
            nav_log = gr.Button("📂 Shift Archives", elem_classes="nav-btn", variant="secondary")
            gr.Markdown("---")
            gr.Markdown("🧪 **Agent Identity**\nShift Supervisor #402")
            gr.Markdown("📡 **Link Status**\nEncrypted (AES-256)")

        # MAIN CONTENT
        with gr.Column(scale=4, elem_classes="main-content"):
            
            # PAGE 1: COMMAND CENTER
            with gr.Column(visible=True) as page_cmd:
                with gr.Row():
                    v_in = gr.Video(label="Factory Visual Feed", height=500)
                    r_out = gr.Textbox(label="Agent Real-Time Reasoning", lines=22, elem_classes="viewer-box")
                run_btn = gr.Button("🚀 EXECUTE AUTONOMOUS ANALYSIS", variant="primary", size="lg")
            
            # PAGE 2: SETUP
            with gr.Column(visible=False) as page_sop:
                gr.Markdown("## 🧠 Cognitive Configuration")
                with gr.Row():
                    sop_text = gr.Textbox(label="Active SOP Directives", value=db.load_sop(), lines=12)
                    with gr.Column():
                        memory_slider = gr.Slider(0, 10, value=5, step=1, label="Historical Memory Window")
                        gr.Markdown("### How it works:\n*The agent queries the archives to find recurring patterns before making a decision.*")
                save_btn = gr.Button("Update Neural Knowledge Base", variant="secondary")
                save_msg = gr.Markdown("")
            
            # PAGE 3: ARCHIVES
            with gr.Column(visible=False) as page_log:
                gr.Markdown("## 📂 Industrial Intelligence Vault")
                with gr.Row():
                    report_df = gr.Dataframe(headers=["Filename"], datatype=["str"], value=db.get_report_list(), interactive=False)
                    with gr.Column():
                        viewer = gr.Textbox(label="Shift Content", lines=15, elem_classes="viewer-box", interactive=False)
                        d_btn = gr.DownloadButton("📥 DOWNLOAD OFFICIAL REPORT", elem_classes="download-red")

    # Nav Logic
    def show_cmd(): return {page_cmd: gr.update(visible=True), page_sop: gr.update(visible=False), page_log: gr.update(visible=False), nav_cmd: gr.update(variant="primary"), nav_sop: gr.update(variant="secondary"), nav_log: gr.update(variant="secondary")}
    def show_sop(): return {page_cmd: gr.update(visible=False), page_sop: gr.update(visible=True), page_log: gr.update(visible=False), nav_cmd: gr.update(variant="secondary"), nav_sop: gr.update(variant="primary"), nav_log: gr.update(variant="secondary")}
    def show_log(): return {page_cmd: gr.update(visible=False), page_sop: gr.update(visible=False), page_log: gr.update(visible=True), report_df: gr.update(value=db.get_report_list()), nav_cmd: gr.update(variant="secondary"), nav_sop: gr.update(variant="secondary"), nav_log: gr.update(variant="primary")}

    nav_cmd.click(show_cmd, None, [page_cmd, page_sop, page_log, nav_cmd, nav_sop, nav_log])
    nav_sop.click(show_sop, None, [page_cmd, page_sop, page_log, nav_cmd, nav_sop, nav_log])
    nav_log.click(show_log, None, [page_cmd, page_sop, page_log, report_df, nav_cmd, nav_sop, nav_log])
    
    report_df.select(load_selected_report, None, [viewer, d_btn])
    save_btn.click(db.save_sop, inputs=sop_text, outputs=save_msg)
    run_btn.click(process_shift, inputs=[v_in, memory_slider], outputs=r_out)

if __name__ == "__main__":
    demo.launch()