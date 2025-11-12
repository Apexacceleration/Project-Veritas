"""
Project Veritas - Streamlit Web Interface
Beautiful, user-friendly web app for family access
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.main import run_veritas
import config

# Page configuration
st.set_page_config(
    page_title="Project Veritas - Review Analysis",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .score-box {
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .score-a { background-color: #d4edda; border: 2px solid #28a745; }
    .score-b { background-color: #d1ecf1; border: 2px solid #17a2b8; }
    .score-c { background-color: #fff3cd; border: 2px solid #ffc107; }
    .score-d { background-color: #f8d7da; border: 2px solid #dc3545; }
    .score-f { background-color: #f8d7da; border: 2px solid #721c24; }
    .big-score {
        font-size: 4rem;
        font-weight: bold;
        margin: 0;
    }
    .score-label {
        font-size: 1.2rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)


def render_score_box(score: float, grade: str, label: str, summary: str):
    """Renders a styled score box."""
    grade_class = f"score-{grade.lower()}"

    st.markdown(f"""
    <div class="score-box {grade_class}">
        <div class="score-label">{label}</div>
        <div class="big-score">{score:.0f}</div>
        <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">Grade: {grade}</div>
        <div style="margin-top: 1rem; font-size: 1rem;">{summary}</div>
    </div>
    """, unsafe_allow_html=True)


def main():
    # Header
    st.markdown('<div class="main-header">🔍 Project Veritas</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Finding truth in online reviews</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        enable_ai = st.checkbox(
            "🤖 Enable AI Analysis",
            value=False,
            help="Uses OpenAI API for enhanced analysis (requires API key)"
        )

        if enable_ai:
            # Check if API key is already configured
            existing_api_key = os.getenv("OPENAI_API_KEY")

            if existing_api_key and existing_api_key != "sk-your-api-key-here":
                # API key is pre-configured - show success message
                st.success("✅ API Key configured")
                api_key = existing_api_key
            else:
                # No API key - show input field
                api_key = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    help="Get your API key from platform.openai.com"
                )
                if api_key:
                    os.environ["OPENAI_API_KEY"] = api_key

            # Model selection
            st.write("**AI Model:**")
            ai_model = st.radio(
                "Select Model",
                options=["GPT-5-mini", "GPT-5"],
                index=0,
                help="GPT-5-mini: Best balance (5x cheaper, 95% accuracy)\nGPT-5: Maximum accuracy (5x cost)",
                label_visibility="collapsed"
            )

            # Show cost comparison
            if ai_model == "GPT-5-mini":
                st.info("💰 **~$0.0015/analysis** | ⭐ Recommended")
                os.environ["VERITAS_AI_MODEL"] = "gpt-5-mini"
            else:
                st.warning("💰 **~$0.0075/analysis** | ⚡ Maximum accuracy")
                os.environ["VERITAS_AI_MODEL"] = "gpt-5"

            # Comparison expander
            with st.expander("📊 Model Comparison"):
                st.markdown("""
                | Feature | GPT-5-mini | GPT-5 |
                |---------|-----------|-------|
                | **Cost/analysis** | $0.0015 | $0.0075 |
                | **Accuracy** | 95% | 100% |
                | **Speed** | Fast | Fast |
                | **Best for** | Personal use | Professional |

                **GPT-5-mini** has 95% of GPT-5's capabilities at 1/5th the cost.
                Perfect for typical Amazon products!
                """)
        else:
            api_key = None

        st.divider()

        st.header("ℹ️ About")
        st.write("""
        **Project Veritas** analyzes Amazon product reviews to detect:
        - Fake reviews
        - Incentivized reviews
        - Review manipulation
        - Coordinated campaigns

        **Two Scores:**
        - **Trust Score**: Review reliability
        - **Quality Score**: Actual product quality
        """)

        st.divider()

        st.caption("Made with ❤️ for truth-seekers")

    # Main content
    st.write("### Enter Amazon Product URL")

    url = st.text_input(
        "Product URL",
        placeholder="https://amazon.com/dp/B08N5WRWNW",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        analyze_button = st.button("🔍 Analyze Reviews", type="primary", use_container_width=True)

    with col2:
        if st.button("📋 Example URL", use_container_width=True):
            st.info("Try: https://amazon.com/dp/B08N5WRWNW")

    # Analysis
    if analyze_button:
        if not url:
            st.error("⚠️ Please enter a valid Amazon product URL")
            return

        if not url.startswith("http"):
            st.error("⚠️ URL must start with http:// or https://")
            return

        # Progress indicator
        with st.spinner("🔍 Analyzing reviews... This may take 1-2 minutes."):
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # Update progress
                status_text.text("📥 Scraping reviews from Amazon...")
                progress_bar.progress(20)

                # Run analysis (capture verbose output)
                import io
                from contextlib import redirect_stdout

                # Redirect prints to capture progress
                output_buffer = io.StringIO()

                with redirect_stdout(output_buffer):
                    report = run_veritas(url, verbose=True)

                status_text.text("✅ Analysis complete!")
                progress_bar.progress(100)

                # Clear progress indicators
                status_text.empty()
                progress_bar.empty()

                # Check for errors
                if "error" in report:
                    st.error(f"❌ Error: {report['error']}")
                    return

                # Display results
                st.success("✅ Analysis Complete!")

                # Summary metrics
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Total Reviews", report["total_reviews_analyzed"])

                with col2:
                    st.metric("Trusted Reviews", report["trusted_reviews_count"])

                with col3:
                    st.metric("Suspicious Reviews", report["suspicious_reviews_count"])

                st.divider()

                # Score displays
                col1, col2 = st.columns(2)

                with col1:
                    render_score_box(
                        report["trust_score"],
                        report["trust_grade"],
                        "🔒 Trust Score",
                        report["trust_summary"]
                    )

                with col2:
                    render_score_box(
                        report["quality_score"],
                        report["quality_grade"],
                        "⭐ Quality Score",
                        report["quality_summary"]
                    )

                # Red flags
                if report.get("red_flags_triggered"):
                    st.divider()
                    st.write("### 🚩 Red Flags Detected")

                    for flag in report["red_flags_triggered"]:
                        st.warning(f"⚠️ {flag}")

                # AI insights (if available)
                if "ai_insights" in report and report["ai_insights"].get("overall_authenticity"):
                    st.divider()

                    # Show which model was used
                    model_used = os.getenv("VERITAS_AI_MODEL", "gpt-5-mini")
                    model_emoji = "⚡" if model_used == "gpt-5" else "🤖"
                    st.write(f"### {model_emoji} AI Insights ({model_used})")

                    ai = report["ai_insights"]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("AI Authenticity Score", f"{ai['overall_authenticity']:.0f}/100")

                    with col2:
                        risk_level = ai.get("manipulation_likelihood", "unknown").upper()
                        risk_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(risk_level, "⚪")
                        st.metric("Manipulation Risk", f"{risk_color} {risk_level}")

                    if ai.get("patterns_detected"):
                        st.write("**Patterns Detected:**")
                        for pattern in ai["patterns_detected"]:
                            st.write(f"- {pattern}")

                    if ai.get("reasoning"):
                        st.info(f"💡 {ai['reasoning']}")

                # Download report
                st.divider()

                col1, col2 = st.columns([1, 3])

                with col1:
                    # Generate filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"veritas_report_{timestamp}.json"

                    st.download_button(
                        label="📥 Download Report (JSON)",
                        data=json.dumps(report, indent=2),
                        file_name=filename,
                        mime="application/json",
                        use_container_width=True
                    )

                # Raw JSON (expandable)
                with st.expander("📄 View Raw JSON Report"):
                    st.json(report)

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.exception(e)


if __name__ == "__main__":
    main()
