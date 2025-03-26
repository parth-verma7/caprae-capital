# Lead Generation Tool

This tool extracts company data (Name, Description, Number of Employees) from websites and updates a Google Sheet using Gemini 2.0 Flash and a Playwright-based `browser_use` agent.

## Installation

### Prerequisites
- Python 3.11+
- Google Sheets API enabled `.json` file for access
- Gemini API Key

### Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/parth-verma7/caprae-capital.git
   cd caprae-capital
   ```

2. **Create Virtual Environment**
   ```bash
   uv venv --python 3.11
   # For Mac/Linux:
   source .venv/bin/activate

   # For Windows:
   .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   uv pip install -r requirements.txt
   uv run playwright install
   ```

4. **Set Up API Keys**
   - Place your Google Sheets API credentials `.json` file in the project directory.
   - Set the Gemini API Key as an environment variable:
     ```bash
     export GEMINI_API_KEY="your-api-key"
     export GSHEETS="your-google-sheet-key"
     ```


## Usage

1. **Run the Lead Generation Script**
   ```bash
   python main.py
   ```

2. **Monitor Google Sheets**
   - Extracted company data will be automatically updated in the linked Google Sheet.
