import cv2
import base64
from openai import OpenAI

class SupervisorAgent:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key, base_url="https://zenmux.ai/api/v1")

    def get_frame_b64(self, video_path):
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_MSEC, 1500) 
        success, frame = cap.read()
        if not success: return None
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode('utf-8')

    def analyze(self, video_path, sop, history):
        img_b64 = self.get_frame_b64(video_path)
        if not img_b64: return "Vision Error: Could not process video."

        prompt = f"""
        ROLE: Industrial Supervisor. 
        SOP: {sop}
        PREVIOUS HISTORY: {history}
        
        TASK: Analyze this shift. Check if current issues match past history. 
        Write a professional handover report.
        """
        
        try:
            # TRYING STEPFUN MODEL (Usually has a separate free quota)
            response = self.client.chat.completions.create(
                model="stepfun/step-3.7-flash-free", 
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Model Error: {str(e)}. \n\nTip: If you see 'Rate Limit', wait 60 seconds or try a different free model name."