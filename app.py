import streamlit as st
import json
import os
from fpdf import FPDF
import io

# 页面配置
st.set_page_config(page_title="Course Topic Selection System", page_icon="📚", layout="wide")

# Force SSL refresh - version 1.1

# 初始化数据文件
def initialize_data():
    """Initialize topics_data.json file"""
    if not os.path.exists("topics_data.json"):
        initial_topics = {
            "Mobile Computing & Edge Intelligence": [
                {"id": 1, "title": "Mobile Edge Computing (MEC) and its Applications in Smart Cities", "student": ""},
                {"id": 2, "title": "AI at the Edge: On-Device Learning and Inference", "student": ""},
                {"id": 3, "title": "Wireless Federated Learning: Opportunities and Challenges", "student": ""},
                {"id": 4, "title": "Federated Unlearning for Privacy in Mobile Systems", "student": ""},
                {"id": 5, "title": "Energy Efficiency in Mobile and IoT Devices", "student": ""},
                {"id": 6, "title": "Mobile App Security: Threats and Countermeasures", "student": ""},
                {"id": 7, "title": "Role of 5G/6G in Enabling Autonomous Vehicles", "student": ""},
                {"id": 8, "title": "UAV-Assisted Mobile Edge Computing", "student": ""},
                {"id": 9, "title": "Mobile Digital Twins for Healthcare and Industry", "student": ""}
            ],
            "Cloud Computing Foundations": [
                {"id": 11, "title": "Virtualization vs. Containerization in the Cloud", "student": ""},
                {"id": 12, "title": "Cloud Storage Systems: Design and Reliability", "student": ""},
                {"id": 13, "title": "Serverless Computing: Benefits and Limitations", "student": ""},
                {"id": 14, "title": "Cloud-native Application Development and Deployment", "student": ""},
                {"id": 15, "title": "Multi-cloud and Hybrid Cloud Architectures", "student": ""},
                {"id": 16, "title": "Cloud Networking: SDN and NFV", "student": ""},
                {"id": 17, "title": "Cloud Databases: SQL vs. NoSQL Approaches", "student": ""},
                {"id": 18, "title": "Scalability and Elasticity in Cloud Platforms", "student": ""},
                {"id": 19, "title": "Cloud Cost Optimization Strategies", "student": ""}
            ],
            "Security, Privacy & Trust": [
                {"id": 21, "title": "Zero Trust Architecture in Mobile and Cloud Environments", "student": ""},
                {"id": 22, "title": "Blockchain for Secure Cloud and Mobile Computing", "student": ""},
                {"id": 23, "title": "Privacy-Preserving Machine Learning in the Cloud", "student": ""},
                {"id": 24, "title": "Data Compliance in Cloud Services (e.g., GDPR, HIPAA)", "student": ""},
                {"id": 25, "title": "Mobile Malware and Cloud-based Detection Techniques", "student": ""},
                {"id": 26, "title": "Quantum Computing Threats to Cloud Security", "student": ""},
                {"id": 27, "title": "Identity and Access Management (IAM) in Cloud Systems", "student": ""},
                {"id": 28, "title": "Secure Multi-Party Computation in Mobile and Cloud Settings", "student": ""},
                {"id": 29, "title": "Green and Sustainable Cloud Computing", "student": ""}
            ]
        }
        
        with open("topics_data.json", "w", encoding="utf-8") as f:
            json.dump(initial_topics, f, ensure_ascii=False, indent=2)

