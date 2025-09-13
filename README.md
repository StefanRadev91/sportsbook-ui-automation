# Sportsbook UI Automation (Playwright + Python)

Automated UI test framework for validating **Live Betting** functionality on [bwin.com](https://www.bwin.com/en/sports/live/betting).  
The project demonstrates how to handle **dynamic, real-time odds updates** using the **Page Object Model (POM)** design pattern.

## Key Features
- **Modular & Maintainable** – separation of pages, components, and tests  
- **Stable** – robust locators, explicit waits, no hard sleeps  
- **Responsive** – scenarios run on both desktop & mobile viewports  
- **Aligned with SDET assignment** – implements the requested coverage (odds updates, betslip, navigation)

## Setup & Run
```
# 1. Clone repository & create virtual environment
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install

# Run all tests (default = desktop)
pytest -v -s

# By markers
pytest -m smoke   -v -s   # Smoke tests
pytest -m live    -v -s   # Live odds update
pytest -m desktop -v -s   # Desktop only
pytest -m mobile  -v -s   # Mobile only

```

## What is Tested

### 1. Add Pick to Betslip
- Navigate to a live event  
- Add a selection to Betslip  
- Verify selection is highlighted in Event View  
- Verify selection appears inside Betslip (desktop tab or mobile Quick Bet modal)  

### 2. Live Odds Update (Dynamic)
- Open a live Tennis event  
- Capture current Match Winner odds  
- Wait for odds change (without refresh)  
- Validate:  
  - Odds text/value updates  
  - Direction indicator (up = increased, down = decreased)  
  - Direction matches numeric change  

### 3. Sport Sorting (A–Z Sports)
- Open A–Z Sports menu  
- Select Tennis  
- Verify correct navigation and page load  

### 4. Responsive Design
- Run all scenarios on **desktop** and **mobile** viewports  

## Project Structure
```
sportsbook_ui_py/
├─ components/             # Reusable UI parts
│  ├─ az_sports_panel.py   # A–Z Sports menu
│  └─ betslip.py           # Betslip (desktop tab & mobile modal)
│
├─ pages/                  # Page Objects
│  ├─ base_page.py         # Common UI actions (click, fill, waits)
│  ├─ live_page.py         # Live events grid
│  └─ event_view_page.py   # Event details (odds, selections)
│
├─ tests/                  # Test specs
│  ├─ test_az_sports.py    # Sport sorting (desktop)
│  ├─ test_betslip.py      # Betslip add pick (desktop)
│  ├─ test_live_updates.py # Live odds update (desktop)
│  ├─ test_mobile.py       # Mobile versions of all scenarios
│
├─ conftest.py             # Fixtures, Playwright setup, device handling
├─ pytest.ini              # Markers & pytest config
├─ requirements.txt        # Dependencies
└─ README.md               # Documentation 