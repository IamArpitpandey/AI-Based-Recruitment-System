import streamlit as st
import PyPDF2


# -------- PDF TEXT --------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text().lower()
    return text


# -------- SIMPLE ANALYZER --------
def analyze_resume(resume, job_desc):
    job_words = set(job_desc.lower().split())
    resume_words = set(resume.split())

    matched = job_words.intersection(resume_words)

    score = len(matched) / len(job_words) * 100 if job_words else 0

    if score > 40:
        decision = "✅ Selected"
    else:
        decision = "❌ Rejected"

    return decision, score, matched


# -------- MAIN APP --------
def main():
    st.title("🚀 AI Recruitment System (Free Mode)")

    st.info("⚡ Running in FREE mode (No API used)")

    file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd = st.text_area("Job Description")

    if st.button("Analyze"):
        if not file or not jd:
            st.warning("Upload resume + enter job description")
            return

        with st.spinner("Analyzing..."):
            resume_text = extract_text_from_pdf(file)

            decision, score, matched = analyze_resume(resume_text, jd)

        st.success("Done")

        st.subheader("Result")
        st.write(decision)
        st.write(f"Match Score: {score:.2f}%")

        st.subheader("Matched Skills")
        st.write(", ".join(list(matched)[:20]))


if __name__ == "__main__":
    main()