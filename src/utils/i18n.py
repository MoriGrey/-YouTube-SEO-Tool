"""
Internationalization (i18n) Module
Provides translation support for Turkish and English.
"""

import json
import os
from typing import Dict, Any, Optional

# Locale directory path
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "../../locales")

# Supported languages
SUPPORTED_LANGUAGES = ["tr", "en", "de", "nl", "fr", "es"]

# Default language
DEFAULT_LANGUAGE = "tr"

# Cache for loaded translations
_translations_cache: Dict[str, Dict[str, Any]] = {}


def load_translations(language: str) -> Dict[str, Any]:
    """
    Load translations for a specific language.
    
    Args:
        language: Language code (tr, en)
    
    Returns:
        Dictionary of translations
    """
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    
    # Check cache first
    if language in _translations_cache:
        return _translations_cache[language]
    
    # Load from file
    locale_file = os.path.join(LOCALE_DIR, f"{language}.json")
    
    try:
        with open(locale_file, "r", encoding="utf-8") as f:
            translations = json.load(f)
            _translations_cache[language] = translations
            return translations
    except FileNotFoundError:
        # Fallback to default language
        if language != DEFAULT_LANGUAGE:
            return load_translations(DEFAULT_LANGUAGE)
        return {}
    except Exception as e:
        print(f"Error loading translations for {language}: {e}")
        return {}


def get_translation(key: str, language: str, **kwargs) -> str:
    """
    Get translation for a key.
    
    Args:
        key: Translation key (e.g., "common.subscribers")
        language: Language code
        **kwargs: Variables to substitute in translation
    
    Returns:
        Translated string
    """
    translations = load_translations(language)
    
    # Navigate through nested keys (e.g., "common.subscribers")
    keys = key.split(".")
    value = translations
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            break
    
    # If translation not found, return key
    if not isinstance(value, str):
        return key
    
    # Substitute variables
    if kwargs:
        try:
            return value.format(**kwargs)
        except (KeyError, ValueError):
            return value
    
    return value


def t(key: str, language: Optional[str] = None, **kwargs) -> str:
    """
    Translation function (shortcut).
    
    Args:
        key: Translation key
        language: Language code (if None, uses default)
        **kwargs: Variables to substitute
    
    Returns:
        Translated string
    """
    if language is None:
        # Try to get from streamlit session state if available
        try:
            import streamlit as st
            language = st.session_state.get("language", DEFAULT_LANGUAGE)
        except:
            language = DEFAULT_LANGUAGE
    
    return get_translation(key, language, **kwargs)


def set_language(language: str):
    """
    Set default language.
    
    Args:
        language: Language code
    """
    if language in SUPPORTED_LANGUAGES:
        try:
            import streamlit as st
            st.session_state.language = language
        except:
            pass


def get_language() -> str:
    """
    Get current language.
    
    Returns:
        Language code
    """
    try:
        import streamlit as st
        return st.session_state.get("language", DEFAULT_LANGUAGE)
    except:
        return DEFAULT_LANGUAGE

