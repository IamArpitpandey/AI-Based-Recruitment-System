import streamlit as st
from phi.agent import Agent
from phi.tools.email import EmailTools
from tools import CustomZoomTool
import google.generativeai as genai


# 🔥 Gemini Model Wrapper
class GeminiModel:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text


# 🔥 Model selector
def get_the_model():
    return GeminiModel(api_key=st.session_state.api_key)


# 🔥 Resume Analyzer
def create_resume_analyzer_agent():
    if not st.session_state.api_key:
        st.error("Please enter your Gemini API Key first.")
        return None

    model = get_the_model()

    return Agent(
        model=model,
        description="You are an expert technical recruiter.",
        instructions=[
            "Analyze resume vs job description",
            "Give selection decision (Selected/Rejected)",
            "Give improvement feedback",
            "Return clean structured response",
        ],
        markdown=True,
    )


# 🔥 Email Agent
def create_email_agent():
    return Agent(
        model=get_the_model(),
        tools=[
            EmailTools(
                receiver_email=st.session_state.candidate_email,
                sender_email=st.session_state.email_sender,
                sender_name=st.session_state.company_name,
                sender_passkey=st.session_state.email_passkey,
            )
        ],
        description="You write professional HR emails.",
        instructions=[
            "Write clean professional email",
            "Keep friendly tone",
            "End with: best, the ai recruiting team",
        ],
        markdown=False,
    )


# 🔥 Scheduler Agent
def create_scheduler_agent():
    zoom_tools = CustomZoomTool(
        account_id=st.session_state.zoom_account_id,
        client_id=st.session_state.zoom_client_id,
        client_secret=st.session_state.zoom_client_secret,
    )

    return Agent(
        name="Interview Scheduler",
        model=get_the_model(),
        tools=[zoom_tools],
        description="Schedules interviews using Zoom.",
        instructions=[
            "Schedule interview next day",
            "Include meeting link",
            "Use proper time format",
        ],
        markdown=False,
    )