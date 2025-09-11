# Course Topic Selection System

A simple course topic selection website based on Streamlit.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
streamlit run app.py
```

### 3. Access the Website
The browser will open automatically, or manually visit: http://localhost:8501

## Features

- ✅ Students can select their preferred course topics
- ✅ Each topic can only be selected by one student
- ✅ Real-time display of topic selection status
- ✅ Teachers can generate PDF reports
- ✅ Teachers can reset all selections
- ✅ Data automatically saved in JSON file

## File Structure

- `app.py` - Main application
- `requirements.txt` - Python dependencies
- `topics_data.json` - Data storage file (auto-generated)

## Topic Categories

The system contains 3 categories with 27 topics total:
1. Mobile Computing & Edge Intelligence (9 topics)
2. Cloud Computing Foundations (9 topics)
3. Security, Privacy & Trust (9 topics)

## Usage Instructions

### For Students:
1. Enter your name
2. Browse available topics
3. Click "Select" button for your chosen topic
4. Each student can only select one topic

### For Teachers:
1. Click "Generate PDF Report" to download selection status
2. Click "Reset All Selections" to clear all selections (requires confirmation)

## Teacher Instructions

### Before Class:
1. Start the application: `streamlit run app.py`
2. Share the URL with students: **http://localhost:8501**
3. Students can access this URL to select their topics

### Network Access:
- **Local access**: http://localhost:8501
- **Network access**: http://[your-ip]:8501 (for students on the same network)

### During Class:
- Monitor selections in real-time
- Generate PDF report when needed
- Reset selections if necessary

## Notes

- Ensure Python environment is installed
- Data is automatically created on first run
- Data is saved in local JSON file
- Recommend backing up `topics_data.json` file regularly
