import streamlit as st
import time
import random
import os
import base64
from process_resume import extract_text_from_pdf, clean_text
from matcher import calculate_match_score, get_missing_skills
from llm_writer import create_prompt, generate_cover_letter

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

icon = "logo.png" if os.path.exists("logo.png") else "🎯"
st.set_page_config(
    page_title="JobHunter",
    page_icon=icon,
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #080b14 !important;
    font-family: 'Inter', sans-serif !important;
    color: #e2e8f0 !important;
}

/* hide streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

/* ── main content padding ── */
[data-testid="stMain"] .block-container, [data-testid="stMainBlockContainer"] {
    padding: 70px 40px 40px 40px !important;
    margin-top: 0 !important;
    max-width: 100% !important;
}

/* ── NAV BAR ── */
.navbar {
    background: linear-gradient(90deg, #0d1020 0%, #111527 100%);
    border-bottom: 1px solid rgba(139, 92, 246, 0.15);
    position: fixed;
    top: 0; left: 0; right: 0;
    padding: 14px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 999;
    backdrop-filter: blur(12px);
}
.nav-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.05rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.3px;
}
.nav-logo-icon {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    box-shadow: 0 4px 14px rgba(124,58,237,0.4);
}
.nav-logo-sub { font-weight: 400; color: #94a3b8; font-size: 0.85rem; }
.nav-right { display: flex; align-items: center; gap: 10px; }
.nav-chip {
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(139,92,246,0.25);
    color: #a78bfa;
    padding: 5px 13px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
}
.nav-credits {
    background: rgba(250,204,21,0.08);
    border: 1px solid rgba(250,204,21,0.2);
    color: #fbbf24;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    display: flex; align-items: center; gap: 5px;
}
.nav-avatar {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #7c3aed, #db2777);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; color: white;
    box-shadow: 0 2px 10px rgba(124,58,237,0.3);
}

/* ── PAGE SHELL ── */
.page-shell {
    display: grid;
    grid-template-columns: 370px 1fr;
    gap: 0;
    min-height: calc(100vh - 63px);
}

/* ── LEFT PANEL ── */
.left-panel {
    background: #0c0f1d;
    border-right: 1px solid rgba(255,255,255,0.05);
    padding: 28px 22px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

/* ── RIGHT PANEL ── */
.right-panel {
    background: #080b14;
    padding: 28px 32px;
}

/* ── SECTION CARDS ── */
.scard {
    background: linear-gradient(145deg, #111527 0%, #0f1220 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.scard::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), transparent);
}
.scard-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
}
.scard-num {
    width: 24px; height: 24px;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 700; color: white;
    flex-shrink: 0;
    box-shadow: 0 3px 10px rgba(124,58,237,0.35);
}
.scard-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #e2e8f0;
    letter-spacing: -0.1px;
}

/* ── UPLOAD ZONE ── */
.upload-zone {
    border: 1.5px dashed rgba(139,92,246,0.3);
    border-radius: 12px;
    padding: 28px 20px;
    text-align: center;
    background: rgba(139,92,246,0.04);
    transition: all 0.2s;
}
.upload-zone-icon { font-size: 2.2rem; margin-bottom: 8px; display: block; }
.upload-zone-text { font-size: 0.8rem; color: #475569; line-height: 1.6; }
.upload-zone-text strong { color: #a78bfa; font-weight: 600; }

/* ── FILE CHIP ── */
.file-chip {
    display: flex; align-items: center; gap: 12px;
    background: rgba(139,92,246,0.08);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 12px;
    padding: 12px 14px;
    margin-top: 10px;
}
.file-chip-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #7c3aed22, #a855f722);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.file-chip-name { font-size: 0.82rem; color: #e2e8f0; font-weight: 500; }
.file-chip-meta { font-size: 0.72rem; color: #4ade80; margin-top: 2px; }

/* ── GENERATE BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 50%, #5b21b6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    width: 100% !important;
    cursor: pointer !important;
    letter-spacing: -0.1px !important;
    box-shadow: 0 4px 20px rgba(109,40,217,0.4), 0 1px 0 rgba(255,255,255,0.1) inset !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 28px rgba(109,40,217,0.55) !important;
    transform: translateY(-1px) !important;
}

/* ── SCORE DISPLAY ── */
.score-wrap {
    background: linear-gradient(145deg, #111527, #0f1220);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    margin-bottom: 14px;
}
.score-wrap::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(74,222,128,0.5), transparent);
}
.score-header { font-size: 0.75rem; color: #94a3b8; font-weight: 500; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.8px; }
.score-main { display: flex; align-items: flex-end; gap: 14px; }
.score-big { font-size: 3.2rem; font-weight: 800; line-height: 1; letter-spacing: -2px; }
.score-side { padding-bottom: 6px; }
.score-badge-green {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(74,222,128,0.1);
    border: 1px solid rgba(74,222,128,0.25);
    color: #4ade80;
    padding: 4px 11px;
    border-radius: 999px;
    font-size: 0.73rem; font-weight: 600;
    margin-bottom: 4px;
}
.score-desc { font-size: 0.75rem; color: #94a3b8; }
.skill-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 16px; }
.skill-tag {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 999px;
    padding: 4px 11px;
    font-size: 0.72rem;
    color: #94a3b8;
    font-weight: 500;
}
.skill-tag.match {
    background: rgba(74,222,128,0.07);
    border-color: rgba(74,222,128,0.2);
    color: #86efac;
}

/* ── COVER LETTER CARD ── */
.letter-wrap {
    background: linear-gradient(145deg, #111527, #0f1220);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 26px;
    position: relative;
    overflow: hidden;
}
.letter-wrap::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), transparent);
}
.letter-topbar {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.letter-title { font-size: 0.88rem; font-weight: 600; color: #e2e8f0; }
.letter-actions { display: flex; gap: 8px; }
.lbtn {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    color: #64748b;
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex; align-items: center; gap: 5px;
    transition: all 0.15s;
}
.lbtn:hover { background: rgba(255,255,255,0.08); color: #94a3b8; }
.letter-body {
    font-size: 0.84rem;
    line-height: 1.85;
    color: #94a3b8;
    white-space: pre-wrap;
}
.letter-body p { margin-bottom: 14px; }
.letter-body strong { color: #cbd5e1; font-weight: 500; }

/* ── EMPTY STATE ── */
.empty-state {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: 460px;
    border: 1.5px dashed rgba(255,255,255,0.05);
    border-radius: 16px;
    gap: 14px;
    background: rgba(255,255,255,0.01);
}
.empty-icon { font-size: 3.5rem; opacity: 0.3; }
.empty-title { font-size: 1rem; font-weight: 600; color: #94a3b8; }
.empty-sub { font-size: 0.8rem; color: #64748b; text-align: center; max-width: 280px; line-height: 1.6; }

/* ── STREAMLIT WIDGET OVERRIDES ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
}
[data-testid="stFileUploader"] section {
    background: rgba(139,92,246,0.04) !important;
    border: 1.5px dashed rgba(139,92,246,0.3) !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] p { color: #94a3b8 !important; font-size: 0.8rem !important; }
[data-testid="stFileUploader"] button {
    background: rgba(139,92,246,0.15) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    color: #a78bfa !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 0.82rem !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.7 !important;
    padding: 14px !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: rgba(139,92,246,0.4) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1) !important;
}
.stTextArea label { display: none !important; }

[data-testid="stSelectbox"] { margin-top: 10px !important; }
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #64748b !important;
    font-size: 0.8rem !important;
}
[data-testid="stSelectbox"] > label { display: none !important; }

/* download button match style */
[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    width: 100% !important;
    box-shadow: none !important;
}

.disclaimer {
    font-size: 0.71rem;
    color: #1e293b;
    text-align: center;
    margin-top: 18px;
    line-height: 1.6;
}

/* divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
    margin: 6px 0 16px;
}
</style>
""", unsafe_allow_html=True)

# ── Session defaults ──────────────────────────────────────────────────────────
for k, v in [("generated", False), ("cover_letter", ""), ("score", 0), ("skills", [])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── NAV ───────────────────────────────────────────────────────────────────────
logo_b64 = get_base64_image("logo.png")
if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 48px; border-radius: 8px; margin-right: 12px; object-fit: contain;">'
else:
    logo_html = '<div class="nav-logo-icon"></div>'

st.markdown(f"""
<div class="navbar">
  <div class="nav-logo">
    {logo_html}
    <div>
      Resume to Cover Letter
      <div class="nav-logo-sub">AI-powered personalisation</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([38, 62], gap="small")

# ════════════════════════════════════════════════════════════════════════════
# LEFT PANEL
# ════════════════════════════════════════════════════════════════════════════
with left:
    st.markdown("""
    <div style="padding: 24px 4px 0 4px;">
      <div style="font-size:1.05rem;font-weight:700;color:#f1f5f9;letter-spacing:-0.3px;margin-bottom:4px;">
        Build your cover letter
      </div>
      <div style="font-size:0.78rem;color:#334155;margin-bottom:22px;">
        Upload your resume &amp; job description to get a personalised cover letter.
      </div>
    """, unsafe_allow_html=True)

    # ── SECTION 1 ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size: 0.95rem; font-weight: 600; color: #e2e8f0; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
      Upload Your Resume
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "resume",
        type=["pdf", "docx", "doc"],
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── SECTION 2 ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size: 0.95rem; font-weight: 600; color: #e2e8f0; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
      Paste Job Description
    </div>
    """, unsafe_allow_html=True)

    sample_jds = {
        "Software Engineer": "We are looking for a Software Engineer with 3+ years experience in Python, REST APIs, and cloud platforms (AWS/GCP). You will build scalable backend systems, participate in code reviews, and collaborate closely with product and design teams.",
        "Data Scientist": "Seeking a Data Scientist with expertise in machine learning, statistical modelling, SQL, and Python. Experience with NLP, LLMs, and data visualisation tools is a plus. You will own end-to-end model development.",
        "AI/ML Engineer": "Join our AI team to build LLM-powered products at scale. Expertise in PyTorch, transformers, and prompt engineering expected. You will design and ship production ML systems with measurable impact.",
        "Product Manager": "Drive product vision and roadmap. 4+ years in product management, strong analytical skills, and experience working with cross-functional teams. Data-driven mindset with strong stakeholder communication.",
        "UX Designer": "UI/UX Designer with a strong Figma portfolio, expertise in design systems and user research. Mobile-first mindset required. You will own the end-to-end design process from discovery to delivery.",
    }

    role_options = list(sample_jds.keys())
    selected_role = st.selectbox(
        "sample",
        ["— or pick a sample role —"] + role_options,
        label_visibility="collapsed",
    )

    prefill = sample_jds.get(selected_role, "")
    job_desc = st.text_area(
        "jd",
        value=prefill,
        placeholder="Paste the job description here…",
        height=160,
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    generate = st.button("Generate Cover Letter", use_container_width=True, type="primary")

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL
# ════════════════════════════════════════════════════════════════════════════
with right:
    st.markdown("<div style='padding: 24px 8px 0 8px;'>", unsafe_allow_html=True)

    if generate:
        if not job_desc.strip():
            st.warning("Please paste a job description to continue.")
        else:
            with st.spinner("Analysing resume and crafting your letter… (This may take a minute)"):
                
                temp_pdf_path = "temp_resume.pdf"
                if uploaded_file:
                    with open(temp_pdf_path, "wb") as f:
                        f.write(uploaded_file.read())
                    raw_resume = extract_text_from_pdf(temp_pdf_path)
                else:
                    raw_resume = ""
                
                cleaned_resume = clean_text(raw_resume)
                cleaned_jd = clean_text(job_desc)
                
                if cleaned_resume and cleaned_jd:
                    score = calculate_match_score(cleaned_resume, cleaned_jd)
                    missing_skills = get_missing_skills(cleaned_resume, cleaned_jd)
                    
                    st.session_state.score = score
                    # Limit to top 15 missing skills for UI
                    st.session_state.skills = missing_skills[:15] if missing_skills else ["None!"]
                    
                    prompt = create_prompt(cleaned_resume, cleaned_jd, missing_skills)
                    st.session_state.cover_letter = generate_cover_letter(prompt)
                    
                    st.session_state.generated = True
                else:
                    st.error("Could not extract text from the provided resume or job description.")
                    st.session_state.generated = False

                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)

    if st.session_state.generated:
        score = st.session_state.score
        
        if score >= 70:
            score_color = "#4ade80"
            badge_bg = "rgba(74,222,128,0.1)"
            badge_text = "✓ Great Match!"
        elif score >= 40:
            score_color = "#facc15"
            badge_bg = "rgba(250,204,21,0.1)"
            badge_text = "⚠ Fair Match"
        else:
            score_color = "#f87171"
            badge_bg = "rgba(248,113,113,0.1)"
            badge_text = "✗ Poor Match"

        badge_html = f'<div style="display:inline-flex;align-items:center;gap:5px;background:{badge_bg};border:1px solid {score_color}40;color:{score_color};padding:4px 11px;border-radius:999px;font-size:0.73rem;font-weight:600;margin-bottom:4px;">{badge_text}</div>'

        # ── SCORE + SKILLS ROW ──────────────────────────────────────────────
        s1, s2 = st.columns([4, 6])
        with s1:
            st.markdown(f"""
            <div class="score-wrap">
              <div class="score-header">Match Score</div>
              <div class="score-main">
                <div class="score-big" style="color:{score_color}">{score}%</div>
                <div class="score-side">
                  {badge_html}
                  <div class="score-desc">vs job description</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with s2:
            tags_html = "".join(
                f'<span class="skill-tag">{s}</span>'
                for s in st.session_state.skills
            )
            st.markdown(f"""
            <div class="score-wrap" style="height:100%">
              <div class="score-header">Missing Skills to Address</div>
              <div class="skill-tags">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        # ── ACTION ROW ─────────────────────────────────────────────────────
        ac1, ac2, ac3 = st.columns([2, 2, 8])
        with ac1:
            if st.button("Copy", use_container_width=True, type="primary"):
                st.toast("Copied!", icon="✅")
        with ac2:
            st.download_button(
                "Download",
                data=st.session_state.cover_letter,
                file_name="cover_letter.txt",
                mime="text/plain",
                use_container_width=True,
            )

        # ── COVER LETTER ────────────────────────────────────────────────────
        letter_html = st.session_state.cover_letter.replace("\n\n", "</p><p>").replace("\n", "<br>")
        st.markdown(f"""
        <div class="letter-wrap">
          <div class="letter-topbar">
            <div class="letter-title">Generated Cover Letter</div>
          </div>
          <div class="letter-body"><p>{letter_html}</p></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer">
          ⚠ AI-generated content. Always review and personalise before sending.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon"></div>
          <div class="empty-title">Your cover letter will appear here</div>
          <div class="empty-sub">Upload your resume and paste a job description on the left, then hit Generate.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
