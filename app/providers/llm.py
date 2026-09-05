import re
from openai import OpenAI
from app.core.config import get_settings

class MockAnswerProvider:
    def answer(self, question, context):
        q = question.lower()
        patterns = [
            ("maximum operating temperature", r"maximum operating temperature\s*:?\s*([^\n.]+)"),
            ("minimum operating temperature", r"minimum operating temperature\s*:?\s*([^\n.]+)"),
            ("pump a fails", r"if pump a fails,\s*([^\n.]+)"),
            ("primary cooling pump", r"if pump a fails,\s*([^\n.]+)"),
            ("low-pressure", r"if coolant pressure falls below 1\.8 bar,\s*([^\n.]+)"),
        ]
        low = context.lower()
        for keyword, pattern in patterns:
            if keyword in q:
                m = re.search(pattern, low, re.I)
                if m:
                    ans = m.group(0).strip()
                    return ans[:1].upper() + ans[1:]
        for line in context.splitlines():
            if line.strip() and not line.startswith("SOURCE="):
                return "Based on the retrieved document: " + line.strip()
        return "I could not find sufficient evidence in the retrieved documents."

class OpenAIAnswerProvider:
    def __init__(self):
        s = get_settings()
        if not s.openai_api_key: raise ValueError("OPENAI_API_KEY required")
        self.client = OpenAI(api_key=s.openai_api_key)
        self.model = s.openai_chat_model
    def answer(self, question, context):
        prompt = f"Answer ONLY from context. If insufficient, say so.\nQuestion: {question}\nContext:\n{context}"
        r = self.client.responses.create(model=self.model, input=prompt)
        return r.output_text

def get_answer_provider():
    return OpenAIAnswerProvider() if get_settings().app_mode.lower() == "openai" else MockAnswerProvider()
