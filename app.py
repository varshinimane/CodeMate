import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="CodeMate - AI Code Companion", layout="wide")

# Function to clean markdown from Gemini outputs
def clean_code_output(output):
    output = output.strip()
    if output.startswith("```"):
        output = output.split("\n", 1)[1]
    if output.endswith("```"):
        output = output.rsplit("\n", 1)[0]
    return output.strip()

# Function to query Gemini
def query_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚫 Error: {e}"

# Sidebar Navigation
with st.sidebar:
    st.markdown(
        "<h2 style='text-align: center; color: #4B8BBE;'>💻 CodeMate</h2>"
        "<h4 style='text-align: center; color: gray;'>Main Menu</h4><hr>",
        unsafe_allow_html=True
    )

    selected = option_menu(
        menu_title=None,
        options=["Translator + Explain + Debug", "Refactor", "Comment", "Pseudocode Generator", "AI Assistant"],
        icons=["arrow-left-right", "recycle", "chat-dots", "text-paragraph", "robot"],
        default_index=0
    )

# Translator + Explain + Debug
if selected == "Translator + Explain + Debug":
    st.title("🔁 Translator | 📖 Explain | 🐞 Debug")

    col1, col2 = st.columns(2)
    with col1:
        input_lang = st.selectbox("Select Input Language", ["Python", "Java", "C++", "JavaScript", "C", "Go", "PHP"])
    with col2:
        output_lang = st.selectbox("Select Output Language", ["Python", "Java", "C++", "JavaScript", "C", "Go", "PHP"])

    st.markdown("#### 📝 Paste your code or upload a file")

    uploaded_file = st.file_uploader("📁 Upload a code file", type=["py", "java", "cpp", "js", "c", "go", "php"])
    code = ""

    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8")
        st.code(code, language=input_lang.lower())
    else:
        code = st.text_area("Paste your code here:", height=300)

    col1, col2, col3 = st.columns(3)

    if col1.button("🔁 Translate"):
        prompt = f"""
Translate the following code from {input_lang} to {output_lang}.
✅ Output only the translated code.
❌ Do NOT include any explanations.

{code}
"""
        output = clean_code_output(query_gemini(prompt))
        st.subheader("Translated Code")
        st.code(output, language=output_lang.lower())
        st.download_button("⬇️ Download", output, file_name=f"translated_code.{output_lang.lower()}")

    if col2.button("📖 Explain"):
        prompt = f"Explain this {input_lang} code step-by-step:\n\n{code}"
        output = query_gemini(prompt)
        st.subheader("Explanation")
        st.write(output)
        st.download_button("⬇️ Download Explanation", output, file_name="explanation.txt")

    if col3.button("🐞 Debug"):
        prompt = f"Find errors, bugs, and suggest fixes for this {input_lang} code:\n\n{code}"
        output = query_gemini(prompt)
        st.subheader("Debugging Suggestions")
        st.write(output)
        st.download_button("⬇️ Download Debug Report", output, file_name="debug.txt")

# Refactor
elif selected == "Refactor":
    st.title("♻️ Code Refactor")
    input_lang = st.selectbox("Language", ["Python", "Java", "C++", "JavaScript", "C", "Go", "PHP"])
    code = st.text_area("Paste your code:", height=300)

    if st.button("♻️ Refactor Code"):
        prompt = f"Refactor this {input_lang} code to improve readability and efficiency:\n\n{code}"
        output = clean_code_output(query_gemini(prompt))
        st.subheader("Refactored Code")
        st.code(output, language=input_lang.lower())
        st.download_button("⬇️ Download Refactored Code", output, file_name=f"refactored.{input_lang.lower()}")

# Comment
elif selected == "Comment":
    st.title("💬 Add Code Comments")
    input_lang = st.selectbox("Language", ["Python", "Java", "C++", "JavaScript", "C", "Go", "PHP"])
    code = st.text_area("Paste your code:", height=300)

    if st.button("💬 Comment Code"):
        prompt = f"Add meaningful comments to this {input_lang} code:\n\n{code}"
        output = clean_code_output(query_gemini(prompt))
        st.subheader("Commented Code")
        st.code(output, language=input_lang.lower())
        st.download_button("⬇️ Download Commented Code", output, file_name=f"commented.{input_lang.lower()}")

# Pseudocode Generator
elif selected == "Pseudocode Generator":
    st.title("🔤 Pseudocode Generator")
    input_lang = st.selectbox("Language", ["Python", "Java", "C++", "JavaScript", "C", "Go", "PHP"])
    code = st.text_area("Paste your code:", height=300)

    if st.button("Generate Pseudocode"):
        prompt = f"Convert the following {input_lang} code into simple step-by-step pseudocode (no syntax):\n\n{code}"
        output = query_gemini(prompt)
        st.subheader("Pseudocode")
        st.write(output)
        st.download_button("⬇️ Download Pseudocode", output, file_name="pseudocode.txt")

# AI Assistant
elif selected == "AI Assistant":
    st.title("🤖 Ask AI Anything")
    query = st.text_area("💬 Enter your coding question:", height=200)

    if st.button("🚀 Get Answer"):
        response = query_gemini(query)
        st.subheader("Response")
        st.write(response)

# Footer
st.markdown("---")
