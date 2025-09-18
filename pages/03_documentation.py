import streamlit as st
import os
import re

# Set page configuration
st.set_page_config(
    page_title="ITMS Documentation",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to render Mermaid diagrams
def render_mermaid(diagram_code):
    # Clean up the diagram code
    diagram_code = diagram_code.strip()
    
    # Display the raw Mermaid code first
    st.code(diagram_code, language="mermaid")
    
    # Then render it using Mermaid.js
    st.markdown(f"""
    <div class="mermaid">
    {diagram_code}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{startOnLoad:true}});
    </script>
    """, unsafe_allow_html=True)

# Function to read and process the README file
def display_readme():
    readme_path = os.path.join(os.getcwd(), "COMPREHENSIVE_README.md")
    
    if not os.path.exists(readme_path):
        st.error("Comprehensive README file not found. Please create it first.")
        return
    
    with open(readme_path, 'r') as file:
        content = file.read()
    
    # Split the content by sections
    sections = re.split(r'## ', content)
    
    # Process the title section separately
    title_section = sections[0]
    st.markdown(title_section, unsafe_allow_html=True)
    
    # Process each section
    for section in sections[1:]:
        if section.strip():
            section_title = section.split('\n')[0]
            section_content = '\n'.join(section.split('\n')[1:])
            
            st.markdown(f"## {section_title}", unsafe_allow_html=True)
            
            # Check for Mermaid diagrams in this section
            mermaid_blocks = re.findall(r'```mermaid\s*(.*?)\s*```', section_content, re.DOTALL)
            
            # Replace Mermaid code blocks with placeholders
            for i, block in enumerate(mermaid_blocks):
                placeholder = f"MERMAID_PLACEHOLDER_{i}"
                section_content = section_content.replace(f"```mermaid\n{block}\n```", placeholder)
            
            # Split the content by placeholders
            parts = re.split(r'(MERMAID_PLACEHOLDER_\d+)', section_content)
            
            for part in parts:
                if part.startswith("MERMAID_PLACEHOLDER_"):
                    # Render Mermaid diagram
                    index = int(part.split('_')[-1])
                    st.subheader("Architecture Diagram")
                    st.info("Below is both the Mermaid code and the rendered diagram. You can copy the code for your own use.")
                    render_mermaid(mermaid_blocks[index])
                else:
                    # Render regular markdown
                    st.markdown(part, unsafe_allow_html=True)

# Main content
st.title("📚 Indian Railways ITMS Documentation")

st.markdown("""
This page provides comprehensive documentation for the Indian Railways Integrated Track Monitoring System (ITMS).
It includes detailed explanations of the system architecture, components, and functionality.

The diagrams below are shown both as code (which you can copy) and as rendered diagrams.
""")

# Display the README content
display_readme()

# Note about Mermaid diagrams
st.info("""
**Note about diagrams:** The diagrams on this page are rendered using Mermaid.js. If you don't see the rendered diagrams properly, 
you can still use the Mermaid code shown above each diagram. This code can be used in GitHub markdown files or other documentation tools 
that support Mermaid.
""")

# Footer
st.markdown("---")
st.markdown("Indian Railways Integrated Track Monitoring System (ITMS) - Documentation Page")