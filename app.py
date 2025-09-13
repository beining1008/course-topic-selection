import streamlit as st
import json
import os
import time
import random
from datetime import datetime

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
    """保存数据并创建备份"""
    # 保存主数据文件
    with open("topics_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 创建带时间戳的备份文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_topics_{timestamp}.json"
    with open(backup_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 记录选择日志
    log_selection_activity(data)

def log_selection_activity(data):
    """记录选择活动日志"""
    try:
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "selections": []
        }

        for category, topics in data.items():
            for topic in topics:
                if topic["student"]:
                    log_entry["selections"].append({
                        "topic_id": topic["id"],
                        "topic_title": topic["title"],
                        "student": topic["student"],
                        "category": category
                    })

        # 追加到日志文件
        log_filename = "selection_log.txt"
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(f"\n=== LOG ENTRY {log_entry['timestamp']} ===\n")
            if log_entry["selections"]:
                for selection in log_entry["selections"]:
                    f.write(f"Topic {selection['topic_id']}: {selection['topic_title']} -> {selection['student']}\n")
            else:
                f.write("No selections yet.\n")
            f.write("=" * 50 + "\n")
    except Exception as e:
        # 静默处理日志错误，不影响主功能
        pass

def check_student_has_selected(data, student_name):
    """Check if student has already selected a topic"""
    for category in data.values():
        for topic in category:
            if topic["student"] == student_name:
                return True, topic["title"]
    return False, None

def select_topic(topic_id, student_name):
    """Select a topic with race condition protection"""
    import time
    import random

    # Add small random delay to reduce simultaneous access
    time.sleep(random.uniform(0.05, 0.15))

    # Reload data to get the most current state (critical for race condition protection)
    data = load_data()

    # Check if student has already selected a topic
    has_selected, selected_topic = check_student_has_selected(data, student_name)
    if has_selected:
        st.error(f"You have already selected a topic: {selected_topic}")
        return False

    # Find and update topic with atomic check
    for category in data.values():
        for topic in category:
            if topic["id"] == topic_id:
                # Critical section: double-check availability before assignment
                if topic["student"] == "":
                    topic["student"] = student_name
                    save_data(data)
                    st.success(f"✅ Successfully selected topic: {topic['title']}")
                    return True
                else:
                    # More user-friendly error message for race condition
                    st.error(f"❌ Sorry, this topic was just selected by another student. Please refresh and choose a different topic.")
                    return False

    st.error("❌ Topic not found")
    return False

def generate_text_report():
    """Generate simple text report"""
    data = load_data()

    # Create text report
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("COURSE TOPIC SELECTION REPORT")
    report_lines.append("=" * 60)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # Count statistics
    total_topics = 0
    selected_topics = 0

    for category, topics in data.items():
        report_lines.append(f"CATEGORY: {category}")
        report_lines.append("-" * 40)

        for topic in topics:
            total_topics += 1
            student_info = topic["student"] if topic["student"] else "Available"
            if topic["student"]:
                selected_topics += 1
                status = "SELECTED"
            else:
                status = "AVAILABLE"

            report_lines.append(f"{topic['id']:2d}. {topic['title']}")
            report_lines.append(f"    Student: {student_info}")
            report_lines.append(f"    Status: {status}")
            report_lines.append("")

        report_lines.append("")

    # Add summary
    report_lines.append("=" * 60)
    report_lines.append("SUMMARY")
    report_lines.append("=" * 60)
    report_lines.append(f"Total Topics: {total_topics}")
    report_lines.append(f"Selected Topics: {selected_topics}")
    report_lines.append(f"Available Topics: {total_topics - selected_topics}")
    report_lines.append(f"Selection Rate: {(selected_topics/total_topics*100):.1f}%")

    return "\n".join(report_lines)



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

        # Show student's current selection if any (privacy-friendly)
        data = load_data()
        student_selection = None
        for category, topics in data.items():
            for topic in topics:
                if topic["student"] == student_name.strip():
                    student_selection = (category, topic)
                    break
            if student_selection:
                break

        if student_selection:
            st.success(f"📋 Your current selection: **{student_selection[1]['title']}** (Topic {student_selection[1]['id']})")
        else:
            st.info("📋 You haven't selected any topic yet.")

    st.markdown("---")

    # Add refresh button and tip for race condition handling
    col_refresh, col_tip = st.columns([1, 3])
    with col_refresh:
        if st.button("🔄 Refresh", help="Click to see the latest topic availability"):
            st.rerun()
    with col_tip:
        st.markdown("*💡 Tip: If you see an error, the topic was just selected by someone else. Try refreshing!*")

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
                        # Selected topic - hide student name for privacy
                        st.markdown(f"**{topic['id']}. {topic['title']}**")
                        st.markdown("🔒 *This topic has been selected*")

                with col2:
                    if topic["student"] == "":
                        if st.button("Select", key=f"select_{topic['id']}"):
                            if not student_name.strip():
                                st.error("Please enter your name first!")
                            else:
                                # Show loading message during selection
                                with st.spinner("Selecting topic..."):
                                    success = select_topic(topic["id"], student_name.strip())
                                    if success:
                                        st.rerun()
                                    else:
                                        # Auto-refresh on conflict to show updated status
                                        time.sleep(0.5)
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
            if st.button("📄 Generate Text Report"):
                try:
                    text_data = generate_text_report()
                    st.download_button(
                        label="Download Text Report",
                        data=text_data,
                        file_name=f"topic_selection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    st.success("✅ Text report generated successfully!")
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")

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

        # 新增：数据恢复和备份管理
        st.markdown("---")
        st.markdown("### 📦 Data Backup & Recovery")

        col3, col4 = st.columns(2)

        with col3:
            if st.button("💾 Download Current Backup"):
                try:
                    # 创建当前数据的备份
                    backup_data = {
                        "backup_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "data": data
                    }
                    backup_json = json.dumps(backup_data, ensure_ascii=False, indent=2)
                    st.download_button(
                        label="Download Backup File",
                        data=backup_json,
                        file_name=f"course_selection_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                    st.success("✅ Backup file ready for download!")
                except Exception as e:
                    st.error(f"Error creating backup: {str(e)}")

        with col4:
            uploaded_file = st.file_uploader("📤 Restore from Backup", type=['json'])
            if uploaded_file is not None:
                try:
                    backup_content = json.loads(uploaded_file.read().decode('utf-8'))
                    if 'data' in backup_content:
                        restored_data = backup_content['data']
                        save_data(restored_data)
                        st.success("✅ Data restored successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid backup file format")
                except Exception as e:
                    st.error(f"❌ Error restoring backup: {str(e)}")

        # 显示备份提示
        st.info("💡 **Important**: Download backups regularly to prevent data loss during system restarts!")

    elif admin_password:
        st.error("❌ Incorrect password")
    else:
        st.info("👆 Teachers: Enter password to access admin functions")

if __name__ == "__main__":
    main()
