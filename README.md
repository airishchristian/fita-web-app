# Fita 🏋️
A multi-page Streamlit fitness tracker app powered by Claude AI Vision.

## Features
- 🔐 Secure user registration and login with bcrypt
- 📸 Upload a food photo → AI identifies it and estimates macros
- 📊 Track daily calories and macros against personal goals
- 📈 View food history with charts (7 or 30 days)
- 🎯 Set daily calorie and macro targets

## Tech Stack
- [Streamlit](https://streamlit.io) — UI framework
- [Anthropic Claude](https://anthropic.com) — AI food identification
- [bcrypt](https://pypi.org/project/bcrypt/) — Password hashing
- [SQLite](https://www.sqlite.org) — Local database
- [Matplotlib](https://matplotlib.org) & [Seaborn](https://seaborn.pydata.org) — Charts
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variables

## Project Structure
```
fita/
├── app.py                  # Entry point, sidebar nav, session routing
├── config.py               # Loads ANTHROPIC_API_KEY from .env
├── auth/
│   ├── auth.py             # require_auth() session guard
│   ├── login.py            # Login form
│   └── register.py         # Registration form
├── food/
│   ├── food_tracker.py     # Page orchestrator
│   ├── image_upload.py     # Image uploader
│   ├── vision_api.py       # Claude Vision API integration
│   └── nutrition.py        # Display and save macros
├── dashboard/
│   ├── dashboard.py        # Today's summary
│   ├── goals.py            # Set daily targets
│   └── history.py          # Charts and history
└── db/
    └── db.py               # SQLite CRUD
```

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/fita.git
cd fita
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```
ANTHROPIC_API_KEY=your_api_key_here
```
Get your API key from [console.anthropic.com](https://console.anthropic.com)

### 5. Initialize the database
```bash
python db/db.py
```

### 6. Run the app
```bash
streamlit run app.py
```

## Environment Variables
| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

## Notes
- Never commit your `.env` file or `fita.db` to git
- The `.gitignore` already excludes both
