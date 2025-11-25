"""
YouTube SEO AGI Tool - Streamlit Dashboard
Interactive web dashboard for channel analysis and optimization.
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

# Load environment
load_dotenv()

# Add project root to path
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

# CRITICAL: Initialize session state keys FIRST, before any imports that use them
# Streamlit-Authenticator accesses these keys internally
# According to Streamlit docs: https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization
# These must be initialized before authenticator methods are called
if 'logout' not in st.session_state:
    st.session_state['logout'] = False
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = None

# CRITICAL: Initialize session state keys FIRST, before any imports that use them
# Streamlit-Authenticator accesses these keys internally
# According to Streamlit docs: https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization
# These must be initialized before authenticator methods are called
if 'logout' not in st.session_state:
    st.session_state['logout'] = False
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = None

from src.utils.youtube_client import YouTubeClient, create_client
from src.modules.channel_analyzer import ChannelAnalyzer
from src.modules.keyword_researcher import KeywordResearcher
from src.modules.competitor_analyzer import CompetitorAnalyzer
from src.modules.title_optimizer import TitleOptimizer
from src.modules.description_generator import DescriptionGenerator
from src.modules.tag_suggester import TagSuggester
from src.modules.trend_predictor import TrendPredictor
from src.modules.proactive_advisor import ProactiveAdvisor
from src.modules.performance_tracker import PerformanceTracker
from src.modules.milestone_tracker import MilestoneTracker
from src.modules.feedback_learner import FeedbackLearner
from src.modules.viral_predictor import ViralPredictor
from src.modules.competitor_benchmark import CompetitorBenchmark
from src.modules.multi_source_integrator import MultiSourceIntegrator
from src.modules.knowledge_graph import KnowledgeGraph
from src.modules.continuous_learner import ContinuousLearner
from src.modules.code_self_improver import CodeSelfImprover
from src.modules.safety_ethics_layer import SafetyEthicsLayer
from src.modules.video_seo_audit import VideoSEOAudit
from src.modules.caption_optimizer import CaptionOptimizer
from src.modules.engagement_booster import EngagementBooster
from src.modules.thumbnail_enhancer import ThumbnailEnhancer
from src.utils.i18n import t, get_language, set_language
from src.utils.process_manager import ProcessManager
from src.utils.encryption import encrypt_api_key, decrypt_api_key, get_encryption_manager
from src.utils.logger import get_logger
from src.utils.auth import get_auth_manager, require_auth
from src.utils.rate_limiter import get_rate_limiter, check_rate_limit
from src.utils.input_validator import get_validator, validate_channel_handle, validate_niche, sanitize_string

# Initialize logger
logger = get_logger("youtube_seo_agi_dashboard")

# Initialize authentication
# Note: Session state keys are already initialized at the top of the file
auth_manager = get_auth_manager()

# Initialize rate limiter
rate_limiter = get_rate_limiter()

# CRITICAL: Restore authentication from cookie BEFORE checking authentication
# Streamlit-Authenticator automatically reads cookie and sets 'authentication_status', 'name', 'username'
# We need to sync these with our session state keys BEFORE checking is_authenticated()
# This must happen BEFORE any authenticator method calls that might reset the state
auth_manager._restore_from_cookie()

# Require authentication (check at the very start)
# Only show login form if not authenticated
if not auth_manager.is_authenticated():
    # Show login form
    st.title("🔐 YouTube SEO AGI Tool - Login")
    st.markdown("---")
    
    # Show default credentials info (only if not already shown)
    if "login_info_shown" not in st.session_state:
        st.info("""
        **Default Credentials (for first-time setup):**
        - Username: `admin`
        - Password: `admin123`
        
        **⚠️ Important:** Change the default password after first login!
        """)
        st.session_state.login_info_shown = True
    
    # Call login - this will render the login form
    # Note: login() returns None when form is displayed (waiting for input)
    # IMPORTANT: login() also checks cookie and may restore authentication
    login_result = auth_manager.login()
    
    # After login() call, check again if authenticated (cookie might have been restored)
    if auth_manager.is_authenticated():
        # Authentication restored from cookie or successful login
        st.rerun()
    elif login_result is True:
        # Login successful, rerun to show dashboard
        st.rerun()
    elif login_result is False:
        # Login failed (wrong credentials)
        # Error message already shown by auth_manager
        # Don't stop, let user try again
        pass
    else:
        # login_result is None - form is shown, waiting for user input
        # Form is already rendered by authenticator.login()
        # Don't call st.stop() - let the form be visible and wait for user input
        pass

# Check rate limit for authenticated users
if auth_manager.is_authenticated():
    allowed, error_msg = check_rate_limit("dashboard_action")
    if not allowed:
        st.error(f"⚠️ **Rate Limit Exceeded**")
        st.warning(error_msg)
        rate_status = rate_limiter.get_rate_limit_status()
        if rate_status.get('blocked'):
            remaining = rate_status.get('blocked_remaining_minutes', 0)
            st.info(f"You are temporarily blocked. Please try again in {remaining} minutes.")
        st.stop()

# Page config
st.set_page_config(
    page_title="YouTube SEO AGI Tool",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Theme CSS
st.markdown("""
<style>
    /* Dark Theme Global Styles */
    .main .block-container {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Card Styling for Dark Theme */
    .card-wrapper {
        border: 1px solid #3a3f4b !important;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        background: #1e2229 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        color: #fafafa;
    }
    
    .card-title {
        margin: 0 0 0.5rem 0;
        color: #fafafa !important;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .card-subtitle {
        color: #b0b0b0 !important;
        font-size: 0.9rem;
        margin: 0.3rem 0;
    }
    
    .card-content {
        color: #d0d0d0 !important;
        line-height: 1.6;
        margin-top: 0.5rem;
    }
    
    /* Streamlit elements dark theme adjustments */
    .stMarkdown {
        color: #fafafa;
    }
    
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #fafafa;
    }
    
    .stSelectbox > div > div > select {
        background-color: #262730;
        color: #fafafa;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #262730;
        color: #fafafa;
    }
    
    /* Sidebar dark theme */
    .css-1d391kg {
        background-color: #0e1117;
    }
    
    /* Metric colors for dark theme */
    .metric-default {
        color: #4a9eff !important;
    }
    
    .metric-success {
        color: #4caf50 !important;
    }
    
    .metric-warning {
        color: #ffc107 !important;
    }
    
    .metric-error {
        color: #f44336 !important;
    }
    
    .metric-info {
        color: #17a2b8 !important;
    }
    
    /* Button styling for dark theme */
    .stButton > button {
        background-color: #262730;
        color: #fafafa;
        border: 1px solid #3a3f4b;
    }
    
    .stButton > button:hover {
        background-color: #3a3f4b;
        border-color: #4a9eff;
    }
    
    /* Dataframe styling */
    .dataframe {
        background-color: #1e2229;
        color: #fafafa;
    }
    
    /* Info, success, warning, error boxes */
    .stAlert {
        background-color: #1e2229;
        border: 1px solid #3a3f4b;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: #1e2229;
        border: 1px solid #3a3f4b;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
# CRITICAL: Initialize required keys for Streamlit-Authenticator BEFORE any usage
# According to Streamlit docs: https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization
# These keys must be initialized before authenticator methods are called
if 'logout' not in st.session_state:
    st.session_state['logout'] = False
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = None
# Initialize Streamlit-Authenticator's internal keys if needed
if '_streamlit_authenticator' not in st.session_state:
    # This key is used internally by Streamlit-Authenticator
    pass  # Will be initialized by authenticator itself

# Initialize target channel and niche (empty by default - user will fill in)
if "target_channel" not in st.session_state:
    st.session_state.target_channel = ""
if "target_niche" not in st.session_state:
    st.session_state.target_niche = ""

# Log app initialization
if "app_initialized" not in st.session_state:
    logger.info("Application initialized", app_version="1.0.0")
    logger.audit_trail("app_started")
    st.session_state.app_initialized = True
if "user_api_key" not in st.session_state:
    # Try to get from environment variable first (for local/dev)
    env_key = os.getenv("YOUTUBE_API_KEY", "")
    st.session_state.user_api_key = env_key
    # Store encrypted version if we have a key
    if env_key:
        try:
            st.session_state.encrypted_api_key = encrypt_api_key(env_key)
        except Exception:
            # If encryption fails, store as plaintext (fallback)
            st.session_state.encrypted_api_key = env_key
    else:
        st.session_state.encrypted_api_key = ""
if "encrypted_api_key" not in st.session_state:
    st.session_state.encrypted_api_key = ""
if "api_key_configured" not in st.session_state:
    st.session_state.api_key_configured = bool(st.session_state.user_api_key)

# Initialize client only if API key is configured
def initialize_client():
    """Initialize YouTube client with user's API key (decrypted if encrypted)."""
    if not st.session_state.user_api_key:
        return None
    
    # Get decrypted API key
    api_key = st.session_state.user_api_key
    
    # If we have encrypted version, try to decrypt
    if st.session_state.get("encrypted_api_key"):
        try:
            encryption_manager = get_encryption_manager()
            if encryption_manager.is_encrypted(st.session_state.encrypted_api_key):
                api_key = decrypt_api_key(st.session_state.encrypted_api_key)
        except Exception as e:
            # If decryption fails, use plaintext version
            st.warning("⚠️ API key decryption failed, using plaintext version")
            api_key = st.session_state.user_api_key
    
    try:
        client = create_client(api_key=api_key)
        logger.info("YouTube client initialized successfully")
        logger.api_usage("youtube", "client_init", "success")
        return client
    except Exception as e:
        logger.error(f"Error initializing YouTube client: {e}", error_type="client_init_error")
        logger.api_usage("youtube", "client_init", "error", error_message=str(e))
        st.error(f"Error initializing client: {e}")
        return None

# Initialize client if API key is available
if st.session_state.api_key_configured and "client" not in st.session_state:
    try:
        st.session_state.client = initialize_client()
        st.session_state.channel_analyzer = ChannelAnalyzer(st.session_state.client)
        st.session_state.keyword_researcher = KeywordResearcher(st.session_state.client)
        st.session_state.competitor_analyzer = CompetitorAnalyzer(st.session_state.client)
        st.session_state.title_optimizer = TitleOptimizer(st.session_state.keyword_researcher)
        st.session_state.description_generator = DescriptionGenerator()
        st.session_state.tag_suggester = TagSuggester(st.session_state.client)
        st.session_state.trend_predictor = TrendPredictor(st.session_state.client)
        st.session_state.proactive_advisor = ProactiveAdvisor(
            st.session_state.client,
            st.session_state.channel_analyzer,
            st.session_state.competitor_analyzer
        )
        st.session_state.performance_tracker = PerformanceTracker(st.session_state.client)
        st.session_state.milestone_tracker = MilestoneTracker(st.session_state.client)
        st.session_state.feedback_learner = FeedbackLearner(
            st.session_state.client,
            st.session_state.performance_tracker
        )
        st.session_state.viral_predictor = ViralPredictor(
            st.session_state.client,
            st.session_state.channel_analyzer,
            st.session_state.keyword_researcher
        )
        st.session_state.competitor_benchmark = CompetitorBenchmark(
            st.session_state.client,
            st.session_state.channel_analyzer,
            st.session_state.competitor_analyzer
        )
        st.session_state.multi_source_integrator = MultiSourceIntegrator(st.session_state.client)
        st.session_state.knowledge_graph = KnowledgeGraph(
            st.session_state.client,
            st.session_state.performance_tracker,
            st.session_state.feedback_learner,
            st.session_state.multi_source_integrator,
            st.session_state.competitor_benchmark
        )
        st.session_state.continuous_learner = ContinuousLearner(
            st.session_state.client,
            st.session_state.performance_tracker,
            st.session_state.feedback_learner,
            st.session_state.multi_source_integrator,
            st.session_state.knowledge_graph,
            st.session_state.trend_predictor
        )
        st.session_state.code_self_improver = CodeSelfImprover(
            st.session_state.client,
            st.session_state.performance_tracker,
            st.session_state.feedback_learner,
            st.session_state.knowledge_graph,
            st.session_state.viral_predictor
        )
        st.session_state.safety_ethics_layer = SafetyEthicsLayer()
        st.session_state.video_seo_audit = VideoSEOAudit(
            st.session_state.client,
            st.session_state.keyword_researcher,
            st.session_state.title_optimizer,
            st.session_state.description_generator,
            st.session_state.tag_suggester
        )
        st.session_state.caption_optimizer = CaptionOptimizer(
            st.session_state.client,
            st.session_state.keyword_researcher
        )
        st.session_state.engagement_booster = EngagementBooster(st.session_state.client)
        st.session_state.thumbnail_enhancer = ThumbnailEnhancer(st.session_state.client)
        st.session_state.process_manager = ProcessManager()
        logger.info("All modules initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing modules: {e}", error_type="module_init_error", 
                    module_count=len([k for k in st.session_state.keys() if not k.startswith('_')]))
        st.error(f"Error initializing: {e}")
        st.stop()

# Initialize target channel and niche if not set (empty by default)
if "target_channel" not in st.session_state:
    st.session_state.target_channel = ""
if "target_niche" not in st.session_state:
    st.session_state.target_niche = ""
if "language" not in st.session_state:
    st.session_state.language = "tr"  # Default to Turkish

# Helper Functions
def render_card(title, content, metric=None, icon="", color="default", subtitle=""):
    """Render a card component with title, content, and optional metric."""
    import html
    
    # Dark theme color map
    color_map = {
        "default": "#4a9eff",
        "success": "#4caf50",
        "warning": "#ffc107",
        "error": "#f44336",
        "info": "#17a2b8"
    }
    metric_color = color_map.get(color, color_map["default"])
    
    # Use Streamlit container for better control
    with st.container():
        # Card wrapper with dark theme CSS
        st.markdown(f"""
        <div class="card-wrapper">
        """, unsafe_allow_html=True)
        
        # Title
        st.markdown(f"### {icon} {title}")
        
        # Subtitle
        if subtitle:
            st.caption(subtitle)
        
        # Metric with dark theme color
        if metric:
            st.markdown(f'<div class="card-metric" style="font-size: 2rem; font-weight: bold; color: {metric_color}; margin: 0.5rem 0;">{html.escape(str(metric))}</div>', unsafe_allow_html=True)
        
        # Content - render as markdown to handle HTML properly
        # Convert <br> to newlines and <b> to ** for markdown
        content_str = str(content)
        # Replace HTML tags with markdown equivalents
        content_str = content_str.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
        content_str = content_str.replace('<b>', '**').replace('</b>', '**')
        content_str = content_str.replace('<strong>', '**').replace('</strong>', '**')
        # Remove other HTML tags but keep text
        import re
        content_str = re.sub(r'<[^>]+>', '', content_str)
        
        st.markdown(content_str)
        
        st.markdown("</div>", unsafe_allow_html=True)

def update_channel_state():
    """Callback to update channel in session state when input changes."""
    channel = st.session_state.get("target_channel", "")
    # Clean and validate
    cleaned_channel = channel.lstrip("@").strip() if channel else ""
    is_valid, _ = validate_channel_handle(cleaned_channel)
    if is_valid or not cleaned_channel:
        st.session_state.target_channel = cleaned_channel

def update_niche_state():
    """Callback to update niche in session state when input changes."""
    niche = st.session_state.get("target_niche", "")
    # Clean and validate
    cleaned_niche = sanitize_string(niche.strip(), max_length=200) if niche else ""
    is_valid, _ = validate_niche(cleaned_niche)
    if is_valid or not cleaned_niche:
        st.session_state.target_niche = cleaned_niche

def render_channel_niche_inputs():
    """Render channel and niche input fields at the top of each page."""
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        # Use target_channel directly as key for automatic syncing
        channel = st.text_input(
            t("forms.target_channel"), 
            value=st.session_state.get("target_channel", ""),
            placeholder="Örn: mori_grey veya @mori_grey",
            key="target_channel",  # Direct key sync with session state
            help=t("forms.channel_help"),
            on_change=update_channel_state  # Update session state immediately on change
        )
        # Validate channel handle and show error if needed
        channel_value = st.session_state.get("target_channel", "")
        is_valid, error_msg = validate_channel_handle(channel_value)
        if not is_valid and channel_value:  # Only show error if user entered something
            st.error(f"⚠️ {error_msg}")
            logger.warning(f"Invalid channel handle: {error_msg}", channel_input=channel_value[:20])
    with col2:
        # Use target_niche directly as key for automatic syncing
        niche = st.text_input(
            t("forms.niche"), 
            value=st.session_state.get("target_niche", ""),
            placeholder="Örn: Techno Music, Psychedelic Rock",
            key="target_niche",  # Direct key sync with session state
            help=t("forms.niche_help"),
            on_change=update_niche_state  # Update session state immediately on change
        )
        # Validate niche and show error if needed
        niche_value = st.session_state.get("target_niche", "")
        is_valid, error_msg = validate_niche(niche_value)
        if not is_valid and niche_value:  # Only show error if user entered something
            st.error(f"⚠️ {error_msg}")
            logger.warning(f"Invalid niche: {error_msg}", niche_input=niche_value[:50])
    st.markdown("---")

# Sidebar
with st.sidebar:
    st.title(t("app.title"))
    
    # User Info
    if auth_manager.is_authenticated():
        user_name = auth_manager.get_user_name()
        username = auth_manager.get_username()
        st.markdown(f"**👤 User:** {user_name or username}")
        st.markdown("---")
    
    # Navigation with Primary and Secondary Panels (ÜSTTE)
    # Primary Panels (Top Section)
    primary_pages = [
        t("navigation.dashboard"),
        t("navigation.channel_analysis"),
        t("navigation.keyword_research"),
        t("navigation.competitor_analysis"),
        t("navigation.title_optimizer"),
        t("navigation.description_generator"),
        t("navigation.tag_suggester"),
        t("navigation.trend_predictor"),
        t("navigation.viral_predictor"),
        t("navigation.proactive_advisor")
    ]
    
    # Secondary Panels (Bottom Section)
    secondary_pages = [
        t("navigation.performance_tracking"),
        t("navigation.milestone_tracker"),
        t("navigation.feedback_learning"),
        t("navigation.competitor_benchmark"),
        t("navigation.multi_source_data"),
        t("navigation.knowledge_graph"),
        t("navigation.continuous_learning"),
        t("navigation.code_self_improvement"),
        t("navigation.safety_ethics"),
        "🔍 Video SEO Audit",
        "📝 Caption Optimizer",
        "🎯 Engagement Booster",
        "🖼️ Thumbnail Enhancer"
    ]
    
    # Combine all pages: primary first, then secondary
    all_pages = primary_pages + secondary_pages
    
    # Initialize current page if not exists
    if "current_page" not in st.session_state:
        st.session_state.current_page = t("navigation.dashboard")
    
    # Display navigation with visual grouping
    st.markdown("### 🎯 Öncelikli Paneller")
    st.caption("Ana kontrol panelleri ve temel özellikler")
    
    # Primary panel selectbox
    primary_index = 0
    if st.session_state.current_page in primary_pages:
        primary_index = primary_pages.index(st.session_state.current_page)
    
    selected_primary = st.selectbox(
        "Ana Paneller",
        primary_pages,
        index=primary_index,
        key="primary_nav_select",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📊 İkincil Paneller")
    st.caption("Gelişmiş analiz ve optimizasyon araçları")
    
    # Secondary panel selectbox
    secondary_index = 0
    if st.session_state.current_page in secondary_pages:
        secondary_index = secondary_pages.index(st.session_state.current_page)
    
    selected_secondary = st.selectbox(
        "İkincil Paneller",
        secondary_pages,
        index=secondary_index,
        key="secondary_nav_select",
        label_visibility="collapsed"
    )
    
    # Determine which page is selected
    # Track previous selections to detect changes
    if "prev_primary" not in st.session_state:
        st.session_state.prev_primary = selected_primary
    if "prev_secondary" not in st.session_state:
        st.session_state.prev_secondary = selected_secondary
    
    # If primary changed, use primary; if secondary changed, use secondary
    if selected_primary != st.session_state.prev_primary:
        page = selected_primary
        st.session_state.current_page = selected_primary
    elif selected_secondary != st.session_state.prev_secondary:
        page = selected_secondary
        st.session_state.current_page = selected_secondary
    else:
        # Use current page from session state
        page = st.session_state.current_page
    
    # Update previous values
    st.session_state.prev_primary = selected_primary
    st.session_state.prev_secondary = selected_secondary
    
    # ALTTA: Dil Seçimi, API Key, Target Channel/Niche, Rate Limit, Logout
    st.markdown("---")
    st.markdown("---")
    
    # Language selector
    st.markdown("### 🌐 Dil Seçimi")
    lang_options = {
        "Türkçe": "tr",
        "English": "en"
    }
    current_lang = get_language()
    selected_lang_display = "Türkçe" if current_lang == "tr" else "English"
    selected_lang = st.selectbox(
        t("app.language_selector"),
        options=list(lang_options.keys()),
        index=0 if current_lang == "tr" else 1,
        label_visibility="collapsed"
    )
    if lang_options[selected_lang] != current_lang:
        set_language(lang_options[selected_lang])
        st.rerun()
    
    st.markdown("---")
    
    # API Key Management (Multi-user support)
    st.markdown("### 🔑 API Key")
    
    # Show current status
    if st.session_state.api_key_configured:
        st.success("✅ API Key Configured")
        if st.button("🔄 Change API Key"):
            # Log security event
            logger.security_event("api_key_change_initiated", "User initiated API key change")
            logger.audit_trail("api_key_changed", action_type="change_initiated")
            
            st.session_state.api_key_configured = False
            st.session_state.user_api_key = ""
            st.session_state.encrypted_api_key = ""
            if "client" in st.session_state:
                del st.session_state.client
            st.rerun()
    else:
        st.warning("⚠️ API Key Required")
        api_key_input = st.text_input(
            "YouTube API Key",
            value="",
            type="password",
            help="Enter your YouTube Data API v3 key. Get one for free at: https://console.cloud.google.com/apis/credentials",
            key="api_key_input"
        )
        
        if st.button("💾 Save API Key", type="primary"):
            if api_key_input:
                # Validate API key format
                validator = get_validator()
                is_valid, error_msg = validator.validate_api_key(api_key_input.strip())
                
                if not is_valid:
                    st.error(f"⚠️ {error_msg}")
                    logger.warning(f"Invalid API key format: {error_msg}")
                elif len(api_key_input.strip()) > 20:
                    try:
                        # Encrypt API key before storing
                        encrypted_key = encrypt_api_key(api_key_input.strip())
                        
                        # Store both encrypted and plaintext (plaintext only in memory for current session)
                        st.session_state.user_api_key = api_key_input.strip()
                        st.session_state.encrypted_api_key = encrypted_key
                        st.session_state.api_key_configured = True
                        
                        # Log security event
                        logger.security_event(
                            "api_key_saved",
                            "API key saved and encrypted",
                            key_length=len(api_key_input.strip()),
                            encrypted=True
                        )
                        logger.audit_trail("api_key_changed", action_type="save")
                        
                        # Reinitialize modules with new API key
                        if "client" in st.session_state:
                            del st.session_state.client
                        st.rerun()
                    except Exception as e:
                        logger.error(f"Failed to encrypt API key: {e}", error_type="encryption_error")
                        st.error(f"Failed to encrypt API key: {e}")
                        # Fallback: store as plaintext (not recommended but better than failing)
                        st.warning("⚠️ Encryption failed, storing as plaintext (not secure)")
                        logger.warning("API key stored as plaintext due to encryption failure")
                        st.session_state.user_api_key = api_key_input.strip()
                        st.session_state.encrypted_api_key = api_key_input.strip()
                        st.session_state.api_key_configured = True
                        if "client" in st.session_state:
                            del st.session_state.client
                        st.rerun()
                else:
                    st.error("Please enter a valid API key (at least 20 characters)")
            else:
                st.error("Please enter an API key")
    
    st.markdown("---")
    channel_display = f"@{st.session_state.target_channel}" if st.session_state.target_channel else "Henüz girilmedi"
    niche_display = st.session_state.target_niche.title() if st.session_state.target_niche else "Henüz girilmedi"
    st.markdown(f"**{t('common.target_channel')}:** {channel_display}")
    st.markdown(f"**{t('common.niche')}:** {niche_display}")
    
    # Rate Limit Status
    if auth_manager.is_authenticated():
        st.markdown("---")
        rate_status = rate_limiter.get_rate_limit_status()
        if rate_status.get('blocked'):
            st.error("🚫 **Rate Limited**")
            remaining = rate_status.get('blocked_remaining_minutes', 0)
            st.caption(f"Blocked for {remaining} more minutes")
        else:
            st.info("✅ **Rate Limit OK**")
            st.caption(f"{rate_status['requests_last_minute']}/{rate_status['limits']['per_minute']} per minute")
    
    # Logout button
    st.markdown("---")
    if auth_manager.is_authenticated():
        # Initialize logout key if not exists
        if 'logout' not in st.session_state:
            st.session_state['logout'] = False
        
        if st.button("🚪 Logout", use_container_width=True):
            try:
                auth_manager.logout()
                # Clear all session state
                for key in list(st.session_state.keys()):
                    if key not in ['_streamlit_authenticator']:
                        del st.session_state[key]
                st.rerun()
            except Exception as e:
                # Manual logout if authenticator fails
                st.session_state['authenticated'] = False
                st.session_state['username'] = None
                st.session_state['user_name'] = None
                st.rerun()

# Main content
current_lang = get_language()

# Helper function to check page
def is_page(page_key):
    """Check if current page matches the key."""
    page_translations = {
        "dashboard": [t("navigation.dashboard"), "📊 Dashboard", "📊 Kontrol Paneli"],
        "channel_analysis": [t("navigation.channel_analysis"), "📈 Channel Analysis", "📈 Kanal Analizi"],
        "keyword_research": [t("navigation.keyword_research"), "🔍 Keyword Research", "🔍 Anahtar Kelime Araştırması"],
        "competitor_analysis": [t("navigation.competitor_analysis"), "⚔️ Competitor Analysis", "⚔️ Rakip Analizi"],
        "title_optimizer": [t("navigation.title_optimizer"), "✏️ Title Optimizer", "✏️ Başlık Optimizasyonu"],
        "description_generator": [t("navigation.description_generator"), "📝 Description Generator", "📝 Açıklama Üretici"],
        "tag_suggester": [t("navigation.tag_suggester"), "🏷️ Tag Suggester", "🏷️ Etiket Önerici"],
        "trend_predictor": [t("navigation.trend_predictor"), "📅 Trend Predictor", "📅 Trend Tahmincisi"],
        "proactive_advisor": [t("navigation.proactive_advisor"), "💡 Proactive Advisor", "💡 Proaktif Danışman"],
        "performance_tracking": [t("navigation.performance_tracking"), "📊 Performance Tracking", "📊 Performans Takibi"],
        "milestone_tracker": [t("navigation.milestone_tracker"), "🎯 Milestone Tracker", "🎯 Milestone Takipçisi"],
        "feedback_learning": [t("navigation.feedback_learning"), "🧠 Feedback Learning", "🧠 Geri Bildirim Öğrenme"],
        "viral_predictor": [t("navigation.viral_predictor"), "🔥 Viral Predictor", "🔥 Viral Tahmincisi"],
        "competitor_benchmark": [t("navigation.competitor_benchmark"), "📊 Competitor Benchmark", "📊 Rakip Kıyaslama"],
        "multi_source_data": [t("navigation.multi_source_data"), "🌐 Multi-Source Data", "🌐 Çok Kaynaklı Veri"],
        "knowledge_graph": [t("navigation.knowledge_graph"), "🧠 Knowledge Graph", "🧠 Bilgi Grafiği"],
        "continuous_learning": [t("navigation.continuous_learning"), "🔄 Continuous Learning", "🔄 Sürekli Öğrenme"],
        "code_self_improvement": [t("navigation.code_self_improvement"), "⚙️ Code Self-Improvement", "⚙️ Kod Kendini Geliştirme"],
        "safety_ethics": [t("navigation.safety_ethics"), "🛡️ Safety & Ethics", "🛡️ Güvenlik ve Etik"],
        "video_seo_audit": ["🔍 Video SEO Audit", "🔍 Video SEO Audit", "🔍 Video SEO Denetimi"],
        "caption_optimizer": ["📝 Caption Optimizer", "📝 Caption Optimizer", "📝 Altyazı Optimizasyonu"],
        "engagement_booster": ["🎯 Engagement Booster", "🎯 Engagement Booster", "🎯 Etkileşim Artırıcı"],
        "thumbnail_enhancer": ["🖼️ Thumbnail Enhancer", "🖼️ Thumbnail Enhancer", "🖼️ Küçük Resim Geliştirici"]
    }
    return page in page_translations.get(page_key, [])

# Check if API key is configured before showing pages
if not st.session_state.api_key_configured or "client" not in st.session_state or st.session_state.client is None:
    st.warning("⚠️ **API Key Required**")
    st.info("""
    Please configure your YouTube API key in the sidebar to use this application.
    
    **How to get a free API key:**
    1. Go to [Google Cloud Console](https://console.cloud.google.com)
    2. Create a new project or select existing one
    3. Enable "YouTube Data API v3"
    4. Create credentials > API Key
    5. Copy and paste your API key in the sidebar
    
    **Note:** YouTube API is completely free with 10,000 daily quota units (sufficient for most use cases).
    """)
    st.stop()

if is_page("dashboard"):
    st.title(t("pages.dashboard.title"))
    st.markdown(t("pages.dashboard.description"))
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    # Quick stats in card grid
    try:
        # Validate channel handle
        if not st.session_state.target_channel or not st.session_state.target_channel.strip():
            st.warning(t("messages.channel_not_found") + " " + t("forms.channel_help"))
        else:
            # Check rate limit before API call
            allowed, error_msg = check_rate_limit("youtube_api")
            if not allowed:
                st.error(f"⚠️ **Rate Limit Exceeded**")
                st.warning(error_msg)
                rate_status = rate_limiter.get_rate_limit_status()
                if rate_status.get('blocked'):
                    remaining = rate_status.get('blocked_remaining_minutes', 0)
                    st.info(f"Please try again in {remaining} minutes.")
                st.stop()
            
            channel_data = st.session_state.client.get_channel_by_handle(st.session_state.target_channel)
            if channel_data.get("items"):
                channel = channel_data["items"][0]
                stats = channel["statistics"]
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    render_card(
                        title=t("common.subscribers"),
                        content=t("cards.total_channel_subscribers"),
                        metric=f"{int(stats.get('subscriberCount', 0)):,}",
                        icon="👥",
                        color="info"
                    )
                with col2:
                    render_card(
                        title=t("common.total_views"),
                        content=t("cards.all_time_video_views"),
                        metric=f"{int(stats.get('viewCount', 0)):,}",
                        icon="👁️",
                        color="info"
                    )
                with col3:
                    render_card(
                        title=t("common.videos"),
                        content=t("cards.total_published_videos"),
                        metric=f"{stats.get('videoCount', 0)}",
                        icon="📹",
                        color="info"
                    )
                with col4:
                    avg_views = int(stats.get("viewCount", 0)) / max(int(stats.get("videoCount", 1)), 1)
                    render_card(
                        title=t("common.avg_views_per_video"),
                        content=t("cards.average_views_per_video"),
                        metric=f"{avg_views:,.0f}",
                        icon="📊",
                        color="info"
                    )
            else:
                st.warning(t("messages.channel_not_found"))
    except ValueError as e:
        # Handle validation errors (empty channel handle)
        st.warning(str(e))
    except Exception as e:
        st.error(t("messages.error_loading", error=str(e)))
    
    # Proactive suggestions in card format
    st.markdown(f"### 💡 {t('pages.dashboard.proactive_suggestions')}")
    
    try:
        suggestions = st.session_state.proactive_advisor.get_proactive_suggestions(st.session_state.target_channel)
        
        if suggestions.get("alerts"):
            alert_cols = st.columns(min(len(suggestions["alerts"]), 3))
            for idx, alert in enumerate(suggestions["alerts"]):
                col_idx = idx % 3
                with alert_cols[col_idx]:
                    alert_type = alert.get("type", "info")
                    color_map = {
                        "warning": "warning",
                        "error": "error",
                        "info": "info"
                    }
                    render_card(
                        title=alert.get("title", "Alert"),
                        content=alert.get("message", ""),
                        icon="⚠️" if alert_type == "warning" else "❌" if alert_type == "error" else "ℹ️",
                        color=color_map.get(alert_type, "info")
                    )
        
        if suggestions.get("suggestions"):
            suggestion_cols = st.columns(min(len(suggestions["suggestions"]), 3))
            for idx, suggestion in enumerate(suggestions["suggestions"]):
                col_idx = idx % 3
                with suggestion_cols[col_idx]:
                    render_card(
                        title=suggestion.get("title", "Suggestion"),
                        content=suggestion.get("message", ""),
                        icon="✅",
                        color="success"
                    )
    except Exception as e:
        st.error(f"Error loading suggestions: {e}")

elif is_page("channel_analysis"):
    st.title(t("pages.channel_analysis.title"))
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    if st.button(t("pages.channel_analysis.analyze_button"), use_container_width=True):
        with st.spinner(t("messages.analyzing")):
            try:
                analysis = st.session_state.channel_analyzer.analyze_channel(st.session_state.target_channel)
                
                # Display results in card format
                st.markdown(f"### {t('pages.channel_analysis.statistics')}")
                stats = analysis["statistics"]
                col1, col2, col3 = st.columns(3)
                with col1:
                    render_card(
                        title=t("common.subscribers"),
                        content=t("cards.total_channel_subscribers"),
                        metric=f"{stats['subscribers']:,}",
                        icon="👥",
                        color="info"
                    )
                with col2:
                    render_card(
                        title=t("common.total_views"),
                        content=t("cards.all_time_video_views"),
                        metric=f"{stats['total_views']:,}",
                        icon="👁️",
                        color="info"
                    )
                with col3:
                    render_card(
                        title=t("common.avg_views_per_video"),
                        content=t("cards.average_views_per_video"),
                        metric=f"{stats['average_views_per_video']:,.0f}",
                        icon="📊",
                        color="info"
                    )
                
                # Video Performance in card format
                st.markdown(f"### {t('pages.channel_analysis.video_performance')}")
                video_perf = analysis["video_performance"]
                col1, col2, col3 = st.columns(3)
                with col1:
                    render_card(
                        title=t("pages.channel_analysis.average_views"),
                        content=t("cards.average_views_per_video"),
                        metric=f"{video_perf.get('average_views', 0):,.0f}",
                        icon="📹",
                        color="info"
                    )
                with col2:
                    render_card(
                        title=t("pages.channel_analysis.average_likes"),
                        content=t("pages.channel_analysis.average_likes"),
                        metric=f"{video_perf.get('average_likes', 0):,.0f}",
                        icon="👍",
                        color="info"
                    )
                with col3:
                    render_card(
                        title=t("pages.channel_analysis.average_comments"),
                        content=t("pages.channel_analysis.average_comments"),
                        metric=f"{video_perf.get('average_comments', 0):,.0f}",
                        icon="💬",
                        color="info"
                    )
                
                # Recommendations in card format
                st.markdown(f"### {t('common.recommendations')}")
                if analysis.get("recommendations"):
                    rec_cols = st.columns(min(len(analysis["recommendations"]), 2))
                    for idx, rec in enumerate(analysis["recommendations"]):
                        col_idx = idx % 2
                        with rec_cols[col_idx]:
                            render_card(
                                title=f"{t('cards.recommendation')} #{idx + 1}",
                                content=rec,
                                icon="💡",
                                color="info"
                            )
                    
            except Exception as e:
                st.error(t("messages.error_loading", error=str(e)))

elif is_page("keyword_research"):
    st.title(t("pages.keyword_research.title"))
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    keywords_input = st.text_area(
        t("pages.keyword_research.enter_keywords"),
        value="",
        placeholder="Örn: techno music\nunderground electronic\nminimal techno\nher satıra bir anahtar kelime"
    )
    
    if st.button(t("pages.keyword_research.research_button"), use_container_width=True):
        with st.spinner(t("messages.researching")):
            try:
                keywords = [k.strip() for k in keywords_input.split("\n") if k.strip()]
                research = st.session_state.keyword_researcher.research_keywords(keywords)
                
                st.markdown(f"### {t('pages.keyword_research.found_keywords', count=research['total_keywords_found'])}")
                
                # Top keywords in card grid
                st.markdown(f"### {t('pages.keyword_research.top_keywords')}")
                ranked_keywords = research["ranked_keywords"][:20]
                keyword_cols = st.columns(min(len(ranked_keywords), 3))
                
                for idx, keyword_data in enumerate(ranked_keywords):
                    col_idx = idx % 3
                    with keyword_cols[col_idx]:
                        search_vol = keyword_data.get('search_volume', 'N/A')
                        competition = keyword_data.get('competition', 'N/A')
                        render_card(
                            title=keyword_data.get("keyword", "N/A"),
                            content=f"Arama Hacmi: {search_vol}<br>Rekabet: {competition}" if current_lang == "tr" else f"Search Volume: {search_vol}<br>Competition: {competition}",
                            metric=f"{t('common.score')}: {keyword_data.get('score', 0):.1f}",
                            icon="🔑",
                            color="info",
                            subtitle=f"{t('pages.keyword_research.rank')} #{idx + 1}"
                        )
                
                # Display as table for detailed view
                df = pd.DataFrame(ranked_keywords)
                st.dataframe(df[["keyword", "score", "competition", "relevance"]])
                
                # Recommendations in card format
                st.markdown(f"### {t('common.recommendations')}")
                if research.get("recommendations"):
                    rec_cols = st.columns(min(len(research["recommendations"]), 2))
                    for idx, rec in enumerate(research["recommendations"]):
                        col_idx = idx % 2
                        with rec_cols[col_idx]:
                            render_card(
                                title=f"{t('cards.recommendation')} #{idx + 1}",
                                content=rec,
                                icon="💡",
                                color="info"
                            )
                    
            except Exception as e:
                st.error(t("messages.error_loading", error=str(e)))

elif is_page("competitor_analysis"):
    st.title(t("pages.competitor_analysis.title"))
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    keywords_input = st.text_area(
        t("pages.competitor_analysis.enter_keywords"),
        value="",
        placeholder="Örn: techno music\nunderground electronic\nher satıra bir anahtar kelime"
    )
    
    if st.button(t("pages.competitor_analysis.find_button"), use_container_width=True):
        with st.spinner(t("messages.loading")):
            try:
                keywords = [k.strip() for k in keywords_input.split("\n") if k.strip()]
                competitors = st.session_state.competitor_analyzer.find_competitors(keywords, max_competitors=10)
                
                st.markdown(f"### {t('pages.competitor_analysis.found_competitors', count=len(competitors))}")
                
                # Competitors in card grid
                competitor_cols = st.columns(min(len(competitors), 3))
                for idx, competitor in enumerate(competitors):
                    col_idx = idx % 3
                    with competitor_cols[col_idx]:
                        # Get channel title (try both field names for compatibility)
                        channel_title = competitor.get("title") or competitor.get("channel_title", "Unknown")
                        # Get channel handle
                        channel_handle = competitor.get("channel_handle", "N/A")
                        # Get relevance score (calculated in analyzer)
                        relevance_score = competitor.get("relevance_score", 0.0)
                        
                        subscribers_text = t("common.subscribers") if current_lang == "tr" else "Subscribers"
                        videos_text = t("common.videos") if current_lang == "tr" else "Videos"
                        views_text = t("common.total_views") if current_lang == "tr" else "Views"
                        
                        render_card(
                            title=channel_title,
                            content=f"{subscribers_text}: {competitor.get('subscribers', 0):,}<br>{videos_text}: {competitor.get('video_count', 0)}<br>{views_text}: {competitor.get('total_views', 0):,}",
                            metric=f"{t('common.score')}: {relevance_score:.2f}",
                            icon="⚔️",
                            color="info",
                            subtitle=f"@{channel_handle}" if channel_handle != "N/A" else f"ID: {competitor.get('channel_id', 'N/A')[:15]}..."
                        )
                
                # Detailed table view
                df = pd.DataFrame(competitors)
                st.dataframe(df)
                
            except Exception as e:
                st.error(t("messages.error_loading", error=str(e)))
    
    # Gap Analysis Section
    st.markdown("---")
    st.markdown("### 🔍 Gap Analysis")
    st.markdown("Compare your channel with competitors to identify content, keyword, and strategy gaps.")
    
    your_channel_handle_gap = st.text_input(
        "Your Channel Handle (e.g., anatolianturkishrock)",
        value=st.session_state.target_channel if st.session_state.target_channel else "",
        placeholder="Örn: mori_grey veya @mori_grey",
        key="gap_your_channel"
    )
    
    competitor_handles_input = st.text_area(
        "Competitor Channel Handles (one per line, e.g., competitor1, competitor2)",
        value="",
        key="gap_competitors",
        help="Enter competitor channel handles without @ symbol, one per line"
    )
    
    max_videos_gap = st.slider(
        "Max Videos to Analyze per Channel",
        min_value=5,
        max_value=20,
        value=10,
        key="gap_max_videos"
    )
    
    if st.button("🔍 Analyze Gaps", use_container_width=True, key="gap_analyze_button"):
        if not your_channel_handle_gap:
            st.error("Please enter your channel handle")
        elif not competitor_handles_input.strip():
            st.error("Please enter at least one competitor channel handle")
        else:
            with st.spinner("Analyzing gaps... This may take a while..."):
                try:
                    competitor_handles = [h.strip().replace("@", "") for h in competitor_handles_input.split("\n") if h.strip()]
                    
                    gaps = st.session_state.competitor_analyzer.analyze_gaps(
                        your_channel_handle_gap,
                        competitor_handles,
                        max_videos_per_channel=max_videos_gap
                    )
                    
                    if gaps.get("error"):
                        st.error(f"Error: {gaps['error']}")
                    else:
                        # Display Opportunities
                        if gaps.get("opportunities"):
                            st.markdown("#### 🎯 Opportunities")
                            opp_cols = st.columns(min(len(gaps["opportunities"]), 3))
                            for idx, opp in enumerate(gaps["opportunities"]):
                                col_idx = idx % 3
                                with opp_cols[col_idx]:
                                    priority_color = "error" if opp.get("priority") == "high" else "warning" if opp.get("priority") == "medium" else "info"
                                    render_card(
                                        title=opp.get("title", "Opportunity"),
                                        content=opp.get("description", ""),
                                        metric=opp.get("priority", "low").upper(),
                                        icon="🎯",
                                        color=priority_color,
                                        subtitle=opp.get("action", "")[:50] + "..." if len(opp.get("action", "")) > 50 else opp.get("action", "")
                                    )
                        
                        # Keyword Gaps
                        if gaps.get("keyword_gaps"):
                            st.markdown("#### 🔑 Missing Keywords")
                            st.info(f"Competitors use {len(gaps['keyword_gaps'])} keywords you don't. Consider adding these:")
                            keyword_cols = st.columns(4)
                            for idx, keyword in enumerate(gaps["keyword_gaps"][:20]):
                                with keyword_cols[idx % 4]:
                                    st.code(keyword, language=None)
                        
                        # Tag Gaps
                        if gaps.get("tag_gaps"):
                            st.markdown("#### 🏷️ Missing Tags")
                            st.info(f"Competitors use {len(gaps['tag_gaps'])} tags you don't. Consider adding these:")
                            tag_cols = st.columns(5)
                            for idx, tag in enumerate(gaps["tag_gaps"][:30]):
                                with tag_cols[idx % 5]:
                                    st.code(tag, language=None)
                        
                        # Content Gaps
                        if gaps.get("content_gaps"):
                            st.markdown("#### 📝 Content Strategy Gaps")
                            for content_gap in gaps["content_gaps"]:
                                st.warning(f"**{content_gap.get('type', 'Gap')}**: {content_gap.get('recommendation', '')}")
                        
                        # Timing Gaps
                        if gaps.get("timing_gaps") and gaps["timing_gaps"].get("competitor_peak_hours"):
                            st.markdown("#### ⏰ Upload Timing Analysis")
                            timing = gaps["timing_gaps"]
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Competitor Peak Hours", ", ".join(map(str, timing.get("competitor_peak_hours", []))))
                            with col2:
                                st.metric("Your Peak Hours", ", ".join(map(str, timing.get("your_peak_hours", []))))
                            if timing.get("recommendation"):
                                st.info(timing["recommendation"])
                        
                        # Description Gaps
                        if gaps.get("description_gaps") and gaps["description_gaps"].get("recommendations"):
                            st.markdown("#### 📄 Description Strategy Gaps")
                            desc_gaps = gaps["description_gaps"]
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Length Gap", f"{int(desc_gaps.get('length_gap', 0))} chars")
                            with col2:
                                st.metric("Word Count Gap", f"{int(desc_gaps.get('word_count_gap', 0))} words")
                            with col3:
                                st.metric("Links Usage Gap", f"{desc_gaps.get('links_usage_gap', 0):.1%}")
                            with col4:
                                st.metric("Hashtag Gap", f"{int(desc_gaps.get('hashtag_gap', 0))}")
                            
                            for rec in desc_gaps.get("recommendations", []):
                                st.info(rec)
                
                except Exception as e:
                    st.error(f"Gap analysis failed: {str(e)}")
                    logger.exception("Gap analysis error")

elif is_page("title_optimizer"):
    st.title(t("pages.title_optimizer.title"))
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    title = st.text_input(t("pages.title_optimizer.enter_title"), value="", placeholder="Örn: Best Techno Mix 2024 | Underground Electronic Music", key="title_optimizer_title")
    song_name = st.text_input(t("pages.title_optimizer.song_name"), value="", placeholder="Örn: Song Name (opsiyonel)", key="title_optimizer_song")
    
    if st.button(t("pages.title_optimizer.generate_button"), use_container_width=True):
        with st.spinner(t("messages.generating")):
            try:
                # Get niche from session state
                niche = st.session_state.get("target_niche", "")
                variations = st.session_state.title_optimizer.generate_title_variations(
                    title, song_name, num_variations=5, niche=niche
                )
                
                st.markdown(f"### {t('pages.title_optimizer.variations')}")
                # Title variations in card grid
                title_cols = st.columns(min(len(variations), 2))
                for idx, var in enumerate(variations):
                    col_idx = idx % 2
                    with title_cols[col_idx]:
                        length_label = t("pages.title_optimizer.length")
                        keywords_label = t("pages.title_optimizer.keywords_found")
                        structure_label = t("pages.title_optimizer.structure")
                        rec_label = t("cards.recommendation")
                        chars_text = "karakter" if current_lang == "tr" else "characters"
                        
                        render_card(
                            title=f"#{idx + 1} - {var['title'][:40]}...",
                            content=f"<b>{length_label}:</b> {var['length']} {chars_text}<br><b>{keywords_label}:</b> {', '.join(var['keywords_found'][:3])}<br><b>{structure_label}:</b> {var['structure']}<br><b>{rec_label}:</b> {var['recommendation']}",
                            metric=f"{t('common.score')}: {var['seo_score']}",
                            icon="✏️",
                            color="success" if var['seo_score'] >= 80 else "warning" if var['seo_score'] >= 60 else "info"
                        )
                        
            except Exception as e:
                st.error(t("messages.error_loading", error=str(e)))

elif is_page("description_generator"):
    st.title(t("pages.description_generator.title"))
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    video_title = st.text_input(t("pages.description_generator.video_title"), value="", placeholder="Örn: Best Techno Mix 2024 | Underground Electronic Music", key="description_generator_title")
    song_name = st.text_input(t("pages.description_generator.song_name"), value="", placeholder="Örn: Song Name (opsiyonel)", key="description_generator_song")
    custom_info = st.text_area(t("pages.description_generator.custom_info"), value="", placeholder="Örn: Bu video hakkında ek bilgiler (opsiyonel)", key="description_generator_custom_info")
    
    if st.button(t("pages.description_generator.generate_button"), use_container_width=True):
        with st.spinner(t("messages.generating")):
            try:
                # Get niche and channel from session state
                niche = st.session_state.get("target_niche", "")
                channel = st.session_state.get("target_channel", "")
                result = st.session_state.description_generator.generate_description(
                    video_title, song_name, custom_info=custom_info, niche=niche, channel_handle=channel
                )
                
                st.markdown(f"### {t('pages.description_generator.generated_description')}")
                st.text_area("", result["description"], height=400)
                
                # Analysis in card format
                st.markdown(f"### {t('common.analysis')}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    render_card(
                        title=t("pages.description_generator.word_count"),
                        content=t("pages.description_generator.word_count"),
                        metric=f"{result['word_count']}",
                        icon="📝",
                        color="info"
                    )
                with col2:
                    render_card(
                        title=t("pages.description_generator.character_count"),
                        content=t("pages.description_generator.character_count"),
                        metric=f"{result['character_count']}",
                        icon="🔤",
                        color="info"
                    )
                with col3:
                    render_card(
                        title=t("pages.description_generator.hashtags"),
                        content=t("pages.description_generator.hashtags"),
                        metric=f"{result['hashtag_count']}",
                        icon="🏷️",
                        color="info"
                    )
                
                # SEO Score in card
                st.markdown(f"### {t('pages.description_generator.seo_score')}")
                seo_score = result['analysis']['seo_score']
                score_color = "success" if seo_score >= 80 else "warning" if seo_score >= 60 else "error"
                render_card(
                    title=t("pages.description_generator.seo_score"),
                    content=t("pages.description_generator.seo_score"),
                    metric=f"{seo_score}/100",
                    icon="📊",
                    color=score_color
                )
                
                st.subheader(t("common.recommendations"))
                for rec in result["analysis"]["recommendations"]:
                    st.info(rec)
                    
            except Exception as e:
                st.error(t("messages.error_loading", error=str(e)))

elif is_page("tag_suggester"):
    st.title(t("pages.tag_suggester.title"))
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    video_title = st.text_input(t("pages.tag_suggester.video_title"), value="", placeholder="Örn: Best Techno Mix 2024 | Underground Electronic Music", key="tag_suggester_title")
    song_name = st.text_input(t("pages.tag_suggester.song_name"), value="", placeholder="Örn: Song Name (opsiyonel)", key="tag_suggester_song")
    
    if st.button(t("pages.tag_suggester.suggest_button"), use_container_width=True):
        with st.spinner(t("messages.generating")):
            try:
                # Get niche from session state
                niche = st.session_state.get("target_niche", "")
                result = st.session_state.tag_suggester.suggest_tags(video_title, song_name, niche=niche)
                
                st.markdown(f"### {t('pages.tag_suggester.suggested_tags')}")
                tags_text = ", ".join(result["suggested_tags"])
                st.text_area(t("pages.tag_suggester.copy_tags"), tags_text, height=100)
                
                # Analysis in card format
                st.markdown(f"### {t('common.analysis')}")
                col1, col2 = st.columns(2)
                with col1:
                    render_card(
                        title=t("pages.tag_suggester.total_tags"),
                        content=t("pages.tag_suggester.total_tags"),
                        metric=f"{result['tag_count']}",
                        icon="🏷️",
                        color="info"
                    )
                with col2:
                    opt_score = result['analysis']['optimization_score']
                    score_color = "success" if opt_score >= 80 else "warning" if opt_score >= 60 else "error"
                    render_card(
                        title=t("pages.tag_suggester.optimization_score"),
                        content=t("pages.tag_suggester.optimization_score"),
                        metric=f"{opt_score}/100",
                        icon="📊",
                        color=score_color
                    )
                
                # Best Practices in card format
                st.markdown(f"### {t('pages.tag_suggester.best_practices')}")
                if result.get("best_practices"):
                    practice_cols = st.columns(min(len(result["best_practices"]), 2))
                    for idx, practice in enumerate(result["best_practices"]):
                        col_idx = idx % 2
                        with practice_cols[col_idx]:
                            render_card(
                                title=f"{t('cards.best_practice')} #{idx + 1}",
                                content=practice,
                                icon="✅",
                                color="info"
                            )
                    
            except Exception as e:
                st.error(t("messages.error_loading", error=str(e)))

elif is_page("trend_predictor"):
    st.title(t("pages.trend_predictor.title"))
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    if st.button(t("pages.trend_predictor.predict_button"), use_container_width=True):
        with st.spinner(t("messages.analyzing")):
            try:
                predictions = st.session_state.trend_predictor.predict_trends(
                    niche=st.session_state.target_niche
                )
                
                # Recent Trends in card format
                st.markdown(f"### {t('pages.trend_predictor.recent_trends')}")
                recent_trends = predictions.get("recent_trends", {})
                if recent_trends:
                    # Get trending keywords
                    trending_keywords = recent_trends.get("trending_keywords", [])
                    if trending_keywords:
                        st.markdown(f"#### {t('pages.trend_predictor.trending_keywords')}")
                        keyword_cols = st.columns(min(len(trending_keywords[:6]), 3))
                        for idx, keyword_data in enumerate(trending_keywords[:6]):
                            col_idx = idx % 3
                            with keyword_cols[col_idx]:
                                count_text = "Tekrar" if current_lang == "tr" else "mentions"
                                render_card(
                                    title=keyword_data.get("word", t("common.count")),
                                    content=f"{t('common.count')}: {keyword_data.get('count', 0)} {count_text}",
                                    metric=f"{keyword_data.get('count', 0)}",
                                    icon="📈",
                                    color="info"
                                )
                    
                    # Get trending themes
                    trending_themes = recent_trends.get("trending_themes", [])
                    if trending_themes:
                        st.markdown(f"#### {t('pages.trend_predictor.trending_themes')}")
                        theme_cols = st.columns(min(len(trending_themes[:6]), 3))
                        for idx, theme_data in enumerate(trending_themes[:6]):
                            col_idx = idx % 3
                            with theme_cols[col_idx]:
                                count_text = "Tekrar" if current_lang == "tr" else "mentions"
                                render_card(
                                    title=theme_data.get("theme", t("common.count")),
                                    content=f"{t('common.count')}: {theme_data.get('count', 0)} {count_text}",
                                    metric=f"{theme_data.get('count', 0)}",
                                    icon="🎨",
                                    color="success"
                                )
                
                # Predictions in card format
                st.markdown(f"### {t('pages.trend_predictor.predictions')}")
                future_predictions = predictions.get("predictions", [])
                if future_predictions:
                    pred_cols = st.columns(min(len(future_predictions[:4]), 2))
                    for idx, pred in enumerate(future_predictions[:4]):
                        col_idx = idx % 2
                        with pred_cols[col_idx]:
                            # Handle both keyword and theme predictions
                            pred_title = pred.get("keyword") or pred.get("theme", t("common.analysis"))
                            trend_dir = pred.get("trend_direction", "Unknown")
                            confidence = pred.get("confidence", "Unknown")
                            action = pred.get("recommended_action", "N/A")
                            
                            trend_label = t("pages.trend_predictor.trend")
                            conf_label = t("pages.trend_predictor.confidence")
                            action_label = t("pages.trend_predictor.action")
                            
                            render_card(
                                title=pred_title,
                                content=f"<b>{trend_label}:</b> {trend_dir}<br><b>{conf_label}:</b> {confidence}<br><b>{action_label}:</b> {action}",
                                icon="🔮",
                                color="info"
                            )
                
                # Recommendations in card format
                st.markdown(f"### {t('common.recommendations')}")
                if predictions.get("recommendations"):
                    rec_cols = st.columns(min(len(predictions["recommendations"]), 2))
                    for idx, rec in enumerate(predictions["recommendations"]):
                        col_idx = idx % 2
                        with rec_cols[col_idx]:
                            render_card(
                                title=f"{t('cards.recommendation')} #{idx + 1}",
                                content=rec,
                                icon="💡",
                                color="info"
                            )
                
                # Best Posting Times in card format
                st.markdown(f"### {t('pages.trend_predictor.best_posting_times')}")
                posting_times = st.session_state.trend_predictor.get_best_posting_times(st.session_state.target_channel)
                if posting_times:
                    best_times_dict = posting_times.get("best_times", {})
                    timezone = posting_times.get("timezone", "UTC+3")
                    
                    # Convert dictionary to list of day-time pairs
                    day_time_list = []
                    for day, times in best_times_dict.items():
                        for time in times:
                            day_time_list.append({
                                "day": day.capitalize(),
                                "time": time,
                                "score": 1.0  # All times are equally good in this implementation
                            })
                    
                    if day_time_list:
                        timezone_label = t("pages.trend_predictor.timezone")
                        st.markdown(f"**{timezone_label}:** {timezone}")
                        time_cols = st.columns(min(len(day_time_list[:12]), 3))
                        for idx, time_data in enumerate(day_time_list[:12]):
                            col_idx = idx % 3
                            with time_cols[col_idx]:
                                time_label = "Saat" if current_lang == "tr" else "Time"
                                render_card(
                                    title=time_data.get("day", "Day"),
                                    content=f"{time_label}: {time_data.get('time', 'N/A')}",
                                    icon="⏰",
                                    color="success"
                                )
                    
                    # Show recommendations
                    recommendations = posting_times.get("recommendations", [])
                    if recommendations:
                        st.markdown(f"#### {t('pages.trend_predictor.recommendations')}")
                        for rec in recommendations:
                            st.info(f"💡 {rec}")
                    
                    # Show next optimal post time
                    next_optimal = posting_times.get("next_optimal_post", {})
                    if next_optimal:
                        st.markdown(f"#### {t('pages.trend_predictor.next_optimal_post')}")
                        reason_label = "Sebep" if current_lang == "tr" else "Reason"
                        time_label = "Saat" if current_lang == "tr" else "Time"
                        render_card(
                            title=next_optimal.get("day", "Day"),
                            content=f"{time_label}: {next_optimal.get('time', 'N/A')}<br>{reason_label}: {next_optimal.get('reason', 'N/A')}",
                            icon="🎯",
                            color="warning"
                        )
                    
            except Exception as e:
                st.error(t("messages.error_loading", error=str(e)))

elif is_page("proactive_advisor"):
    st.title(t("pages.proactive_advisor.title"))
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    if st.button(t("pages.proactive_advisor.get_suggestions_button"), use_container_width=True):
        with st.spinner(t("messages.analyzing")):
            try:
                suggestions = st.session_state.proactive_advisor.get_proactive_suggestions(st.session_state.target_channel)
                
                # Alerts in card format
                st.markdown(f"### {t('common.alerts')}")
                if suggestions.get("alerts"):
                    alert_cols = st.columns(min(len(suggestions["alerts"]), 3))
                    for idx, alert in enumerate(suggestions["alerts"]):
                        col_idx = idx % 3
                        with alert_cols[col_idx]:
                            alert_type = alert.get("type", "info")
                            color_map = {
                                "warning": "warning",
                                "error": "error",
                                "info": "info"
                            }
                            render_card(
                                title=alert.get("title", t("cards.alert")),
                                content=alert.get("message", ""),
                                icon="⚠️" if alert_type == "warning" else "❌" if alert_type == "error" else "ℹ️",
                                color=color_map.get(alert_type, "info")
                            )
                
                # Suggestions in card format
                st.markdown(f"### {t('common.suggestions')}")
                if suggestions.get("suggestions"):
                    suggestion_cols = st.columns(min(len(suggestions["suggestions"]), 3))
                    for idx, suggestion in enumerate(suggestions["suggestions"]):
                        col_idx = idx % 3
                        with suggestion_cols[col_idx]:
                            render_card(
                                title=suggestion.get("title", t("cards.suggestion")),
                                content=suggestion.get("message", ""),
                                icon="✅",
                                color="success"
                            )
                
                # Content Ideas in card format
                st.markdown(f"### {t('pages.proactive_advisor.content_ideas')}")
                if suggestions.get("content_ideas"):
                    idea_cols = st.columns(min(len(suggestions["content_ideas"]), 2))
                    for idx, idea in enumerate(suggestions["content_ideas"]):
                        col_idx = idx % 2
                        with idea_cols[col_idx]:
                            reason_label = t("pages.proactive_advisor.reason")
                            difficulty_label = t("pages.proactive_advisor.difficulty")
                            render_card(
                                title=idea.get("idea", t("cards.content_idea")),
                                content=f"<b>{reason_label}:</b> {idea.get('reason', 'N/A')}<br><b>{difficulty_label}:</b> {idea.get('difficulty', 'N/A')}",
                                icon="💡",
                                color="info"
                            )
                
                # Priority Actions in card format
                st.markdown(f"### {t('pages.proactive_advisor.priority_actions')}")
                if suggestions.get("priority_actions"):
                    action_cols = st.columns(min(len(suggestions["priority_actions"]), 2))
                    for idx, action in enumerate(suggestions["priority_actions"]):
                        col_idx = idx % 2
                        with action_cols[col_idx]:
                            render_card(
                                title=f"{t('pages.proactive_advisor.priority_actions')} #{idx + 1}",
                                content=action,
                                icon="🎯",
                                color="warning"
                            )
                    
            except Exception as e:
                st.error(t("messages.error_loading", error=str(e)))

elif is_page("performance_tracking"):
    st.title("📊 Performance Tracking & Self-Improvement")
    st.markdown("Track recommendation performance and learn from successes/failures")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📸 Take Snapshot", use_container_width=True):
            with st.spinner("Taking performance snapshot..."):
                try:
                    snapshot = st.session_state.performance_tracker.track_snapshot(st.session_state.target_channel)
                    if "error" not in snapshot:
                        st.success("✅ Snapshot recorded!")
                        st.json(snapshot)
                    else:
                        st.error(f"Error: {snapshot.get('error')}")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        if st.button("📈 Analyze Growth Trend", use_container_width=True):
            with st.spinner("Analyzing growth trend..."):
                try:
                    trend = st.session_state.performance_tracker.analyze_growth_trend(st.session_state.target_channel, days=30)
                    st.subheader("Growth Trend Analysis (30 days)")
                    st.json(trend)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    if st.button("🧠 Learn from Recommendations", use_container_width=True):
        with st.spinner("Analyzing learned patterns..."):
            try:
                learned = st.session_state.performance_tracker.learn_from_recommendations()
                st.subheader("Learned Patterns")
                st.json(learned)
            except Exception as e:
                st.error(f"Error: {e}")
    
    if st.button("📋 Get Performance Summary", use_container_width=True):
        with st.spinner("Generating performance summary..."):
            try:
                summary = st.session_state.performance_tracker.get_performance_summary(st.session_state.target_channel)
                
                # Current Metrics in card grid
                st.markdown("### Current Metrics")
                metrics = summary.get("current_metrics", {})
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    render_card(
                        title="Subscribers",
                        content="Total channel subscribers",
                        metric=f"{metrics.get('subscribers', 0):,}",
                        icon="👥",
                        color="info"
                    )
                with col2:
                    render_card(
                        title="Total Views",
                        content="All-time video views",
                        metric=f"{metrics.get('total_views', 0):,}",
                        icon="👁️",
                        color="info"
                    )
                with col3:
                    render_card(
                        title="Videos",
                        content="Total published videos",
                        metric=f"{metrics.get('total_videos', 0)}",
                        icon="📹",
                        color="info"
                    )
                with col4:
                    render_card(
                        title="Avg Views/Video",
                        content="Average views per video",
                        metric=f"{metrics.get('average_views_per_video', 0):,.0f}",
                        icon="📊",
                        color="info"
                    )
                
                # Growth Trend in card format
                st.markdown("### Growth Trend")
                growth = summary.get("growth_trend", {})
                if growth.get("status") != "insufficient_data":
                    growth_data = growth.get("growth", {})
                    sub_growth = growth_data.get("subscribers", {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        render_card(
                            title="Subscriber Growth",
                            content="Growth over analysis period",
                            metric=f"{sub_growth.get('change', 0):,}",
                            icon="📈",
                            color="success"
                        )
                    with col2:
                        render_card(
                            title="Daily Average Growth",
                            content="Average daily subscriber growth",
                            metric=f"{sub_growth.get('daily_average', 0):.2f}",
                            icon="📅",
                            color="info"
                        )
                    with col3:
                        render_card(
                            title="Growth Rate",
                            content="Percentage growth rate",
                            metric=f"{sub_growth.get('growth_rate_percent', 0):.2f}%",
                            icon="📊",
                            color="info"
                        )
                    
                    projection = growth.get("projection", {})
                    if projection.get("days_to_1m"):
                        st.markdown("### Projection to 1M Subscribers")
                        render_card(
                            title="Days to 1M",
                            content=f"Projected date: {datetime.fromisoformat(projection['projected_date']).strftime('%Y-%m-%d')}" if projection.get("projected_date") else "Based on current growth rate",
                            metric=f"{projection.get('days_to_1m', 0):,.0f}",
                            icon="🎯",
                            color="warning"
                        )
                else:
                    render_card(
                        title="Insufficient Data",
                        content="Need more snapshots to analyze growth trend. Take snapshots regularly!",
                        icon="ℹ️",
                        color="warning"
                    )
                
                # Recommendations in card format
                st.markdown("### Recommendations")
                if summary.get("recommendations"):
                    rec_cols = st.columns(min(len(summary["recommendations"]), 2))
                    for idx, rec in enumerate(summary["recommendations"]):
                        col_idx = idx % 2
                        with rec_cols[col_idx]:
                            render_card(
                                title=f"Recommendation #{idx + 1}",
                                content=rec,
                                icon="💡",
                                color="info"
                            )
                    
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Performance Forecasting Section
    st.markdown("---")
    st.markdown("### 📈 Performance Forecasting")
    st.markdown("Forecast future performance based on historical data and analyze different strategy scenarios.")
    
    forecast_days = st.selectbox(
        "Forecast Period",
        options=[7, 30, 90, 180, 365],
        index=1,  # Default to 30 days
        key="forecast_days"
    )
    
    forecast_scenarios = st.multiselect(
        "Scenarios to Analyze",
        options=["realistic", "optimistic", "pessimistic"],
        default=["realistic", "optimistic"],
        key="forecast_scenarios"
    )
    
    if st.button("🔮 Generate Forecast", use_container_width=True, key="forecast_button"):
        with st.spinner("Generating forecast... This may take a moment..."):
            try:
                forecast = st.session_state.performance_tracker.forecast_performance(
                    st.session_state.target_channel,
                    days_ahead=forecast_days,
                    scenarios=forecast_scenarios if forecast_scenarios else None
                )
                
                if forecast.get("error"):
                    st.error(f"Error: {forecast.get('error')} - {forecast.get('message', '')}")
                else:
                    # Current Metrics
                    st.markdown("#### Current Metrics")
                    current = forecast.get("current_metrics", {})
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Subscribers", f"{current.get('subscribers', 0):,}")
                    with col2:
                        st.metric("Total Views", f"{current.get('total_views', 0):,}")
                    with col3:
                        st.metric("Videos", current.get('total_videos', 0))
                    with col4:
                        st.metric("Avg Views/Video", f"{current.get('average_views_per_video', 0):,.0f}")
                    
                    # Forecast Scenarios
                    st.markdown("#### Forecast Scenarios")
                    scenarios = forecast.get("scenarios", {})
                    
                    for scenario_name, scenario_data in scenarios.items():
                        st.markdown(f"##### {scenario_name.title()} Scenario")
                        scenario_cols = st.columns(4)
                        
                        subs_data = scenario_data.get("subscribers", {})
                        views_data = scenario_data.get("views", {})
                        videos_data = scenario_data.get("videos", {})
                        milestone_data = scenario_data.get("milestone", {})
                        
                        with scenario_cols[0]:
                            render_card(
                                title="Projected Subscribers",
                                content=f"Change: +{subs_data.get('change', 0):,}",
                                metric=f"{subs_data.get('projected', 0):,}",
                                icon="👥",
                                color="success" if subs_data.get('change', 0) > 0 else "info"
                            )
                        with scenario_cols[1]:
                            render_card(
                                title="Projected Views",
                                content=f"Change: +{views_data.get('change', 0):,}",
                                metric=f"{views_data.get('projected', 0):,}",
                                icon="👁️",
                                color="success" if views_data.get('change', 0) > 0 else "info"
                            )
                        with scenario_cols[2]:
                            render_card(
                                title="New Videos",
                                content=f"Total: {videos_data.get('projected', 0)}",
                                metric=f"+{videos_data.get('new_videos', 0)}",
                                icon="📹",
                                color="info"
                            )
                        with scenario_cols[3]:
                            days_to_1m = milestone_data.get("days_to_1m")
                            if days_to_1m:
                                render_card(
                                    title="Days to 1M",
                                    content=f"Date: {datetime.fromisoformat(milestone_data['projected_1m_date']).strftime('%Y-%m-%d')}" if milestone_data.get("projected_1m_date") else "",
                                    metric=f"{days_to_1m:,.0f}",
                                    icon="🎯",
                                    color="warning"
                                )
                            else:
                                render_card(
                                    title="Days to 1M",
                                    content="Insufficient growth rate",
                                    metric="N/A",
                                    icon="🎯",
                                    color="error"
                                )
                    
                    # Confidence
                    confidence = forecast.get("confidence", {})
                    if confidence:
                        st.markdown("#### Forecast Confidence")
                        conf_level = confidence.get("level", "unknown")
                        conf_score = confidence.get("score", 0)
                        conf_color = "success" if conf_level == "high" else "warning" if conf_level == "medium" else "error"
                        render_card(
                            title="Confidence Level",
                            content=f"Based on {confidence.get('snapshot_count', 0)} snapshots",
                            metric=f"{conf_level.upper()} ({conf_score}%)",
                            icon="📊",
                            color=conf_color
                        )
                    
                    # Recommendations
                    recommendations = forecast.get("recommendations", [])
                    if recommendations:
                        st.markdown("#### Forecast Recommendations")
                        for rec in recommendations:
                            st.info(rec)
            
            except Exception as e:
                st.error(f"Forecast error: {e}")
    
    # Scenario Impact Analysis
    st.markdown("---")
    st.markdown("### 🎯 Strategy Impact Analysis")
    st.markdown("Analyze the impact of different strategy changes on future performance.")
    
    col1, col2 = st.columns(2)
    with col1:
        upload_freq = st.number_input(
            "Upload Frequency (videos/week)",
            min_value=0.0,
            max_value=10.0,
            value=1.0,
            step=0.5,
            key="strategy_upload_freq"
        )
        ctr_improvement = st.slider(
            "CTR Improvement (%)",
            min_value=0,
            max_value=50,
            value=10,
            key="strategy_ctr"
        ) / 100.0
    with col2:
        engagement_improvement = st.slider(
            "Engagement Improvement (%)",
            min_value=0,
            max_value=50,
            value=10,
            key="strategy_engagement"
        ) / 100.0
        seo_optimization = st.slider(
            "SEO Optimization Impact (%)",
            min_value=0,
            max_value=50,
            value=10,
            key="strategy_seo"
        ) / 100.0
    
    strategy_changes = {}
    if upload_freq > 0:
        strategy_changes["upload_frequency"] = upload_freq
    if ctr_improvement > 0:
        strategy_changes["ctr_improvement"] = ctr_improvement
    if engagement_improvement > 0:
        strategy_changes["engagement_improvement"] = engagement_improvement
    if seo_optimization > 0:
        strategy_changes["seo_optimization"] = seo_optimization
    
    scenario_days = st.selectbox(
        "Analysis Period (days)",
        options=[7, 30, 90, 180],
        index=1,
        key="scenario_days"
    )
    
    if st.button("📊 Analyze Strategy Impact", use_container_width=True, key="scenario_button"):
        if not strategy_changes:
            st.warning("Please select at least one strategy change to analyze.")
        else:
            with st.spinner("Analyzing strategy impact..."):
                try:
                    impact = st.session_state.performance_tracker.analyze_scenario_impact(
                        st.session_state.target_channel,
                        strategy_changes,
                        days_ahead=scenario_days
                    )
                    
                    if impact.get("error"):
                        st.error(f"Error: {impact.get('error')}")
                    else:
                        # Strategy Changes Summary
                        st.markdown("#### Strategy Changes")
                        changes = impact.get("strategy_changes", {})
                        changes_text = []
                        if "upload_frequency" in changes:
                            changes_text.append(f"Upload Frequency: {changes['upload_frequency']} videos/week")
                        if "ctr_improvement" in changes:
                            changes_text.append(f"CTR Improvement: {changes['ctr_improvement']*100:.0f}%")
                        if "engagement_improvement" in changes:
                            changes_text.append(f"Engagement Improvement: {changes['engagement_improvement']*100:.0f}%")
                        if "seo_optimization" in changes:
                            changes_text.append(f"SEO Optimization: {changes['seo_optimization']*100:.0f}%")
                        st.info(" | ".join(changes_text))
                        
                        # Impact Comparison
                        st.markdown("#### Impact Comparison")
                        impact_data = impact.get("impact", {})
                        
                        subs_impact = impact_data.get("subscribers", {})
                        views_impact = impact_data.get("views", {})
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Subscribers Impact**")
                            render_card(
                                title="Baseline",
                                content="Without strategy changes",
                                metric=f"{subs_impact.get('baseline', 0):,}",
                                icon="📊",
                                color="info"
                            )
                            render_card(
                                title="With Strategy",
                                content=f"Change: {subs_impact.get('change_percent', 0):+.1f}%",
                                metric=f"{subs_impact.get('modified', 0):,}",
                                icon="📈",
                                color="success" if subs_impact.get('change', 0) > 0 else "error"
                            )
                        with col2:
                            st.markdown("**Views Impact**")
                            render_card(
                                title="Baseline",
                                content="Without strategy changes",
                                metric=f"{views_impact.get('baseline', 0):,}",
                                icon="📊",
                                color="info"
                            )
                            render_card(
                                title="With Strategy",
                                content=f"Change: {views_impact.get('change_percent', 0):+.1f}%",
                                metric=f"{views_impact.get('modified', 0):,}",
                                icon="📈",
                                color="success" if views_impact.get('change', 0) > 0 else "error"
                            )
                        
                        # Recommendations
                        recommendations = impact.get("recommendations", [])
                        if recommendations:
                            st.markdown("#### Strategy Recommendations")
                            for rec in recommendations:
                                st.info(rec)
                
                except Exception as e:
                    st.error(f"Strategy analysis error: {e}")

elif is_page("milestone_tracker"):
    st.title(t("pages.milestone_tracker.title"))
    st.markdown("Track your progress toward 1 million subscribers!")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    if st.button("🔄 Update Status", use_container_width=True):
        with st.spinner("Checking milestone status..."):
            try:
                status = st.session_state.milestone_tracker.get_current_status(st.session_state.target_channel)
                
                if "error" in status:
                    st.error(f"Error: {status.get('error')}")
                else:
                    # Current Status in card format
                    st.markdown("### Current Status")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        render_card(
                            title="Current Subscribers",
                            content=f"Target: 1,000,000 subscribers",
                            metric=f"{status['current_subscribers']:,}",
                            icon="👥",
                            color="info",
                            subtitle=f"+{status['current_subscribers'] - 11:,}" if status['current_subscribers'] > 11 else ""
                        )
                    with col2:
                        render_card(
                            title="Overall Progress",
                            content="Progress toward 1M subscribers",
                            metric=f"{status['overall_progress_percent']:.3f}%",
                            icon="📊",
                            color="info"
                        )
                    with col3:
                        next_milestone = status.get("next_milestone")
                        if next_milestone:
                            render_card(
                                title="Next Milestone",
                                content=f"{status['progress_to_next']['subscribers_needed']:,} subscribers needed",
                                metric=next_milestone["name"],
                                icon="🎯",
                                color="warning"
                            )
                    
                    # Progress Bar in card
                    st.markdown("### Progress to Next Milestone")
                    progress = status.get("progress_to_next", {})
                    render_card(
                        title="Progress",
                        content=f"{progress.get('subscribers_needed', 0):,} subscribers needed to reach next milestone",
                        metric=f"{progress.get('percent', 0):.1f}%",
                        icon="📈",
                        color="info"
                    )
                    st.progress(progress.get("percent", 0) / 100)
                    
                    # Motivation in card
                    render_card(
                        title="Motivation",
                        content=status.get('motivation', 'Keep going!'),
                        icon="💪",
                        color="success"
                    )
                    
                    # Time Estimates in card grid
                    st.markdown("### ⏱️ Time Estimates to Next Milestone")
                    estimates = status.get("time_estimates", {})
                    estimate_cols = st.columns(min(len([e for e in estimates.values() if e.get("days_needed")]), 3))
                    estimate_idx = 0
                    for scenario, data in estimates.items():
                        if data.get("days_needed"):
                            col_idx = estimate_idx % 3
                            with estimate_cols[col_idx]:
                                days = data["days_needed"]
                                render_card(
                                    title=scenario.title(),
                                    content=f"{data['daily_growth']} subs/day<br>Estimated: {days:,.0f} days",
                                    metric=f"{days:,.0f} days",
                                    icon="⏱️",
                                    color="info"
                                )
                            estimate_idx += 1
                    
                    # Strategy
                    st.subheader("🎯 Milestone Strategy")
                    strategy = status.get("strategy", {})
                    st.write(f"**Focus:** {strategy.get('focus', 'N/A')}")
                    
                    st.write("**Key Actions:**")
                    for action in strategy.get("key_actions", []):
                        st.write(f"• {action}")
                    
                    with st.expander("📝 Content Tips"):
                        for tip in strategy.get("content_tips", []):
                            st.write(f"• {tip}")
                    
                    with st.expander("🚀 Growth Hacks"):
                        for hack in strategy.get("growth_hacks", []):
                            st.write(f"• {hack}")
                    
                    # Achieved Milestones
                    achieved = status.get("achieved_milestones", [])
                    if achieved:
                        st.subheader("🏆 Achieved Milestones")
                        for milestone in achieved:
                            st.success(f"✅ {milestone['name']} - Level: {milestone['level']}")
                    
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Milestone History
    if st.button("📜 View Milestone History", use_container_width=True):
        with st.spinner("Loading milestone history..."):
            try:
                history = st.session_state.milestone_tracker.get_milestone_history()
                st.subheader("Milestone History")
                st.json(history)
            except Exception as e:
                st.error(f"Error: {e}")

elif is_page("feedback_learning"):
    st.title(t("pages.feedback_learning.title"))
    st.markdown("Learn from user feedback and recommendation performance")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Record Feedback", "Analyze Patterns", "Growth Patterns", "Improvements"])
    
    with tab1:
        st.subheader("Record Feedback on Recommendation")
        
        recommendation_id = st.text_input("Recommendation ID", placeholder="rec_12345", key="feedback_recommendation_id")
        feedback_type = st.selectbox(
            "Feedback Type",
            ["accepted", "rejected", "modified", "applied"],
            key="feedback_type"
        )
        rating = st.slider("Rating (1-5)", 1, 5, 3, key="feedback_rating")
        notes = st.text_area("Notes (optional)", key="feedback_notes")
        video_id = st.text_input("Video ID (optional)", placeholder="dQw4w9WgXcQ", key="feedback_video_id")
        
        if st.button("Record Feedback", use_container_width=True):
            with st.spinner("Recording feedback..."):
                try:
                    feedback_data = {
                        "rating": rating,
                        "notes": notes
                    }
                    st.session_state.feedback_learner.record_feedback(
                        recommendation_id,
                        feedback_type,
                        feedback_data,
                        video_id if video_id else None
                    )
                    st.success("✅ Feedback recorded!")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        if st.button("Correlate with Performance", use_container_width=True):
            with st.spinner("Analyzing correlation..."):
                try:
                    correlation = st.session_state.feedback_learner.correlate_with_performance(
                        recommendation_id,
                        video_id if video_id else None
                    )
                    st.subheader("Correlation Analysis")
                    st.json(correlation)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab2:
        st.subheader("Analyze Learned Patterns")
        
        if st.button("Analyze All Patterns", use_container_width=True):
            with st.spinner("Analyzing patterns..."):
                try:
                    patterns = st.session_state.feedback_learner.analyze_patterns()
                    
                    st.subheader("Pattern Summary")
                    summary = patterns.get("summary", {})
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Feedback", summary.get("total_feedback", 0))
                    with col2:
                        st.metric("Types Analyzed", summary.get("types_analyzed", 0))
                    with col3:
                        st.metric("Best Type", summary.get("best_performing_type", "N/A"))
                    
                    st.subheader("Performance by Type")
                    by_type = patterns.get("by_type", {})
                    for rec_type, stats in by_type.items():
                        with st.expander(f"📋 {rec_type}"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Acceptance Rate", f"{stats.get('acceptance_rate', 0):.1f}%")
                            with col2:
                                st.metric("Average Rating", f"{stats.get('average_rating', 0):.2f}")
                            with col3:
                                st.metric("Success Score", f"{stats.get('success_score', 0):.2f}")
                    
                    st.subheader("Insights")
                    for insight in patterns.get("insights", []):
                        st.info(insight)
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab3:
        st.subheader("Subscriber Growth Patterns")
        
        if st.button("Analyze Growth Patterns", use_container_width=True):
            with st.spinner("Analyzing growth patterns..."):
                try:
                    growth_patterns = st.session_state.feedback_learner.learn_subscriber_growth_patterns()
                    
                    st.subheader("Growth Pattern Analysis")
                    st.metric("Growth Periods Analyzed", growth_patterns.get("growth_periods_analyzed", 0))
                    st.metric("Patterns Identified", growth_patterns.get("patterns_identified", 0))
                    
                    st.subheader("Best Growth Patterns")
                    best_patterns = growth_patterns.get("best_growth_patterns", [])
                    for pattern in best_patterns:
                        stats = pattern.get("stats", {})
                        with st.expander(f"📈 {pattern.get('type', 'Unknown')}"):
                            st.metric("Times Used", stats.get("times_used", 0))
                            st.metric("Avg Subscriber Growth", f"{stats.get('average_subscriber_growth', 0):.1f}")
                            st.metric("Total Growth", f"{stats.get('total_growth', 0):,}")
                    
                    st.subheader("Insights")
                    for insight in growth_patterns.get("insights", []):
                        st.success(insight)
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab4:
        st.subheader("Get Improvement Suggestions")
        
        recommendation_type = st.selectbox(
            "Recommendation Type",
            ["title", "description", "tags", "thumbnail", "timing"]
        )
        
        if st.button("Get Improvements", use_container_width=True):
            with st.spinner("Generating improvements..."):
                try:
                    improvements = st.session_state.feedback_learner.get_recommendation_improvements(recommendation_type)
                    
                    if improvements.get("status") == "insufficient_data":
                        st.info(improvements.get("message"))
                    else:
                        st.subheader(f"Improvements for {recommendation_type}")
                        
                        current = improvements.get("current_performance", {})
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Success Score", f"{current.get('success_score', 0):.2f}")
                        with col2:
                            st.metric("Acceptance Rate", f"{current.get('acceptance_rate', 0):.1f}%")
                        with col3:
                            st.metric("Average Rating", f"{current.get('average_rating', 0):.2f}")
                        
                        st.subheader("Improvement Suggestions")
                        for improvement in improvements.get("improvements", []):
                            st.warning(improvement)
                        
                        st.subheader("Specific Recommendations")
                        for rec in improvements.get("recommendations", []):
                            st.info(rec)
                        
                        st.subheader("Successful Examples")
                        examples = improvements.get("successful_examples", [])
                        for example in examples[:3]:
                            st.json(example)
                            
                except Exception as e:
                    st.error(f"Error: {e}")

elif is_page("viral_predictor"):
    st.title(t("pages.viral_predictor.title"))
    st.markdown("Predict viral potential before publishing")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    tab1, tab2 = st.tabs(["Predict Viral Potential", "Learn from Viral Content"])
    
    with tab1:
        st.subheader("Analyze Content for Viral Potential")
        
        title = st.text_input("Video Title", value="", placeholder="Örn: Best Techno Mix 2024 | Underground Electronic Music", key="viral_predictor_title")
        description = st.text_area("Video Description", value="", placeholder="Örn: Video açıklamasını buraya girin...", height=150, key="viral_predictor_description")
        tags_input = st.text_input("Tags (comma-separated)", value="", placeholder="Örn: techno, electronic, underground, minimal", key="viral_predictor_tags")
        song_name = st.text_input("Song Name (optional)", value="", placeholder="Örn: Song Name (opsiyonel)", key="viral_predictor_song")
        niche = st.text_input("Niche", value=st.session_state.target_niche if st.session_state.target_niche else "", placeholder="Örn: Techno Music, Psychedelic Rock", key="viral_predictor_niche")
        
        if st.button("Predict Viral Potential", use_container_width=True):
            with st.spinner("Analyzing viral potential..."):
                try:
                    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
                    prediction = st.session_state.viral_predictor.predict_viral_potential(
                        title, description, tags, song_name, niche
                    )
                    
                    # Viral Score
                    viral_score = prediction.get("viral_score", 0)
                    potential_level = prediction.get("potential_level", "unknown")
                    
                    # Viral Score in card
                    st.markdown("### Viral Potential Score")
                    score_color = "success" if viral_score >= 0.7 else "warning" if viral_score >= 0.5 else "error"
                    render_card(
                        title="Viral Score",
                        content=f"Potential Level: {potential_level.replace('_', ' ').title()}",
                        metric=f"{viral_score:.2f}",
                        icon="🔥",
                        color=score_color
                    )
                    st.progress(viral_score)
                    
                    # Indicators in card grid
                    st.markdown("### Viral Indicators Breakdown")
                    indicators = prediction.get("indicators", {})
                    indicator_cols = st.columns(min(len(indicators), 3))
                    for idx, (indicator, score) in enumerate(indicators.items()):
                        col_idx = idx % 3
                        with indicator_cols[col_idx]:
                            render_card(
                                title=indicator.replace('_', ' ').title(),
                                content=f"Indicator strength",
                                metric=f"{score:.2f}",
                                icon="📊",
                                color="info"
                            )
                            st.progress(score)
                    
                    # Recommendation in card
                    st.markdown("### Recommendation")
                    render_card(
                        title="Recommendation",
                        content=prediction.get("recommendation", ""),
                        icon="💡",
                        color="info"
                    )
                    
                    # Improvements in card grid
                    improvements = prediction.get("improvements", [])
                    if improvements:
                        st.markdown("### Improvement Suggestions")
                        improvement_cols = st.columns(min(len(improvements), 2))
                        for idx, improvement in enumerate(improvements):
                            col_idx = idx % 2
                            with improvement_cols[col_idx]:
                                render_card(
                                    title=f"Suggestion #{idx + 1}",
                                    content=improvement,
                                    icon="⚠️",
                                    color="warning"
                                )
                    
                    # Confidence in card
                    confidence = prediction.get("confidence", 0)
                    render_card(
                        title="Prediction Confidence",
                        content="Confidence level of this prediction",
                        metric=f"{confidence:.1%}",
                        icon="🎯",
                        color="success" if confidence >= 0.7 else "warning"
                    )
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab2:
        st.subheader("Learn from Viral Content")
        
        video_id = st.text_input("Viral Video ID", placeholder="dQw4w9WgXcQ", key="viral_learn_video_id")
        
        if st.button("Analyze Viral Video", use_container_width=True):
            with st.spinner("Learning from viral content..."):
                try:
                    learned = st.session_state.viral_predictor.learn_from_viral_content(video_id)
                    
                    if learned.get("status") == "learned":
                        st.success("✅ Patterns learned from viral content!")
                        
                        st.subheader("Learned Patterns")
                        patterns = learned.get("patterns", {})
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Title Length", f"{patterns.get('title_length', 0)} chars")
                            st.metric("Views", f"{patterns.get('views', 0):,}")
                        with col2:
                            st.metric("Description Length", f"{patterns.get('description_length', 0)} chars")
                            st.metric("Likes", f"{patterns.get('likes', 0):,}")
                        with col3:
                            st.metric("Tag Count", patterns.get("tag_count", 0))
                            st.metric("Comments", f"{patterns.get('comments', 0):,}")
                        
                        st.subheader("Insights")
                        for insight in learned.get("insights", []):
                            st.info(insight)
                    else:
                        st.warning(learned.get("message", "Could not learn from this video"))
                        
                except Exception as e:
                    st.error(f"Error: {e}")

elif is_page("competitor_benchmark"):
    st.title(t("pages.competitor_benchmark.title"))
    st.markdown("Learn from 1M+ subscriber channels")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    tab1, tab2, tab3 = st.tabs(["Benchmark Channel", "Differentiation", "Learned Strategies"])
    
    with tab1:
        st.subheader("Benchmark a Successful Channel")
        
        col1, col2 = st.columns(2)
        with col1:
            channel_handle = st.text_input("Channel Handle", placeholder="@channelname", key="benchmark_channel_handle")
        with col2:
            channel_id = st.text_input("Channel ID (alternative)", placeholder="UC...", key="benchmark_channel_id")
        
        if st.button("Benchmark Channel", use_container_width=True):
            with st.spinner("Benchmarking channel..."):
                try:
                    result = st.session_state.competitor_benchmark.benchmark_channel(
                        channel_handle if channel_handle else None,
                        channel_id if channel_id else None
                    )
                    
                    if result.get("error"):
                        st.error(result.get("error"))
                    elif result.get("status") == "below_threshold":
                        st.warning(f"⚠️ {result.get('message')}")
                    elif result.get("status") == "success":
                        st.success("✅ Channel benchmarked successfully!")
                        
                        benchmark = result.get("benchmark", {})
                        
                        st.subheader("Channel Metrics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Subscribers", f"{benchmark.get('subscribers', 0):,}")
                        with col2:
                            st.metric("Total Views", f"{benchmark.get('total_views', 0):,}")
                        with col3:
                            st.metric("Videos", benchmark.get("total_videos", 0))
                        with col4:
                            st.metric("Avg Views/Video", f"{benchmark.get('average_views_per_video', 0):,.0f}")
                        
                        # Content Strategy in card format
                        st.markdown("### Content Strategy")
                        strategy = benchmark.get("content_strategy", {})
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            render_card(
                                title="Avg Title Length",
                                content="Average title length",
                                metric=f"{strategy.get('average_title_length', 0):.0f} chars",
                                icon="✏️",
                                color="info"
                            )
                        with col2:
                            render_card(
                                title="Upload Frequency",
                                content="Days between uploads",
                                metric=f"{strategy.get('upload_frequency_days', 0):.1f} days",
                                icon="📅",
                                color="info"
                            )
                        with col3:
                            render_card(
                                title="Engagement Rate",
                                content="Average engagement rate",
                                metric=f"{strategy.get('engagement_rate', 0):.2f}%",
                                icon="💬",
                                color="info"
                            )
                        
                        # Best Practices in card format
                        st.markdown("### Best Practices")
                        if benchmark.get("best_practices"):
                            practice_cols = st.columns(min(len(benchmark["best_practices"]), 2))
                            for idx, practice in enumerate(benchmark["best_practices"]):
                                col_idx = idx % 2
                                with practice_cols[col_idx]:
                                    render_card(
                                        title=f"Best Practice #{idx + 1}",
                                        content=practice,
                                        icon="✅",
                                        color="success"
                                    )
                        
                        # Insights in card format
                        st.markdown("### Insights")
                        if result.get("insights"):
                            insight_cols = st.columns(min(len(result["insights"]), 2))
                            for idx, insight in enumerate(result["insights"]):
                                col_idx = idx % 2
                                with insight_cols[col_idx]:
                                    render_card(
                                        title=f"Insight #{idx + 1}",
                                        content=insight,
                                        icon="💡",
                                        color="info"
                                    )
                            
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab2:
        st.subheader("Find Differentiation Opportunities")
        
        if st.button("Analyze Opportunities", use_container_width=True):
            with st.spinner("Finding differentiation opportunities..."):
                try:
                    opportunities = st.session_state.competitor_benchmark.find_differentiation_opportunities(
                        st.session_state.target_channel
                    )
                    
                    if opportunities.get("status") == "no_benchmarks":
                        render_card(
                            title="No Benchmarks",
                            content=opportunities.get("message", ""),
                            icon="⚠️",
                            color="warning"
                        )
                    else:
                        st.markdown("### Differentiation Opportunities")
                        render_card(
                            title="Total Opportunities",
                            content="Differentiation opportunities found",
                            metric=f"{opportunities.get('total_opportunities', 0)}",
                            icon="🎯",
                            color="info"
                        )
                        
                        high_priority = opportunities.get("high_priority", [])
                        if high_priority:
                            st.markdown("### 🔴 High Priority")
                            high_pri_cols = st.columns(min(len(high_priority), 2))
                            for idx, opp in enumerate(high_priority):
                                col_idx = idx % 2
                                with high_pri_cols[col_idx]:
                                    render_card(
                                        title=opp.get('type', 'Unknown').replace('_', ' ').title(),
                                        content=f"{opp.get('opportunity', '')}<br><b>Benchmark:</b> {opp.get('benchmark', 'N/A')}",
                                        icon="🔴",
                                        color="error"
                                    )
                        
                        medium_priority = opportunities.get("medium_priority", [])
                        if medium_priority:
                            st.markdown("### 🟡 Medium Priority")
                            med_pri_cols = st.columns(min(len(medium_priority), 2))
                            for idx, opp in enumerate(medium_priority):
                                col_idx = idx % 2
                                with med_pri_cols[col_idx]:
                                    render_card(
                                        title=opp.get('type', 'Unknown').replace('_', ' ').title(),
                                        content=f"{opp.get('opportunity', '')}<br><b>Benchmark:</b> {opp.get('benchmark', 'N/A')}",
                                        icon="🟡",
                                        color="warning"
                                    )
                            
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab3:
        st.subheader("Learned Strategies from All Benchmarks")
        
        if st.button("Get Learned Strategies", use_container_width=True):
            with st.spinner("Analyzing learned strategies..."):
                try:
                    strategies = st.session_state.competitor_benchmark.get_learned_strategies()
                    
                    if strategies.get("status") == "no_data":
                        st.info(strategies.get("message"))
                    else:
                        learned = strategies.get("learned_strategies", {})
                        
                        st.subheader("Aggregated Strategies")
                        st.metric("Channels Analyzed", learned.get("channels_analyzed", 0))
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            avg_title = learned.get("average_title_length")
                            if avg_title:
                                st.metric("Avg Title Length", f"{avg_title:.0f} chars")
                        with col2:
                            avg_freq = learned.get("average_upload_frequency")
                            if avg_freq:
                                st.metric("Avg Upload Frequency", f"{avg_freq:.1f} days")
                        with col3:
                            avg_engagement = learned.get("average_engagement_rate")
                            if avg_engagement:
                                st.metric("Avg Engagement Rate", f"{avg_engagement:.2f}%")
                        
                        # Most Common Themes
                        themes = learned.get("most_common_themes", [])
                        if themes:
                            st.subheader("Most Common Content Themes")
                            st.write(", ".join(themes))
                        
                        # Best Practices
                        practices = learned.get("common_best_practices", [])
                        if practices:
                            st.subheader("Common Best Practices")
                            for practice in practices:
                                st.info(f"✅ {practice}")
                        
                        # Recommendations
                        st.subheader("Recommendations")
                        for rec in strategies.get("recommendations", []):
                            st.success(rec)
                            
                except Exception as e:
                    st.error(f"Error: {e}")

elif is_page("multi_source_data"):
    st.title(t("pages.multi_source_data.title"))
    st.markdown("Integrate data from Google Trends, Reddit, Twitter, and more")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Synthesize Opportunities", 
        "Google Trends", 
        "Reddit Trends", 
        "Twitter Trends",
        "Data Source Status"
    ])
    
    with tab1:
        st.subheader("Synthesize Viral Content Opportunities")
        st.markdown("Combine data from all sources to identify viral opportunities")
        
        keywords_input = st.text_area(
            "Keywords (one per line)",
            value="",
            placeholder="Örn: techno music\nunderground electronic\nminimal techno\nher satıra bir anahtar kelime",
            key="multi_source_keywords"
        )
        niche = st.text_input("Niche", value=st.session_state.target_niche, key="multi_source_niche")
        
        if st.button("Synthesize Opportunities", use_container_width=True):
            with st.spinner("Analyzing multiple data sources..."):
                try:
                    keywords = [k.strip() for k in keywords_input.split("\n") if k.strip()]
                    opportunities = st.session_state.multi_source_integrator.synthesize_opportunities(
                        keywords, niche
                    )
                    
                    st.markdown("### Data Sources Analyzed")
                    sources = opportunities.get("sources_analyzed", [])
                    source_cols = st.columns(min(len(sources), 4))
                    for idx, source in enumerate(sources):
                        col_idx = idx % 4
                        with source_cols[col_idx]:
                            render_card(
                                title=source,
                                content="Data source analyzed",
                                icon="✅",
                                color="success"
                            )
                    
                    # Viral Opportunities in card grid
                    viral_opps = opportunities.get("viral_opportunities", [])
                    if viral_opps:
                        st.subheader(f"🔥 Top {len(viral_opps)} Viral Opportunities")
                        for i, opp in enumerate(viral_opps, 1):
                            with st.expander(f"#{i} - {opp.get('type', 'Unknown').replace('_', ' ').title()} - Potential: {opp.get('viral_potential', 0):.1%}"):
                                st.write(f"**Source:** {opp.get('source', 'N/A')}")
                                st.write(f"**Opportunity:** {opp.get('opportunity', 'N/A')}")
                                if opp.get('title'):
                                    st.write(f"**Title:** {opp.get('title')}")
                                if opp.get('score'):
                                    st.metric("Engagement Score", opp.get('score'))
                                if opp.get('relevance'):
                                    st.metric("Relevance", f"{opp.get('relevance'):.1%}")
                    else:
                        st.info("No viral opportunities identified. Try different keywords or check data sources.")
                    
                    # Trending Topics
                    trending = opportunities.get("trending_topics", [])
                    if trending:
                        st.subheader("📈 Trending Topics")
                        for topic in trending[:5]:
                            st.info(f"**{topic.get('source')}** - {topic.get('title', 'N/A')} (Score: {topic.get('score', 0)})")
                    
                    # Recommendations
                    recommendations = opportunities.get("recommendations", [])
                    if recommendations:
                        st.subheader("💡 Recommendations")
                        for rec in recommendations:
                            st.success(rec)
                            
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab2:
        st.subheader("Google Trends Analysis")
        
        keywords_input = st.text_input("Keywords (comma-separated)", value="", placeholder="Örn: techno music, electronic, underground, minimal", key="google_trends_keywords")
        region = st.selectbox("Region", ["TR", "US", "GB", "DE", "FR"], index=0, key="google_trends_region")
        timeframe = st.selectbox(
            "Timeframe",
            ["today 3-m", "today 12-m", "today 5-y"],
            index=0,
            key="google_trends_timeframe"
        )
        
        if st.button("Get Google Trends", use_container_width=True):
            with st.spinner("Fetching Google Trends data..."):
                try:
                    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
                    trends = st.session_state.multi_source_integrator.get_google_trends(
                        keywords, region, timeframe
                    )
                    
                    if trends.get("error"):
                        st.error(trends.get("error"))
                    else:
                        st.subheader("Trending Keywords")
                        trend_data = trends.get("trends", {})
                        for keyword, data in trend_data.items():
                            with st.expander(f"📊 {keyword}"):
                                st.metric("Interest Score", data.get("interest_score", 0))
                                st.write(f"**Trending:** {data.get('trending', False)}")
                                if data.get("note"):
                                    st.info(data.get("note"))
                                    
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab3:
        st.subheader("Reddit Trends")
        
        subreddits_input = st.text_input(
            "Subreddits (comma-separated)",
            value="",
            placeholder="Örn: techno, electronicmusic, underground, minimaltechno",
            key="reddit_subreddits"
        )
        limit = st.slider("Posts per subreddit", 5, 25, 10, key="reddit_limit")
        
        if st.button("Get Reddit Trends", use_container_width=True):
            with st.spinner("Fetching Reddit trends..."):
                try:
                    subreddits = [s.strip() for s in subreddits_input.split(",") if s.strip()]
                    reddit_data = st.session_state.multi_source_integrator.get_reddit_trends(
                        subreddits, limit
                    )
                    
                    if reddit_data.get("error"):
                        st.warning(reddit_data.get("error"))
                    
                    st.markdown("### Trending Posts")
                    trending_posts = reddit_data.get("trending_posts", {})
                    for subreddit, posts in trending_posts.items():
                        if posts:
                            st.markdown(f"#### r/{subreddit}")
                            post_cols = st.columns(min(len(posts[:5]), 2))
                            for idx, post in enumerate(posts[:5]):
                                col_idx = idx % 2
                                with post_cols[col_idx]:
                                    render_card(
                                        title=post.get('title', 'N/A')[:50] + "..." if len(post.get('title', '')) > 50 else post.get('title', 'N/A'),
                                        content=f"<b>Upvotes:</b> {post.get('score', 0)}<br><b>Comments:</b> {post.get('comments', 0)}<br><b>URL:</b> <a href='{post.get('url', '')}' target='_blank'>View Post</a>",
                                        icon="🔥",
                                        color="info"
                                    )
                        else:
                            render_card(
                                title=f"r/{subreddit}",
                                content="No posts found",
                                icon="ℹ️",
                                color="warning"
                            )
                            
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab4:
        st.subheader("Twitter/X Trends")
        
        keywords_input = st.text_input("Keywords (comma-separated)", value="", placeholder="Örn: techno music, electronic, underground, minimal", key="twitter_trends_keywords")
        region = st.selectbox("Region", ["Turkey", "United States", "Global"], index=0, key="twitter_trends_region")
        
        if st.button("Get Twitter Trends", use_container_width=True):
            with st.spinner("Fetching Twitter trends..."):
                try:
                    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
                    twitter_data = st.session_state.multi_source_integrator.get_twitter_trends(
                        keywords, region
                    )
                    
                    if twitter_data.get("note"):
                        st.info(twitter_data.get("note"))
                    
                    st.subheader("Twitter Trends")
                    trends = twitter_data.get("trends", {})
                    for keyword, data in trends.items():
                        with st.expander(f"🐦 {keyword}"):
                            st.write(f"**Tweet Count:** {data.get('tweet_count', 'N/A')}")
                            st.write(f"**Trending:** {data.get('trending', False)}")
                            if data.get("note"):
                                st.info(data.get("note"))
                                
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab5:
        st.subheader("Data Source Status")
        
        if st.button("Check Data Sources", use_container_width=True):
            with st.spinner("Checking data sources..."):
                try:
                    status = st.session_state.multi_source_integrator.get_data_source_status()
                    
                    st.metric("Active Sources", f"{status.get('active_sources', 0)}/{status.get('total_sources', 0)}")
                    
                    st.subheader("Source Details")
                    sources = status.get("sources", {})
                    for source_name, source_info in sources.items():
                        with st.expander(f"{source_name} - {source_info.get('status', 'unknown').upper()}"):
                            st.write(f"**Status:** {source_info.get('status', 'N/A')}")
                            st.write(f"**Configured:** {source_info.get('configured', False)}")
                            st.write(f"**Note:** {source_info.get('note', 'N/A')}")
                            
                except Exception as e:
                    st.error(f"Error: {e}")

elif is_page("knowledge_graph"):
    st.title(t("pages.knowledge_graph.title"))
    st.markdown("Unified knowledge graph integrating all data sources")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Build Graph",
        "Detect Contradictions",
        "Resolve Contradictions",
        "Growth Patterns",
        "Query Graph"
    ])
    
    with tab1:
        st.subheader("Build Knowledge Graph")
        st.markdown("Integrate all data sources into unified knowledge graph")
        
        if st.button("Build Knowledge Graph", use_container_width=True):
            with st.spinner("Building knowledge graph from all sources..."):
                try:
                    result = st.session_state.knowledge_graph.build_graph(st.session_state.target_channel)
                    
                    st.success("✅ Knowledge graph built successfully!")
                    
                    # Graph stats in card format
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        render_card(
                            title="Nodes",
                            content="Total nodes in graph",
                            metric=f"{result.get('nodes_count', 0)}",
                            icon="🔵",
                            color="info"
                        )
                    with col2:
                        render_card(
                            title="Edges",
                            content="Total connections in graph",
                            metric=f"{result.get('edges_count', 0)}",
                            icon="🔗",
                            color="info"
                        )
                    with col3:
                        render_card(
                            title="Patterns",
                            content="Growth patterns identified",
                            metric=f"{result.get('patterns_count', 0)}",
                            icon="📊",
                            color="info"
                        )
                    
                    # Show graph structure
                    graph = result.get("graph", {})
                    nodes = graph.get("nodes", {})
                    
                    # Node types breakdown
                    node_types = {}
                    for node in nodes.values():
                        node_type = node.get("type", "unknown")
                        node_types[node_type] = node_types.get(node_type, 0) + 1
                    
                    st.subheader("Graph Structure")
                    for node_type, count in node_types.items():
                        st.write(f"**{node_type.title()}:** {count} nodes")
                    
                    # Show patterns
                    patterns = graph.get("patterns", {})
                    if patterns:
                        st.subheader("Extracted Patterns")
                        for pattern_id, pattern_data in patterns.items():
                            with st.expander(f"📊 {pattern_data.get('pattern_type', 'Unknown').replace('_', ' ').title()}"):
                                st.write(f"**Description:** {pattern_data.get('description', 'N/A')}")
                                st.write(f"**Value:** {pattern_data.get('value', 'N/A')}")
                                st.metric("Confidence", f"{pattern_data.get('confidence', 0):.1%}")
                                
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab2:
        st.subheader("Detect Contradictions")
        st.markdown("Find contradictory recommendations and patterns")
        
        if st.button("Detect Contradictions", use_container_width=True):
            with st.spinner("Analyzing for contradictions..."):
                try:
                    contradictions = st.session_state.knowledge_graph.detect_contradictions()
                    
                    # Contradictions count in card
                    contr_count = contradictions.get("contradictions_count", 0)
                    render_card(
                        title="Contradictions Found",
                        content="Total contradictions detected in knowledge graph",
                        metric=f"{contr_count}",
                        icon="⚠️",
                        color="error" if contr_count > 0 else "success"
                    )
                    
                    # Severity breakdown in card grid
                    severity = contradictions.get("severity_breakdown", {})
                    if severity:
                        st.markdown("### Severity Breakdown")
                        sev_cols = st.columns(min(len(severity), 3))
                        for idx, (sev, count) in enumerate(severity.items()):
                            col_idx = idx % 3
                            with sev_cols[col_idx]:
                                render_card(
                                    title=sev.title(),
                                    content="Contradictions of this severity",
                                    metric=f"{count}",
                                    icon="⚠️",
                                    color="error" if sev == "high" else "warning" if sev == "medium" else "info"
                                )
                    
                    # Contradictions list in card grid
                    contr_list = contradictions.get("contradictions", [])
                    if contr_list:
                        st.markdown("### Detected Contradictions")
                        contr_cols = st.columns(min(len(contr_list), 2))
                        for idx, contr in enumerate(contr_list):
                            col_idx = idx % 2
                            with contr_cols[col_idx]:
                                render_card(
                                    title=f"#{idx + 1} - {contr.get('type', 'Unknown').replace('_', ' ').title()}",
                                    content=f"<b>Pattern:</b> {contr.get('pattern', 'N/A')}<br><b>Severity:</b> {contr.get('severity', 'unknown')}<br><b>Recommendation:</b> {contr.get('recommendation', 'N/A')}<br><b>Reality:</b> {contr.get('reality', 'N/A')}",
                                    icon="⚠️",
                                    color="error" if contr.get('severity') == 'high' else "warning"
                                )
                    else:
                        render_card(
                            title="No Contradictions",
                            content="Knowledge graph is consistent!",
                            icon="✅",
                            color="success"
                        )
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab3:
        st.subheader("Resolve Contradictions")
        st.markdown("Resolve detected contradictions using evidence-based approach")
        
        if st.button("Resolve Contradictions", use_container_width=True):
            with st.spinner("Resolving contradictions..."):
                try:
                    resolution = st.session_state.knowledge_graph.resolve_contradictions()
                    
                    resolved_count = resolution.get("resolved_count", 0)
                    if resolved_count > 0:
                        st.success(f"✅ Resolved {resolved_count} contradiction(s)!")
                        
                        st.subheader("Resolutions")
                        resolutions = resolution.get("resolutions", [])
                        for i, res in enumerate(resolutions, 1):
                            with st.expander(f"Resolution #{i}"):
                                contr = res.get("contradiction", {})
                                resol = res.get("resolution", {})
                                
                                st.write(f"**Contradiction:** {contr.get('type', 'Unknown').replace('_', ' ').title()}")
                                st.write(f"**Action:** {resol.get('action', 'N/A').replace('_', ' ').title()}")
                                st.write(f"**Reason:** {resol.get('reason', 'N/A')}")
                                st.info(f"💡 {resol.get('recommendation', 'N/A')}")
                    else:
                        st.info("No contradictions to resolve.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab4:
        st.subheader("Subscriber Growth Patterns")
        st.markdown("Identify patterns that lead to subscriber growth")
        
        if st.button("Analyze Growth Patterns", use_container_width=True):
            with st.spinner("Analyzing growth patterns..."):
                try:
                    patterns = st.session_state.knowledge_graph.get_subscriber_growth_patterns()
                    
                    if patterns.get("status") == "insufficient_data":
                        render_card(
                            title="Insufficient Data",
                            content=patterns.get("message", ""),
                            icon="⚠️",
                            color="warning"
                        )
                    else:
                        pattern_data = patterns.get("patterns", {})
                        
                        # Title Patterns in card format
                        title_patterns = pattern_data.get("title_patterns", {})
                        if title_patterns:
                            st.markdown("### 📝 Title Patterns")
                            col1, col2 = st.columns(2)
                            with col1:
                                render_card(
                                    title="Average Length",
                                    content="Average title length for growth",
                                    metric=f"{title_patterns.get('average_length', 0):.0f} chars",
                                    icon="✏️",
                                    color="info"
                                )
                            with col2:
                                render_card(
                                    title="Optimal Range",
                                    content="Optimal title length range",
                                    metric=title_patterns.get("optimal_range", "N/A"),
                                    icon="📏",
                                    color="info"
                                )
                            if title_patterns.get("common_words"):
                                st.markdown("**Common Words:**")
                                word_cols = st.columns(min(len(title_patterns["common_words"]), 5))
                                for idx, word in enumerate(title_patterns["common_words"][:10]):
                                    col_idx = idx % 5
                                    with word_cols[col_idx]:
                                        render_card(
                                            title=word,
                                            content="",
                                            icon="🔑",
                                            color="info"
                                        )
                        
                        # Timing Patterns in card format
                        timing_patterns = pattern_data.get("timing_patterns", {})
                        if timing_patterns:
                            st.markdown("### ⏰ Timing Patterns")
                            col1, col2 = st.columns(2)
                            with col1:
                                if timing_patterns.get("best_hour") is not None:
                                    render_card(
                                        title="Best Hour",
                                        content="Optimal posting hour",
                                        metric=f"{timing_patterns['best_hour']}:00",
                                        icon="⏰",
                                        color="success"
                                    )
                            with col2:
                                if timing_patterns.get("best_day"):
                                    render_card(
                                        title="Best Day",
                                        content="Optimal posting day",
                                        metric=timing_patterns["best_day"],
                                        icon="📅",
                                        color="success"
                                    )
                        
                        # Content Patterns in card format
                        content_patterns = pattern_data.get("content_patterns", {})
                        if content_patterns:
                            st.markdown("### 📄 Content Patterns")
                            render_card(
                                title="Average Description Length",
                                content="Optimal description length",
                                metric=f"{content_patterns.get('average_description_length', 0):.0f} chars",
                                icon="📝",
                                color="info"
                            )
                            if content_patterns.get("common_tags"):
                                st.markdown("**Common Tags:**")
                                tag_cols = st.columns(min(len(content_patterns["common_tags"][:10]), 5))
                                for idx, tag in enumerate(content_patterns["common_tags"][:10]):
                                    col_idx = idx % 5
                                    with tag_cols[col_idx]:
                                        render_card(
                                            title=tag,
                                            content="",
                                            icon="🏷️",
                                            color="info"
                                        )
                        
                        # Recommendation Patterns
                        rec_patterns = pattern_data.get("recommendation_patterns", {})
                        if rec_patterns:
                            st.subheader("✅ Recommendation Patterns")
                            best_type = rec_patterns.get("best_performing_type")
                            if best_type:
                                st.metric("Best Performing Type", best_type)
                            
                            by_type = rec_patterns.get("by_type", {})
                            if by_type:
                                st.write("**Success Rates by Type:**")
                                for rec_type, stats in by_type.items():
                                    st.metric(
                                        rec_type.title(),
                                        f"{stats.get('success_rate', 0):.1f}%",
                                        f"{stats.get('success', 0)}/{stats.get('total', 0)}"
                                    )
                        
                        # Insights
                        insights = patterns.get("insights", [])
                        if insights:
                            st.subheader("💡 Key Insights")
                            for insight in insights:
                                st.success(insight)
                                
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab5:
        st.subheader("Query Knowledge Graph")
        st.markdown("Query the knowledge graph for specific information")
        
        query_type = st.selectbox(
            "Query Type",
            ["videos", "recommendations", "patterns", "contradictions"]
        )
        
        filters = {}
        if query_type == "videos":
            min_views = st.number_input("Minimum Views", min_value=0, value=0)
            if min_views > 0:
                filters["min_views"] = min_views
        
        if query_type == "recommendations":
            status_filter = st.selectbox(
                "Status Filter",
                ["all", "pending", "applied", "success", "failure", "rejected"]
            )
            if status_filter != "all":
                filters["status"] = status_filter
        
        if st.button("Execute Query", use_container_width=True):
            with st.spinner("Querying knowledge graph..."):
                try:
                    results = st.session_state.knowledge_graph.query_graph(query_type, filters if filters else None)
                    
                    if results.get("error"):
                        st.error(results.get("error"))
                    else:
                        st.metric("Results Found", results.get("count", 0))
                        
                        result_list = results.get("results", [])
                        if result_list:
                            st.subheader("Query Results")
                            # Show first 10 results
                            for i, result in enumerate(result_list[:10], 1):
                                with st.expander(f"Result #{i}"):
                                    st.json(result)
                        else:
                            st.info("No results found.")
                            
                except Exception as e:
                    st.error(f"Error: {e}")

elif is_page("continuous_learning"):
    st.title(t("pages.continuous_learning.title"))
    st.markdown("Automated learning system that runs continuously")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Learning Status",
        "Daily Report",
        "Weekly Report",
        "Learning History"
    ])
    
    with tab1:
        st.subheader("Learning Loop Status")
        
        # Check process status
        process_status = st.session_state.process_manager.get_status()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not process_status.get("running"):
                if st.button("▶️ Start Learning Loop", use_container_width=True):
                    with st.spinner("Starting continuous learning process..."):
                        try:
                            result = st.session_state.process_manager.start_process(st.session_state.target_channel)
                            if result.get("status") == "started":
                                st.success("✅ Learning process started!")
                                st.info(f"Process ID: {result.get('pid')}")
                                st.info("💡 The learning loop will continue running even if you close this page!")
                                st.rerun()
                            else:
                                st.warning(result.get("message"))
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                st.info("🟢 Learning process is running")
        
        with col2:
            if process_status.get("running"):
                if st.button("⏹️ Stop Learning Loop", use_container_width=True):
                    with st.spinner("Stopping learning process..."):
                        try:
                            result = st.session_state.process_manager.stop_process()
                            if result.get("status") == "stopped":
                                st.success("✅ Learning process stopped!")
                                st.rerun()
                            else:
                                st.warning(result.get("message"))
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                st.info("⚪ Learning process is stopped")
        
        # Auto-refresh status
        st.markdown("---")
        st.subheader("Current Status")
        
        # Process status
        col1, col2, col3 = st.columns(3)
        with col1:
            if process_status.get("running"):
                st.success("🟢 Process Running")
                st.caption(f"PID: {process_status.get('pid')}")
            else:
                st.info("⚪ Process Stopped")
        with col2:
            st.metric("Channel", f"@{process_status.get('channel_handle', 'N/A')}")
        with col3:
            # Get learning data status
            try:
                learning_status = st.session_state.continuous_learner.get_learning_status()
                total_sessions = learning_status.get("total_sessions", 0)
                st.metric("Total Sessions", total_sessions)
            except:
                st.metric("Total Sessions", "N/A")
        
        # Learning data info
        try:
            learning_status = st.session_state.continuous_learner.get_learning_status()
            last_learning = learning_status.get("last_learning")
            if last_learning:
                st.write(f"**Last Learning:** {datetime.fromisoformat(last_learning).strftime('%Y-%m-%d %H:%M')}")
            else:
                st.write("**Last Learning:** Never")
            
            st.write(f"**Learning Interval:** {learning_status.get('interval_seconds', 3600) / 60:.0f} minutes")
        except Exception as e:
            st.warning(f"Could not load learning data: {e}")
        
        # Important note
        if process_status.get("running"):
            st.info("💡 **Note:** The learning process runs as a separate Python process. It will continue running even if you close the dashboard or navigate away from this page. Use the 'Stop' button to terminate it.")
        else:
            st.warning("⚠️ **Note:** The learning process is not running. Click 'Start Learning Loop' to begin continuous learning.")
    
    with tab2:
        st.subheader("Generate Daily Learning Report")
        
        if st.button("📊 Generate Daily Report", use_container_width=True):
            with st.spinner("Generating daily report..."):
                try:
                    report = st.session_state.continuous_learner.generate_daily_report(st.session_state.target_channel)
                    
                    st.success(f"✅ Daily Report for {report.get('date', 'N/A')}")
                    
                    # Summary
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Learning Sessions", report.get("learning_sessions", 0))
                    with col2:
                        st.metric("Discoveries", report.get("discoveries", 0))
                    with col3:
                        st.metric("Viral Opportunities", len(report.get("viral_opportunities", [])))
                    
                    # Growth Trend
                    growth = report.get("growth_trend", {})
                    if growth.get("status") != "insufficient_data":
                        st.subheader("📈 Growth Trend")
                        growth_data = growth.get("growth", {}).get("subscribers", {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Daily Average Growth", f"{growth_data.get('daily_average', 0):.2f}")
                        with col2:
                            st.metric("Growth Rate", f"{growth_data.get('growth_rate_percent', 0):.2f}%")
                    
                    # Viral Opportunities
                    viral_opps = report.get("viral_opportunities", [])
                    if viral_opps:
                        st.subheader("🔥 Top Viral Opportunities")
                        for i, opp in enumerate(viral_opps[:5], 1):
                            with st.expander(f"#{i} - {opp.get('type', 'Unknown').replace('_', ' ').title()} - {opp.get('viral_potential', 0):.1%}"):
                                st.write(f"**Source:** {opp.get('source', 'N/A')}")
                                st.write(f"**Opportunity:** {opp.get('opportunity', 'N/A')}")
                    
                    # A/B Test Recommendations
                    ab_tests = report.get("ab_test_recommendations", [])
                    if ab_tests:
                        st.subheader("🧪 A/B Test Recommendations")
                        for test in ab_tests:
                            priority_color = "🔴" if test.get("priority") == "high" else "🟡"
                            st.write(f"{priority_color} **{test.get('type', 'Unknown').replace('_', ' ').title()}:** {test.get('test', 'N/A')}")
                            st.caption(test.get("reason", ""))
                    
                    # Key Insights
                    insights = report.get("key_insights", [])
                    if insights:
                        st.subheader("💡 Key Insights")
                        for insight in insights:
                            st.info(insight)
                    
                    # Recommendations
                    recommendations = report.get("recommendations", [])
                    if recommendations:
                        st.subheader("📋 Recommendations")
                        for rec in recommendations:
                            st.success(rec)
                            
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab3:
        st.subheader("Generate Weekly Learning Report")
        
        if st.button("📅 Generate Weekly Report", use_container_width=True):
            with st.spinner("Generating weekly report..."):
                try:
                    report = st.session_state.continuous_learner.get_weekly_report(st.session_state.target_channel)
                    
                    st.success(f"✅ Weekly Report: {report.get('week_start')} to {report.get('week_end')}")
                    
                    # Summary
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Daily Reports", report.get("daily_reports_count", 0))
                    with col2:
                        st.metric("Learning Sessions", report.get("total_learning_sessions", 0))
                    with col3:
                        st.metric("Discoveries", report.get("total_discoveries", 0))
                    with col4:
                        st.metric("Top Opportunities", len(report.get("top_discoveries", [])))
                    
                    # Growth Summary
                    growth = report.get("growth_summary", {})
                    if growth.get("status") != "insufficient_data":
                        st.subheader("📈 Weekly Growth Summary")
                        growth_data = growth.get("growth", {}).get("subscribers", {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Weekly Growth", f"{growth_data.get('change', 0):,}")
                        with col2:
                            st.metric("Daily Average", f"{growth_data.get('daily_average', 0):.2f}")
                        
                        projection = growth.get("projection", {})
                        if projection.get("days_to_1m"):
                            st.info(f"🎯 Projected time to 1M subscribers: {projection['days_to_1m']:,.0f} days")
                    
                    # Top Discoveries
                    top_discoveries = report.get("top_discoveries", [])
                    if top_discoveries:
                        st.subheader("🔥 Top Discoveries This Week")
                        for i, disc in enumerate(top_discoveries[:5], 1):
                            with st.expander(f"#{i} - {disc.get('opportunity', 'N/A')[:50]}..."):
                                st.write(f"**Viral Potential:** {disc.get('viral_potential', 0):.1%}")
                                st.write(f"**Source:** {disc.get('source', 'N/A')}")
                    
                    # Weekly Insights
                    insights = report.get("weekly_insights", [])
                    if insights:
                        st.subheader("💡 Weekly Insights")
                        for insight in insights:
                            st.success(insight)
                    
                    # Next Week Recommendations
                    recommendations = report.get("next_week_recommendations", [])
                    if recommendations:
                        st.subheader("📋 Recommendations for Next Week")
                        for rec in recommendations:
                            st.info(rec)
                            
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab4:
        st.subheader("Learning History")
        
        days = st.slider("Days to look back", 1, 30, 7)
        
        if st.button("📜 View Learning History", use_container_width=True):
            with st.spinner("Loading learning history..."):
                try:
                    history = st.session_state.continuous_learner.get_learning_history(days=days)
                    
                    st.subheader("History Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Sessions", history.get("sessions_count", 0))
                    with col2:
                        st.metric("Discoveries", history.get("discoveries_count", 0))
                    with col3:
                        st.metric("Period", f"{days} days")
                    
                    # Discovery Types
                    discovery_types = history.get("discovery_types", {})
                    if discovery_types:
                        st.subheader("Discovery Types")
                        for disc_type, count in discovery_types.items():
                            st.write(f"**{disc_type.replace('_', ' ').title()}:** {count}")
                    
                    # Recent Sessions
                    sessions = history.get("sessions", [])
                    if sessions:
                        st.subheader("Recent Learning Sessions")
                        for i, session in enumerate(sessions[:10], 1):
                            with st.expander(f"Session #{i} - {datetime.fromisoformat(session['timestamp']).strftime('%Y-%m-%d %H:%M')}"):
                                st.write(f"**Discoveries:** {len(session.get('discoveries', []))}")
                                st.write(f"**Updates:** {len(session.get('updates', []))}")
                                
                                if session.get("discoveries"):
                                    st.write("**Discoveries:**")
                                    for disc in session.get("discoveries", [])[:3]:
                                        st.write(f"• {disc.get('type', 'Unknown')}")
                                
                                if session.get("updates"):
                                    st.write("**Updates:**")
                                    for update in session.get("updates", [])[:5]:
                                        st.write(f"• {update}")
                    else:
                        st.info("No learning sessions found for this period.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")

elif is_page("code_self_improvement"):
    st.title(t("pages.code_self_improvement.title"))
    st.markdown("Optimize algorithms and improve code based on performance metrics")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Optimize Algorithms",
        "Code Suggestions",
        "Measure Improvement",
        "Set Baseline",
        "Optimization History"
    ])
    
    with tab1:
        st.subheader("Optimize Algorithm Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎯 Optimize Viral Predictor Weights", use_container_width=True):
                with st.spinner("Optimizing viral predictor weights..."):
                    try:
                        result = st.session_state.code_self_improver.optimize_viral_predictor_weights()
                        
                        if result.get("status") == "optimized":
                            st.success("✅ Weights optimized!")
                            
                            st.subheader("Weight Changes")
                            changes = result.get("changes", {})
                            for indicator, change_data in changes.items():
                                with st.expander(f"📊 {indicator.replace('_', ' ').title()}"):
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric("Before", f"{change_data.get('before', 0):.3f}")
                                    with col2:
                                        st.metric("After", f"{change_data.get('after', 0):.3f}")
                                    with col3:
                                        change_pct = change_data.get("change_percent", 0)
                                        st.metric("Change", f"{change_pct:+.1f}%")
                            
                            st.metric("Improvement Score", f"{result.get('improvement_score', 0):.3f}")
                            
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        with col2:
            if st.button("⚙️ Optimize All Parameters", use_container_width=True):
                with st.spinner("Optimizing all algorithm parameters..."):
                    try:
                        result = st.session_state.code_self_improver.optimize_algorithm_parameters()
                        
                        if result.get("status") == "optimized":
                            st.success("✅ Parameters optimized!")
                            
                            optimizations = result.get("optimizations", {})
                            for opt_type, opt_data in optimizations.items():
                                if "error" not in opt_data:
                                    with st.expander(f"📈 {opt_type.replace('_', ' ').title()}"):
                                        st.json(opt_data)
                            
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        if st.button("✅ Apply Optimizations", use_container_width=True):
            with st.spinner("Applying optimizations..."):
                try:
                    result = st.session_state.code_self_improver.apply_optimizations()
                    
                    st.success(f"✅ Applied {result.get('applied_count', 0)} optimization(s)!")
                    
                    applied = result.get("applied", [])
                    if applied:
                        st.subheader("Applied Optimizations")
                        for app in applied:
                            st.success(f"✅ {app.get('module', 'Unknown')} - {app.get('optimization', 'N/A')}")
                    
                    errors = result.get("errors", [])
                    if errors:
                        st.subheader("Errors")
                        for err in errors:
                            st.error(f"❌ {err.get('module', 'Unknown')}: {err.get('error', 'N/A')}")
                            
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab2:
        st.subheader("Code Update Suggestions")
        st.markdown("Get suggestions for code improvements based on learned patterns")
        
        if st.button("💡 Get Code Suggestions", use_container_width=True):
            with st.spinner("Analyzing patterns for code suggestions..."):
                try:
                    suggestions = st.session_state.code_self_improver.suggest_code_updates()
                    
                    st.metric("Suggestions Found", suggestions.get("suggestions_count", 0))
                    
                    sugg_list = suggestions.get("suggestions", [])
                    if sugg_list:
                        # Group by priority
                        high_priority = [s for s in sugg_list if s.get("priority") == "high"]
                        medium_priority = [s for s in sugg_list if s.get("priority") == "medium"]
                        low_priority = [s for s in sugg_list if s.get("priority") == "low"]
                        
                        if high_priority:
                            st.subheader("🔴 High Priority")
                            for sugg in high_priority:
                                with st.expander(f"📝 {sugg.get('module', 'Unknown')} - {sugg.get('type', 'Unknown').replace('_', ' ').title()}"):
                                    st.write(f"**Suggestion:** {sugg.get('suggestion', 'N/A')}")
                                    st.write(f"**Reason:** {sugg.get('reason', 'N/A')}")
                                    if sugg.get("current"):
                                        st.write(f"**Current:** {sugg.get('current', 'N/A')}")
                                    if sugg.get("recommended"):
                                        st.write(f"**Recommended:** {sugg.get('recommended', 'N/A')}")
                        
                        if medium_priority:
                            st.subheader("🟡 Medium Priority")
                            for sugg in medium_priority:
                                with st.expander(f"📝 {sugg.get('module', 'Unknown')} - {sugg.get('type', 'Unknown').replace('_', ' ').title()}"):
                                    st.write(f"**Suggestion:** {sugg.get('suggestion', 'N/A')}")
                                    st.write(f"**Reason:** {sugg.get('reason', 'N/A')}")
                        
                        if low_priority:
                            st.subheader("🟢 Low Priority")
                            for sugg in low_priority:
                                with st.expander(f"📝 {sugg.get('module', 'Unknown')} - {sugg.get('type', 'Unknown').replace('_', ' ').title()}"):
                                    st.write(f"**Suggestion:** {sugg.get('suggestion', 'N/A')}")
                                    st.write(f"**Reason:** {sugg.get('reason', 'N/A')}")
                    else:
                        st.info("No code suggestions at this time. Continue learning to generate suggestions.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab3:
        st.subheader("Measure Improvement")
        st.markdown("Compare current performance with baseline")
        
        days = st.slider("Analysis Period (days)", 1, 30, 7)
        
        if st.button("📊 Measure Improvement", use_container_width=True):
            with st.spinner("Measuring improvement..."):
                try:
                    improvement = st.session_state.code_self_improver.measure_improvement(days=days)
                    
                    baseline = improvement.get("baseline", {})
                    current = improvement.get("current", {})
                    improvements = improvement.get("improvements", {})
                    
                    if baseline:
                        st.subheader("Baseline vs Current")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if baseline.get("daily_growth"):
                                st.metric("Baseline Daily Growth", f"{baseline['daily_growth']:.2f}")
                        with col2:
                            if current.get("daily_growth"):
                                st.metric("Current Daily Growth", f"{current['daily_growth']:.2f}")
                        with col3:
                            if improvements.get("daily_growth"):
                                imp = improvements["daily_growth"]
                                st.metric("Improvement", f"{imp.get('improvement_percent', 0):+.1f}%")
                        
                        if baseline.get("success_rate") is not None:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Baseline Success Rate", f"{baseline['success_rate']:.1f}%")
                            with col2:
                                if current.get("success_rate") is not None:
                                    st.metric("Current Success Rate", f"{current['success_rate']:.1f}%")
                            with col3:
                                if improvements.get("success_rate"):
                                    imp = improvements["success_rate"]
                                    st.metric("Improvement", f"{imp.get('improvement_percent', 0):+.1f}%")
                        
                        # Overall improvement
                        overall = improvement.get("overall_improvement", 0)
                        if overall != 0:
                            st.subheader("Overall Improvement")
                            st.metric("Overall Score", f"{overall:+.1f}%")
                            if overall > 0:
                                st.success("🎉 System is improving!")
                            elif overall < 0:
                                st.warning("⚠️ Performance has decreased. Review optimizations.")
                    else:
                        st.warning("⚠️ No baseline set. Set a baseline first to measure improvements.")
                        st.info("Go to 'Set Baseline' tab to establish a performance baseline.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab4:
        st.subheader("Set Performance Baseline")
        st.markdown("Set current performance as baseline for future comparisons")
        
        if st.button("📌 Set Baseline", use_container_width=True):
            with st.spinner("Setting performance baseline..."):
                try:
                    result = st.session_state.code_self_improver.set_performance_baseline()
                    
                    if result.get("status") == "baseline_set":
                        st.success("✅ Baseline set successfully!")
                        
                        baseline = result.get("baseline", {})
                        st.subheader("Baseline Metrics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Daily Growth", f"{baseline.get('daily_growth', 0):.2f}")
                        with col2:
                            st.metric("Conversion Rate", f"{baseline.get('conversion_rate', 0):.2f}%")
                        with col3:
                            st.metric("Success Rate", f"{baseline.get('success_rate', 0):.1f}%")
                        with col4:
                            st.metric("Subscribers", f"{baseline.get('subscribers', 0):,}")
                        
                        st.info(f"📅 Baseline set on: {datetime.fromisoformat(baseline.get('timestamp', '')).strftime('%Y-%m-%d %H:%M')}")
                    else:
                        st.error(result.get("error", "Failed to set baseline"))
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab5:
        st.subheader("Optimization History")
        st.markdown("View history of all optimizations")
        
        if st.button("📜 View History", use_container_width=True):
            with st.spinner("Loading optimization history..."):
                try:
                    history = st.session_state.code_self_improver.get_optimization_history()
                    
                    st.metric("Total Improvements", history.get("total_improvements", 0))
                    
                    # Recent improvements
                    recent = history.get("recent_improvements", [])
                    if recent:
                        st.subheader("Recent Optimizations")
                        for i, imp in enumerate(recent[-10:], 1):
                            with st.expander(f"#{i} - {imp.get('module', 'Unknown')} - {datetime.fromisoformat(imp.get('timestamp', '')).strftime('%Y-%m-%d %H:%M')}"):
                                st.write(f"**Type:** {imp.get('optimization_type', 'N/A').replace('_', ' ').title()}")
                                st.write(f"**Improvement Score:** {imp.get('improvement_score', 0):.3f}")
                                st.write(f"**Reason:** {imp.get('reason', 'N/A')}")
                                
                                if imp.get("before") and imp.get("after"):
                                    st.write("**Before:**")
                                    st.json(imp["before"])
                                    st.write("**After:**")
                                    st.json(imp["after"])
                    
                    # Current config
                    config = history.get("current_config", {})
                    if config:
                        st.subheader("Current Optimized Configuration")
                        with st.expander("View Config"):
                            st.json(config)
                    
                    # Baseline
                    baseline = history.get("performance_baseline", {})
                    if baseline:
                        st.subheader("Performance Baseline")
                        st.json(baseline)
                    else:
                        st.info("No baseline set yet. Set a baseline to track improvements.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")

elif is_page("safety_ethics"):
    st.title(t("pages.safety_ethics.title"))
    st.markdown("Ensure content compliance with YouTube Community Guidelines and ethical standards")
    
    # Channel and Niche Inputs
    render_channel_niche_inputs()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Content Safety Check",
        "Filter Recommendations",
        "Ethical Guidelines",
        "Safety Statistics",
        "Recent Violations"
    ])
    
    with tab1:
        st.subheader("Check Content Safety")
        st.markdown("Analyze content for safety, ethics, and YouTube Community Guidelines compliance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title", placeholder="Enter video title", key="safety_ethics_title")
            description = st.text_area("Description", placeholder="Enter video description", height=150, key="safety_ethics_description")
        
        with col2:
            tags_input = st.text_input("Tags (comma-separated)", placeholder="tag1, tag2, tag3", key="safety_ethics_tags")
            content_type = st.selectbox("Content Type", ["video", "thumbnail", "recommendation"], key="safety_ethics_content_type")
        
        if st.button("🔍 Check Safety", use_container_width=True):
            if title:
                with st.spinner("Checking content safety..."):
                    try:
                        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
                        result = st.session_state.safety_ethics_layer.check_content_safety(
                            title=title,
                            description=description,
                            tags=tags,
                            content_type=content_type
                        )
                        
                        # Display results
                        st.subheader("Safety Check Results")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            risk_score = result.get("risk_score", 0)
                            if risk_score < 0.3:
                                st.metric("Risk Score", f"{risk_score:.2f}", delta="Safe", delta_color="normal")
                            elif risk_score < 0.5:
                                st.metric("Risk Score", f"{risk_score:.2f}", delta="Low Risk", delta_color="off")
                            elif risk_score < 0.7:
                                st.metric("Risk Score", f"{risk_score:.2f}", delta="Medium Risk", delta_color="inverse")
                            else:
                                st.metric("Risk Score", f"{risk_score:.2f}", delta="High Risk", delta_color="inverse")
                        
                        with col2:
                            clickbait_score = result.get("clickbait_score", 0)
                            st.metric("Clickbait Score", f"{clickbait_score:.2f}")
                        
                        with col3:
                            spam_score = result.get("spam_score", 0)
                            st.metric("Spam Score", f"{spam_score:.2f}")
                        
                        with col4:
                            safety_status = result.get("safety_status", "unknown")
                            status_emoji = {
                                "safe": "✅",
                                "low_risk": "⚠️",
                                "medium_risk": "🔶",
                                "high_risk": "🔴"
                            }
                            st.metric("Status", f"{status_emoji.get(safety_status, '❓')} {safety_status.replace('_', ' ').title()}")
                        
                        # Violations
                        violations = result.get("violations", {})
                        if violations:
                            st.error("🚨 Violations Detected")
                            for violation_type, keywords in violations.items():
                                with st.expander(f"⚠️ {violation_type.replace('_', ' ').title()}"):
                                    st.write("**Keywords found:**", ", ".join(keywords))
                        else:
                            st.success("✅ No violations detected")
                        
                        # Recommendation
                        recommendation = result.get("recommendation", "")
                        if recommendation:
                            st.info(f"💡 {recommendation}")
                        
                        # Suggestions
                        suggestions = result.get("suggestions", [])
                        if suggestions:
                            st.subheader("Safety Suggestions")
                            for suggestion in suggestions:
                                st.write(f"• {suggestion}")
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter a title to check")
    
    with tab2:
        st.subheader("Filter Recommendations")
        st.markdown("Filter a list of recommendations for safety and ethics compliance")
        
        recommendations_input = st.text_area(
            "Recommendations (one per line)",
            placeholder="Enter recommendations, one per line",
            height=200
        )
        
        if st.button("🔍 Filter Recommendations", use_container_width=True):
            if recommendations_input:
                with st.spinner("Filtering recommendations..."):
                    try:
                        recommendations = [r.strip() for r in recommendations_input.split("\n") if r.strip()]
                        result = st.session_state.safety_ethics_layer.filter_recommendations(recommendations)
                        
                        st.subheader("Filtering Results")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Checked", result.get("total_checked", 0))
                        with col2:
                            st.metric("Safe", result.get("safe_count", 0), delta_color="normal")
                        with col3:
                            st.metric("Filtered Out", result.get("filtered_count", 0), delta_color="inverse")
                        
                        # Safe recommendations
                        safe_recs = result.get("safe_recommendations", [])
                        if safe_recs:
                            st.subheader("✅ Safe Recommendations")
                            for rec in safe_recs:
                                with st.expander(f"✅ {rec.get('recommendation', '')[:60]}..."):
                                    st.write(f"**Risk Score:** {rec.get('risk_score', 0):.2f}")
                                    st.write(f"**Status:** {rec.get('safety_status', 'unknown')}")
                        
                        # Filtered out
                        filtered = result.get("filtered_out", [])
                        if filtered:
                            st.subheader("🚫 Filtered Out")
                            for rec in filtered:
                                with st.expander(f"🚫 {rec.get('recommendation', '')[:60]}..."):
                                    st.write(f"**Risk Score:** {rec.get('risk_score', 0):.2f}")
                                    st.write(f"**Status:** {rec.get('safety_status', 'unknown')}")
                                    if rec.get("reasons"):
                                        st.write("**Reasons:**")
                                        st.json(rec.get("reasons"))
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter recommendations to filter")
    
    with tab3:
        st.subheader("Ethical Guidelines")
        st.markdown("Guidelines for creating ethical and compliant content")
        
        try:
            guidelines = st.session_state.safety_ethics_layer.get_ethical_guidelines()
            
            st.markdown("### Core Principles")
            for principle, description in guidelines.get("guidelines", {}).items():
                with st.expander(f"📋 {principle.replace('_', ' ').title()}"):
                    st.write(description)
            
            st.markdown("### Best Practices")
            best_practices = guidelines.get("best_practices", [])
            for practice in best_practices:
                st.write(f"✅ {practice}")
            
            st.markdown("### Things to Avoid")
            avoid = guidelines.get("avoid", [])
            for item in avoid:
                st.write(f"❌ {item}")
                
        except Exception as e:
            st.error(f"Error: {e}")
    
    with tab4:
        st.subheader("Safety Statistics")
        st.markdown("Overall safety and compliance statistics")
        
        try:
            stats = st.session_state.safety_ethics_layer.get_safety_statistics()
            
            if stats.get("total_checks", 0) > 0:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Checks", stats.get("total_checks", 0))
                
                with col2:
                    violation_rate = stats.get("violation_rate", 0)
                    st.metric("Violation Rate", f"{violation_rate:.1%}")
                
                with col3:
                    clickbait_rate = stats.get("clickbait_rate", 0)
                    st.metric("Clickbait Rate", f"{clickbait_rate:.1%}")
                
                with col4:
                    safety_rate = stats.get("safety_rate", 0)
                    st.metric("Safety Rate", f"{safety_rate:.1%}", delta_color="normal")
                
                st.markdown("---")
                
                st.subheader("Detailed Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Violations Found", stats.get("violations_found", 0))
                with col2:
                    st.metric("Clickbait Detected", stats.get("clickbait_detected", 0))
                with col3:
                    st.metric("Spam Detected", stats.get("spam_detected", 0))
                with col4:
                    st.metric("Safe Content", stats.get("safe_content_count", 0))
            else:
                st.info("No safety checks performed yet. Use the Content Safety Check tab to start.")
                
        except Exception as e:
            st.error(f"Error: {e}")
    
    with tab5:
        st.subheader("Recent Violations")
        st.markdown("Recently detected violations and filtered content")
        
        try:
            limit = st.number_input("Number of violations to show", min_value=1, max_value=50, value=10)
            
            if st.button("🔄 Refresh", use_container_width=True):
                violations = st.session_state.safety_ethics_layer.get_recent_violations(limit=limit)
                
                if violations:
                    for i, violation in enumerate(reversed(violations), 1):
                        with st.expander(f"🚨 Violation #{i} - {violation.get('timestamp', 'Unknown')[:10]}"):
                            violations_data = violation.get("violations", {})
                            for violation_type, keywords in violations_data.items():
                                st.write(f"**{violation_type.replace('_', ' ').title()}:**")
                                st.write(", ".join(keywords))
                            
                            content = violation.get("content", {})
                            if content:
                                st.write("**Content:**")
                                st.write(f"Title: {content.get('title', 'N/A')}")
                                if content.get("description"):
                                    st.write(f"Description: {content.get('description', '')[:200]}...")
                else:
                    st.success("✅ No violations detected recently!")
        except Exception as e:
            st.error(f"Error: {e}")

elif is_page("video_seo_audit"):
    st.title("🔍 Video SEO Audit")
    st.markdown("Comprehensive SEO analysis for your videos")
    
    render_channel_niche_inputs()
    
    # Video selection
    video_id_input = st.text_input(
        "Video ID or URL",
        placeholder="Enter YouTube video ID or full URL",
        help="You can find the video ID in the YouTube URL: youtube.com/watch?v=VIDEO_ID",
        key="seo_audit_video_id"
    )
    
    if video_id_input:
        # Extract video ID from URL if needed
        video_id = video_id_input
        if "youtube.com" in video_id or "youtu.be" in video_id:
            import re
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', video_id)
            if video_id_match:
                video_id = video_id_match.group(1)
        
        if st.button("🔍 Audit Video", use_container_width=True, type="primary"):
            with st.spinner("Analyzing video SEO..."):
                try:
                    audit_result = st.session_state.video_seo_audit.audit_video(video_id)
                    
                    if "error" in audit_result:
                        st.error(f"Error: {audit_result['error']}")
                    else:
                        # Overall Score
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Overall SEO Score", f"{audit_result['overall_seo_score']}/100", 
                                     audit_result.get('seo_grade', 'N/A'))
                        with col2:
                            improvement = audit_result.get('improvement_potential', {})
                            st.metric("Improvement Potential", 
                                     f"+{improvement.get('improvement_points', 0)} points")
                        with col3:
                            st.metric("SEO Grade", audit_result.get('seo_grade', 'N/A'))
                        
                        st.markdown("---")
                        
                        # Detailed Analysis
                        st.subheader("📊 Detailed Analysis")
                        audit_details = audit_result.get('audit_details', {})
                        
                        tabs = st.tabs(["Title", "Description", "Tags", "Thumbnail"])
                        
                        with tabs[0]:
                            title_audit = audit_details.get('title', {})
                            st.metric("Title Score", f"{title_audit.get('score', 0)}/100", 
                                     title_audit.get('status', 'unknown'))
                            st.write(f"**Title:** {title_audit.get('title', 'N/A')}")
                            st.write(f"**Length:** {title_audit.get('length', 0)} characters")
                            if title_audit.get('recommendations'):
                                st.write("**Recommendations:**")
                                for rec in title_audit['recommendations']:
                                    st.write(f"- {rec}")
                        
                        with tabs[1]:
                            desc_audit = audit_details.get('description', {})
                            st.metric("Description Score", f"{desc_audit.get('score', 0)}/100",
                                     desc_audit.get('status', 'unknown'))
                            st.write(f"**Word Count:** {desc_audit.get('word_count', 0)}")
                            st.write(f"**Character Count:** {desc_audit.get('character_count', 0)}")
                            st.write(f"**Hashtags:** {desc_audit.get('hashtag_count', 0)}")
                            if desc_audit.get('recommendations'):
                                st.write("**Recommendations:**")
                                for rec in desc_audit['recommendations']:
                                    st.write(f"- {rec}")
                        
                        with tabs[2]:
                            tags_audit = audit_details.get('tags', {})
                            st.metric("Tags Score", f"{tags_audit.get('score', 0)}/100",
                                     tags_audit.get('status', 'unknown'))
                            st.write(f"**Tag Count:** {tags_audit.get('tag_count', 0)}")
                            st.write(f"**Keyword Coverage:** {tags_audit.get('keyword_coverage', 'N/A')}")
                            if tags_audit.get('recommendations'):
                                st.write("**Recommendations:**")
                                for rec in tags_audit['recommendations']:
                                    st.write(f"- {rec}")
                        
                        with tabs[3]:
                            thumb_audit = audit_details.get('thumbnail', {})
                            st.metric("Thumbnail Score", f"{thumb_audit.get('score', 0)}/100",
                                     thumb_audit.get('status', 'unknown'))
                            if thumb_audit.get('recommendations'):
                                st.write("**Recommendations:**")
                                for rec in thumb_audit['recommendations']:
                                    st.write(f"- {rec}")
                        
                        # Priority Actions
                        st.markdown("---")
                        st.subheader("🎯 Priority Actions")
                        priority_actions = audit_result.get('priority_actions', [])
                        for action in priority_actions[:5]:
                            with st.expander(f"{action.get('action', 'Action')} - Priority: {action.get('priority', 'medium').upper()}"):
                                st.write(f"**Current Score:** {action.get('current_score', 0)}/100")
                                st.write(f"**Impact:** {action.get('impact', 'medium')}")
                                st.write(f"**Quick Fix:** {action.get('quick_fix', 'N/A')}")
                        
                        # Recommendations
                        st.markdown("---")
                        st.subheader("💡 Recommendations")
                        recommendations = audit_result.get('recommendations', [])
                        for rec in recommendations:
                            with st.expander(f"{rec.get('category', 'General').title()} - {rec.get('priority', 'medium').upper()} Priority"):
                                st.write(rec.get('message', ''))
                                if rec.get('details'):
                                    st.write("**Details:**")
                                    for detail in rec['details']:
                                        st.write(f"- {detail}")
                
                except Exception as e:
                    st.error(f"Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())

elif is_page("caption_optimizer"):
    st.title("📝 Caption & Transcript Optimizer")
    st.markdown("Optimize your video captions for better SEO")
    
    render_channel_niche_inputs()
    
    video_id_input = st.text_input(
        "Video ID or URL",
        placeholder="Enter YouTube video ID or full URL",
        key="caption_optimizer_video_id"
    )
    
    if video_id_input:
        import re
        video_id = video_id_input
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', video_id)
            if video_id_match:
                video_id = video_id_match.group(1)
        
        tab1, tab2, tab3 = st.tabs(["Analyze Captions", "Optimize", "Multilingual Support"])
        
        with tab1:
            if st.button("📊 Analyze Captions", use_container_width=True, type="primary"):
                with st.spinner("Analyzing captions..."):
                    try:
                        keywords_input = st.text_input("Target Keywords (comma-separated)", 
                                                       value="",
                                                       placeholder="Örn: techno, electronic, underground, minimal",
                                                       key="caption_analyze_keywords")
                        keywords = [k.strip() for k in keywords_input.split(",")] if keywords_input else None
                        
                        analysis = st.session_state.caption_optimizer.analyze_captions(video_id, keywords)
                        
                        if "error" in analysis:
                            st.error(f"❌ **Error:** {analysis['error']}")
                            
                            # Special handling for OAuth2 requirement
                            if analysis.get('error_type') == 'oauth2_required':
                                st.warning("🔐 **OAuth2 Authentication Required**")
                                st.markdown("""
                                **Why this happens:**
                                - YouTube Captions API requires OAuth2 authentication (not just API key)
                                - You can only download captions for videos you own
                                - This is a YouTube API security requirement
                                """)
                            
                            if "recommendation" in analysis:
                                st.info(f"💡 **Recommendation:**\n\n{analysis['recommendation']}")
                            
                            if "workaround" in analysis:
                                st.success(f"✅ **Workaround:**\n\n{analysis['workaround']}")
                            
                            if "download_error" in analysis:
                                with st.expander("🔧 Technical Details"):
                                    st.code(analysis['download_error'], language=None)
                            
                            if "available_languages" in analysis:
                                st.info(f"📝 **Available Languages:** {', '.join(analysis['available_languages'])}")
                        else:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("SEO Score", f"{analysis.get('seo_score', 0)}/100")
                            with col2:
                                st.metric("Word Count", analysis.get('word_count', 0))
                            with col3:
                                st.metric("Keywords Found", f"{analysis.get('keywords_in_first_200', 0)}/{analysis.get('total_keywords', 0)}")
                            
                            st.markdown("---")
                            st.subheader("Keyword Analysis")
                            keyword_analysis = analysis.get('keyword_analysis', {})
                            for keyword, data in keyword_analysis.items():
                                with st.expander(f"Keyword: {keyword}"):
                                    st.write(f"**Count:** {data.get('count', 0)}")
                                    st.write(f"**Density:** {data.get('density', 0)}%")
                                    st.write(f"**Present:** {'Yes' if data.get('present') else 'No'}")
                            
                            st.markdown("---")
                            st.subheader("Recommendations")
                            for rec in analysis.get('recommendations', []):
                                st.write(f"- {rec}")
                            
                            if analysis.get('transcript_preview'):
                                with st.expander("Transcript Preview"):
                                    st.text(analysis['transcript_preview'])
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        with tab2:
            if st.button("✨ Optimize Captions", use_container_width=True, type="primary"):
                with st.spinner("Generating optimization suggestions..."):
                    try:
                        keywords_input = st.text_input("Target Keywords (comma-separated)", 
                                                       value="",
                                                       placeholder="Örn: techno, electronic, underground, minimal",
                                                       key="optimize_keywords")
                        keywords = [k.strip() for k in keywords_input.split(",")] if keywords_input else None
                        
                        optimization = st.session_state.caption_optimizer.optimize_captions(video_id, keywords)
                        
                        if "error" in optimization:
                            st.error(f"Error: {optimization['error']}")
                        else:
                            st.metric("Current SEO Score", f"{optimization.get('current_seo_score', 0)}/100")
                            improvement = optimization.get('estimated_improvement', {})
                            st.metric("Potential Score", f"{improvement.get('potential_score', 0)}/100",
                                     f"+{improvement.get('improvement_points', 0)} points")
                            
                            st.markdown("---")
                            st.subheader("Optimization Suggestions")
                            suggestions = optimization.get('optimization_suggestions', [])
                            for suggestion in suggestions:
                                with st.expander(f"{suggestion.get('keyword', 'General')} - {suggestion.get('action', 'optimize')}"):
                                    st.write(suggestion.get('suggestion', ''))
                                    if suggestion.get('example'):
                                        st.code(suggestion['example'])
                            
                            st.markdown("---")
                            st.subheader("Best Practices")
                            for practice in optimization.get('best_practices', []):
                                st.write(f"✅ {practice}")
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        with tab3:
            if st.button("🌍 Check Multilingual Support", use_container_width=True, type="primary"):
                with st.spinner("Checking multilingual support..."):
                    try:
                        support = st.session_state.caption_optimizer.get_multilingual_support(video_id)
                        
                        if "error" in support:
                            st.error(f"Error: {support['error']}")
                        else:
                            st.metric("Available Languages", support.get('language_count', 0))
                            
                            st.markdown("---")
                            st.subheader("Available Languages")
                            languages = support.get('available_languages', [])
                            for lang in languages:
                                st.write(f"- **{lang.get('language_name', lang.get('language', 'Unknown'))}** ({lang.get('language', 'N/A')})")
                                if lang.get('is_auto_generated'):
                                    st.caption("Auto-generated")
                            
                            st.markdown("---")
                            st.subheader("Recommendations")
                            for rec in support.get('recommendations', []):
                                st.write(f"- {rec}")
                    
                    except Exception as e:
                        st.error(f"Error: {e}")

elif is_page("engagement_booster"):
    st.title("🎯 Engagement Booster")
    st.markdown("Suggest polls, cards, and end screens to boost engagement")
    
    render_channel_niche_inputs()
    
    video_id_input = st.text_input(
        "Video ID or URL",
        placeholder="Enter YouTube video ID or full URL",
        key="engagement_booster_video_id"
    )
    
    if video_id_input:
        import re
        video_id = video_id_input
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', video_id)
            if video_id_match:
                video_id = video_id_match.group(1)
        
        if st.button("🎯 Get Engagement Suggestions", use_container_width=True, type="primary"):
            with st.spinner("Analyzing engagement opportunities..."):
                try:
                    # Get niche from session state
                    niche = st.session_state.get("target_niche", "")
                    suggestions = st.session_state.engagement_booster.suggest_engagement_elements(video_id, niche=niche)
                    
                    if "error" in suggestions:
                        st.error(f"Error: {suggestions['error']}")
                    else:
                        st.metric("Engagement Score", f"{suggestions.get('engagement_score', 0)}/100")
                        st.write(f"**Video Duration:** {suggestions.get('video_duration_seconds', 0)} seconds")
                        
                        st.markdown("---")
                        
                        tabs = st.tabs(["Polls", "Cards", "End Screens", "Priority Actions"])
                        
                        with tabs[0]:
                            st.subheader("📊 Poll Suggestions")
                            poll_suggestions = suggestions.get('suggestions', {}).get('polls', [])
                            for i, poll in enumerate(poll_suggestions, 1):
                                if poll.get('recommendation'):
                                    st.info(poll['recommendation'])
                                else:
                                    with st.expander(f"Poll #{i}: {poll.get('question', 'Question')}"):
                                        st.write(f"**Timing:** {poll.get('timing_seconds', 0)}s ({poll.get('timing_percentage', 0)}%)")
                                        st.write(f"**Reason:** {poll.get('reason', 'N/A')}")
                                        st.write(f"**Priority:** {poll.get('priority', 'medium')}")
                                        st.write("**Options:**")
                                        for option in poll.get('options', []):
                                            st.write(f"- {option}")
                        
                        with tabs[1]:
                            st.subheader("🎴 Card Suggestions")
                            card_suggestions = suggestions.get('suggestions', {}).get('cards', [])
                            for i, card in enumerate(card_suggestions, 1):
                                if card.get('recommendation'):
                                    st.info(card['recommendation'])
                                else:
                                    with st.expander(f"Card #{i}: {card.get('title', 'Card')}"):
                                        st.write(f"**Type:** {card.get('type', 'N/A')}")
                                        st.write(f"**Timing:** {card.get('timing_seconds', 0)}s ({card.get('timing_percentage', 0)}%)")
                                        st.write(f"**Reason:** {card.get('reason', 'N/A')}")
                                        st.write(f"**Priority:** {card.get('priority', 'medium')}")
                                        if card.get('best_practices'):
                                            st.write("**Best Practices:**")
                                            for practice in card['best_practices']:
                                                st.write(f"- {practice}")
                        
                        with tabs[2]:
                            st.subheader("📺 End Screen Suggestions")
                            end_screen_suggestions = suggestions.get('suggestions', {}).get('end_screens', [])
                            for i, end_screen in enumerate(end_screen_suggestions, 1):
                                with st.expander(f"End Screen #{i}: {end_screen.get('title', 'Element')}"):
                                    st.write(f"**Type:** {end_screen.get('type', 'N/A')}")
                                    st.write(f"**Timing:** {end_screen.get('timing_seconds', 0)}s")
                                    st.write(f"**Duration:** {end_screen.get('duration_seconds', 0)}s")
                                    st.write(f"**Position:** {end_screen.get('position', 'N/A')}")
                                    st.write(f"**Reason:** {end_screen.get('reason', 'N/A')}")
                                    st.write(f"**Priority:** {end_screen.get('priority', 'medium')}")
                                    if end_screen.get('best_practices'):
                                        st.write("**Best Practices:**")
                                        for practice in end_screen['best_practices']:
                                            st.write(f"- {practice}")
                        
                        with tabs[3]:
                            st.subheader("🎯 Priority Actions")
                            priority_actions = suggestions.get('priority_actions', [])
                            for action in priority_actions:
                                with st.expander(f"{action.get('action', 'Action')} - {action.get('priority', 'medium').upper()} Priority"):
                                    st.write(f"**Impact:** {action.get('impact', 'medium')}")
                                    st.write(f"**Reason:** {action.get('reason', 'N/A')}")
                                    st.write(f"**Quick Start:** {action.get('quick_start', 'N/A')}")
                        
                        st.markdown("---")
                        st.subheader("📚 Best Practices")
                        best_practices = suggestions.get('best_practices', {})
                        for category, practices in best_practices.items():
                            with st.expander(f"{category.title()}"):
                                for practice in practices:
                                    st.write(f"- {practice}")
                
                except Exception as e:
                    st.error(f"Error: {e}")

elif is_page("thumbnail_enhancer"):
    st.title("🖼️ Thumbnail Enhancer")
    st.markdown("Analyze and improve your video thumbnails for better CTR")
    
    render_channel_niche_inputs()
    
    video_id_input = st.text_input(
        "Video ID or URL",
        placeholder="Enter YouTube video ID or full URL",
        key="thumbnail_enhancer_video_id"
    )
    
    if video_id_input:
        import re
        video_id = video_id_input
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', video_id)
            if video_id_match:
                video_id = video_id_match.group(1)
        
        tab1, tab2, tab3 = st.tabs(["Analyze", "Improvements", "A/B Tests"])
        
        with tab1:
            if st.button("🔍 Analyze Thumbnail", use_container_width=True, type="primary"):
                with st.spinner("Analyzing thumbnail..."):
                    try:
                        analysis = st.session_state.thumbnail_enhancer.analyze_thumbnail(video_id)
                        
                        if "error" in analysis:
                            st.error(f"Error: {analysis['error']}")
                        else:
                            ctr_potential = analysis.get('ctr_potential', {})
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("CTR Score", f"{ctr_potential.get('score', 0)}/100",
                                         ctr_potential.get('grade', 'N/A'))
                            with col2:
                                st.metric("CTR Estimate", ctr_potential.get('ctr_estimate', 'N/A'))
                            with col3:
                                st.metric("Improvement Potential", 
                                         f"+{ctr_potential.get('improvement_potential', 0)} points")
                            
                            if analysis.get('thumbnail_url'):
                                st.image(analysis['thumbnail_url'], caption="Current Thumbnail", width=400)
                            
                            st.markdown("---")
                            st.subheader("Analysis Details")
                            analysis_details = analysis.get('analysis', {})
                            st.write(f"**Resolution:** {analysis_details.get('resolution', 'N/A')}")
                            st.write(f"**Has Text Overlay:** {'Yes' if analysis_details.get('has_text_overlay') else 'No'}")
                            st.write(f"**Title Relevance:** {'Yes' if analysis_details.get('title_relevance') else 'No'}")
                            
                            st.markdown("---")
                            st.subheader("Recommendations")
                            recommendations = analysis.get('recommendations', [])
                            for rec in recommendations:
                                with st.expander(f"{rec.get('category', 'General').title()} - {rec.get('priority', 'medium').upper()} Priority"):
                                    st.write(f"**Issue:** {rec.get('issue', 'N/A')}")
                                    st.write(f"**Recommendation:** {rec.get('recommendation', 'N/A')}")
                                    st.write(f"**Impact:** {rec.get('impact', 'medium')}")
                                    if rec.get('tips'):
                                        st.write("**Tips:**")
                                        for tip in rec['tips']:
                                            st.write(f"- {tip}")
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        with tab2:
            if st.button("✨ Get Improvement Suggestions", use_container_width=True, type="primary"):
                with st.spinner("Generating improvement suggestions..."):
                    try:
                        improvements = st.session_state.thumbnail_enhancer.suggest_thumbnail_improvements(video_id)
                        
                        if "error" in improvements:
                            st.error(f"Error: {improvements['error']}")
                        else:
                            current_ctr = improvements.get('current_ctr_potential', {})
                            st.metric("Current CTR Score", f"{current_ctr.get('score', 0)}/100")
                            
                            estimated = improvements.get('estimated_total_improvement', {})
                            st.metric("Potential CTR Score", f"{estimated.get('potential_new_score', 0)}/100",
                                     f"Grade: {estimated.get('grade_improvement', 'N/A')}")
                            
                            st.markdown("---")
                            st.subheader("Improvement Suggestions")
                            improvement_list = improvements.get('improvements', [])
                            for improvement in improvement_list:
                                with st.expander(f"{improvement.get('improvement', 'Improvement')} - {improvement.get('priority', 'medium').upper()} Priority"):
                                    st.write(f"**Description:** {improvement.get('description', 'N/A')}")
                                    st.write(f"**Expected Impact:** {improvement.get('expected_impact', 'N/A')}")
                                    st.write("**Implementation Steps:**")
                                    for step in improvement.get('implementation', []):
                                        st.write(f"- {step}")
                            
                            st.markdown("---")
                            st.subheader("Next Steps")
                            for step in improvements.get('next_steps', []):
                                st.write(f"✅ {step}")
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        with tab3:
            if st.button("🧪 Get A/B Test Suggestions", use_container_width=True, type="primary"):
                with st.spinner("Generating A/B test suggestions..."):
                    try:
                        analysis = st.session_state.thumbnail_enhancer.analyze_thumbnail(video_id)
                        
                        if "error" in analysis:
                            st.error(f"Error: {analysis['error']}")
                        else:
                            ab_tests = analysis.get('ab_test_suggestions', [])
                            st.subheader("A/B Test Suggestions")
                            
                            for test in ab_tests:
                                with st.expander(f"{test.get('test_name', 'Test')} - {test.get('priority', 'medium').upper()} Priority"):
                                    st.write(f"**Variation A:** {test.get('variation_a', 'N/A')}")
                                    st.write(f"**Variation B:** {test.get('variation_b', 'N/A')}")
                                    st.write(f"**Hypothesis:** {test.get('hypothesis', 'N/A')}")
                                    st.write(f"**Metric:** {test.get('metric', 'N/A')}")
                                    st.write(f"**Duration:** {test.get('duration', 'N/A')}")
                            
                            st.markdown("---")
                            st.subheader("Best Practices")
                            best_practices = analysis.get('best_practices', {})
                            for category, practices in best_practices.items():
                                with st.expander(f"{category.title()}"):
                                    for practice in practices:
                                        st.write(f"- {practice}")
                    
                    except Exception as e:
                        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("**YouTube SEO AGI Tool** - Universal Self-Evolving Open-Source AGI Assistant")

