# PDF Report Generation System

An AI-powered educational assessment platform that generates personalized PDF reports based on a comprehensive 7-factor psychological analysis model. The system processes user assessment data, leverages artificial intelligence for content generation, creates data visualizations, and produces professional PDF reports through an HTML-to-PDF conversion pipeline.

## Features

- **7-Factor Assessment Model**: Evaluates users across Career Interest, Aptitude, Personality, Learning Style, Basic Values, Work Style, and Emotional Intelligence
- **AI-Powered Content Generation**: Uses OpenAI GPT-4-turbo for personalized report content
- **Dynamic Chart Generation**: Creates radar charts, bar charts, polar area charts, and stream comparison visualizations
- **Template-Based Rendering**: Uses Jinja2 templates with modular CSS for consistent report layouts 
- **PDF Assembly**: Merges individual pages into cohesive reports using PyPDF 

## Installation

```bash
pip install pypdf matplotlib jinja2 weasyprint numpy openai python-dotenv requests werkzeug pymupdf
```

## Configuration

Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Basic Usage

```python
from generate_pdf import make_all_pdf, start_makeing_all_charts
import json

# Load user data
with open("data/new_data_diagnostic.json") as f:
    all_data = json.load(f)["data"]

user_detail = {
    "user_id": 11111,
    "name": "Student Name",
    "Class": "10",
    "year": "June 2025"
}

# Generate charts and PDF reports
start_makeing_all_charts(user_id, all_data)
make_all_pdf(user_id, user_detail, all_data)
```

### Running the Main Script

```bash
python generate_pdf.py
```

## Project Structure

```
├── generate_pdf.py          # Main orchestration script
├── gpt_helper.py            # AI content generation
├── renderer.py              # Template rendering and PDF generation
├── data/
│   ├── new_data_diagnostic.json  # Assessment data
│   └── factor/              # Factor metadata
├── factors/                 # Factor-specific components
│   ├── Career_interest.py
│   ├── Aptitude.py
│   └── ...
├── charts/                  # Chart generation modules
│   ├── radar_chart.py
│   ├── bar_chart.py
│   └── ...
├── templates/pages/         # Jinja2 templates
└── static/
    ├── styles/              # CSS files
    └── charts/              # Generated charts
```

## Core Components

### Factor Analysis
Each of the 7 factors has a dedicated component that processes assessment data and generates factor-specific content :

- **Career Interest**: Uses radar charts for visualization
- **Aptitude**: Uses polar area charts  
- **Personality**: Uses dual bar charts
- **Learning Style**: Uses dual bar charts
- **Basic Values**: Uses dual bar charts
- **Work Style**: Uses radar charts
- **Emotional Intelligence**: Uses radar charts

### Chart Generation
The system generates various chart types based on factor requirements :

```python
# Example: Radar chart generation
generate_radar_chart(user_id, factor, traits)
```

### AI Content Generation
Leverages multiple AI services for personalized content :

- Report summaries
- Stream recommendations  
- Interest alignments
- Subject analysis

## Data Format

Assessment data follows a structured format with user scores, global averages, and metadata :

```json
{
  "factors": {
    "Career Interest": {
      "subfactor_name": {
        "user_score": 85,
        "global_avg": 70,
        "global_max": 95,
        "global_min": 45
      }
    }
  }
}
```

## Output

The system generates:
- Individual factor reports (PDF)
- Composite analysis report (PDF)  
- Merged final report combining all components
- Dynamic charts and visualizations

Reports are saved to `reports/users/{user_id}/merged/` directory.

## Dependencies

- **pypdf**: PDF manipulation and merging
- **matplotlib**: Chart generation
- **jinja2**: Template rendering
- **weasyprint**: HTML to PDF conversion
- **openai**: AI content generation
- **numpy**: Numerical computations

## Notes

This system is designed for educational assessment and career guidance, providing personalized insights through a combination of psychometric analysis and AI-powered content generation. The modular architecture allows for easy extension of factors, chart types, and AI content generation capabilities. The template-based rendering system ensures consistent professional formatting across all generated reports.