def load_data():
    """加载数据"""
    with open("topics_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """保存数据"""
    with open("topics_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_student_has_selected(data, student_name):
    """Check if student has already selected a topic"""
    for category in data.values():
        for topic in category:
            if topic["student"] == student_name:
                return True, topic["title"]
    return False, None

def select_topic(topic_id, student_name):
    """Select a topic"""
    data = load_data()

    # Check if student has already selected a topic
    has_selected, selected_topic = check_student_has_selected(data, student_name)
    if has_selected:
        st.error(f"You have already selected a topic: {selected_topic}")
        return False

    # Find and update topic
    for category in data.values():
        for topic in category:
            if topic["id"] == topic_id:
                if topic["student"] == "":
                    topic["student"] = student_name
                    save_data(data)
                    st.success(f"Successfully selected topic: {topic['title']}")
                    return True
                else:
                    st.error(f"This topic has been selected by {topic['student']}")
                    return False
    return False

def generate_pdf():
    """Generate PDF report"""
    data = load_data()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()

    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Course Topic Selection Report', 0, 1, 'C')
    pdf.ln(10)

    pdf.set_font('Arial', '', 12)

    for category, topics in data.items():
        # Category title
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'Category: {category}', 0, 1)
        pdf.set_font('Arial', '', 10)

        for topic in topics:
            student_info = topic["student"] if topic["student"] else "Available"
            # Handle long topic titles by splitting them
            topic_text = f'  {topic["id"]}. {topic["title"]}: {student_info}'
            if len(topic_text) > 80:
                # Split long lines
                lines = [topic_text[i:i+80] for i in range(0, len(topic_text), 80)]
                for i, line in enumerate(lines):
                    if i == 0:
                        pdf.cell(0, 6, line, 0, 1)
                    else:
                        pdf.cell(0, 6, '    ' + line, 0, 1)
            else:
                pdf.cell(0, 6, topic_text, 0, 1)

        pdf.ln(5)

    return pdf.output(dest='S').encode('latin-1')

# 主应用
def main():
    # 初始化数据
    initialize_data()
    
    # Page title
    st.title("📚 Course Topic Selection System")
    st.markdown("### Welcome! Please select your presentation topic.")
    st.markdown("---")

    # Student name input
    student_name = st.text_input("Please enter your name:", placeholder="e.g., John Smith")

    if student_name:
        st.markdown(f"**Current user:** {student_name}")

    st.markdown("---")
    
    # Load data
    data = load_data()

    # Display topics
    for category, topics in data.items():
        st.subheader(f"🔹 {category}")

        for topic in topics:
            # Create a container for each topic
            with st.container():
                col1, col2 = st.columns([4, 1])

                with col1:
                    if topic["student"] == "":
                        # Available topic
                        st.markdown(f"**{topic['id']}. {topic['title']}**")
                        st.markdown("✅ *Available*")
                    else:
                        # Selected topic
                        st.markdown(f"**{topic['id']}. {topic['title']}**")
                        st.markdown(f"🔒 *Selected by {topic['student']}*")

                with col2:
                    if topic["student"] == "":
                        if st.button("Select", key=f"select_{topic['id']}"):
                            if not student_name.strip():
                                st.error("Please enter your name first!")
                            else:
                                if select_topic(topic["id"], student_name.strip()):
                                    st.rerun()

                st.markdown("---")

        st.markdown("")
    
    # Admin functions with password protection
    st.markdown("---")
    st.subheader("🔐 Teacher/Admin Functions")

    # Password protection
    admin_password = st.text_input("Enter admin password:", type="password", key="admin_pass")

    if admin_password == "teacher2024":  # You can change this password
        st.success("✅ Admin access granted")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📄 Generate PDF Report"):
                try:
                    pdf_data = generate_pdf()
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_data,
                        file_name="topic_selection_report.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")

        with col2:
            if st.button("🔄 Reset All Selections"):
                if st.session_state.get('confirm_reset', False):
                    # Reset data
                    for category in data.values():
                        for topic in category:
                            topic["student"] = ""
                    save_data(data)
                    st.success("All selections have been reset!")
                    st.session_state.confirm_reset = False
                    st.rerun()
                else:
                    st.session_state.confirm_reset = True
                    st.warning("Click again to confirm reset of all selections")

    elif admin_password:
        st.error("❌ Incorrect password")
    else:
        st.info("👆 Teachers: Enter password to access admin functions")

if __name__ == "__main__":
    main()
