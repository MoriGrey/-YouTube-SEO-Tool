# YouTube SEO AGI Tool 🎸

Universal Self-Evolving Open-Source AGI Assistant for YouTube Channel Optimization

**Target Channel:** @anatolianturkishrock  
**Niche:** Psychedelic Anatolian Rock

---

## 🚀 Features

### Faz 1: Temel Altyapı ✅
- ✅ Python virtual environment setup
- ✅ YouTube Data API v3 integration
- ✅ CLI interface with multiple commands

### Faz 2: Analiz Modülleri ✅
- ✅ **Channel Analyzer**: Comprehensive channel performance analysis
- ✅ **Keyword Researcher**: Advanced keyword research and SEO analysis
- ✅ **Competitor Analyzer**: Competitor channel analysis and strategy insights

### Faz 3: Optimizasyon Araçları ✅
- ✅ **Title Optimizer**: Generate SEO-optimized title variations
- ✅ **Description Generator**: Create SEO-optimized video descriptions
- ✅ **Tag Suggester**: Suggest optimized tags for videos

### Faz 4: Akıllı Özellikler ✅
- ✅ **Trend Predictor**: Predict trending topics and optimal posting times
- ✅ **Proactive Advisor**: Get proactive suggestions and alerts

### Faz 5: Dashboard ve Raporlama ✅
- ✅ **Streamlit Dashboard**: Interactive web dashboard
- ✅ **Report Generator**: Automated PDF report generation

---

## 📦 Installation

1. **Clone or navigate to the project:**
   ```bash
   cd YouTube-SEO-AGI-Tool
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your YouTube API key:
     ```
     YOUTUBE_API_KEY=your_api_key_here
     ```

---

## 🎯 Usage

### CLI Commands

```bash
# Test API connection
python main.py test

# Analyze channel
python main.py channel

# Comprehensive analysis
python main.py analyze

# Optimize title
python main.py optimize-title "GEL I 70's Psychedelic Turkish Rock" --song "GEL"

# Generate description
python main.py generate-desc "GEL I 70's Psychedelic Turkish Rock" --song "GEL"

# Suggest tags
python main.py suggest-tags "GEL I 70's Psychedelic Turkish Rock" --song "GEL"

# Get proactive suggestions
python main.py proactive

# Search YouTube
python main.py search "psychedelic anatolian rock"

# Get keyword suggestions
python main.py suggest

# Show help
python main.py --help
```

### Web Dashboard

```bash
streamlit run dashboard.py
```

Then open your browser to `http://localhost:8501`

---

## 📁 Project Structure

```
YouTube-SEO-AGI-Tool/
├── src/
│   ├── modules/
│   │   ├── channel_analyzer.py      # Channel analysis
│   │   ├── keyword_researcher.py    # Keyword research
│   │   ├── competitor_analyzer.py   # Competitor analysis
│   │   ├── title_optimizer.py       # Title optimization
│   │   ├── description_generator.py # Description generation
│   │   ├── tag_suggester.py         # Tag suggestions
│   │   ├── trend_predictor.py       # Trend prediction
│   │   ├── proactive_advisor.py    # Proactive suggestions
│   │   └── report_generator.py     # PDF report generation
│   └── utils/
│       └── youtube_client.py        # YouTube API client
├── data/                            # Data storage
├── reports/                         # Generated reports
├── tests/                           # Test files
├── .cursor/
│   └── scratchpad.md                # Project planning
├── dashboard.py                     # Streamlit dashboard
├── main.py                          # CLI interface
├── test_api.py                      # API test script
├── requirements.txt                 # Dependencies
└── README.md                        # This file
```

---

## 🔑 YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "YouTube Data API v3"
4. Create credentials (API Key)
5. Add the key to `.env` file

**Note:** YouTube API has a daily quota of 10,000 units. The tool uses caching to minimize API calls.

---

## 🎨 AGI Paradigms Implemented

- **Fractal Knowledge Acquisition**: Each keyword leads to more keywords
- **Self-Evolving Architecture**: System learns and adapts
- **Omnipresent Data Mining**: Unified access to YouTube's knowledge
- **Proactive Assistant Interface**: Provides suggestions without being asked
- **Continuous Learning Mechanism**: Tracks trends and adapts

---

## 📊 Current Channel Status

- **Channel:** Anatolian Turkish Rock
- **Subscribers:** 11
- **Total Views:** 1,738
- **Videos:** 6
- **Average Views/Video:** 298

---

## 🛠️ Development

### Running Tests

```bash
python test_api.py
```

### Adding New Features

1. Create module in `src/modules/`
2. Add CLI command in `main.py`
3. Add dashboard page in `dashboard.py`
4. Update documentation

---

## 📝 License

This project is part of the Universal Self-Evolving Open-Source AGI Assistant initiative.

---

## 🤝 Contributing

This is a specialized tool for @anatolianturkishrock channel optimization. For questions or improvements, please refer to the project documentation.

---

**Built with ❤️ for Psychedelic Anatolian Rock enthusiasts**

