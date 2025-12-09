#!/usr/bin/env python3
"""
Localization Framework
======================
Multi-language support for games.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from enum import Enum

from logging_config import get_logger
from error_handling import error_context


logger = get_logger(__name__)


class Language(Enum):
    """Supported languages"""
    ENGLISH = ("en", "English")
    SPANISH = ("es", "Español")
    FRENCH = ("fr", "Français")
    GERMAN = ("de", "Deutsch")
    ITALIAN = ("it", "Italiano")
    PORTUGUESE = ("pt", "Português")
    RUSSIAN = ("ru", "Русский")
    JAPANESE = ("ja", "日本語")
    KOREAN = ("ko", "한국어")
    CHINESE_SIMPLIFIED = ("zh-CN", "简体中文")
    CHINESE_TRADITIONAL = ("zh-TW", "繁體中文")

    def __init__(self, code: str, native_name: str):
        self.code = code
        self.native_name = native_name


@dataclass
class TranslationMetadata:
    """Metadata about a translation"""
    language_code: str
    language_name: str
    version: str
    author: str
    completion_percent: float
    last_updated: str


class Localization:
    """
    Localization system for multi-language support.

    Features:
    - Load translations from JSON files
    - Fallback to English if translation missing
    - Pluralization support
    - Variable substitution
    - Context-aware translations
    - Easy to add new languages
    """

    def __init__(
        self,
        game_id: str,
        localization_dir: Optional[Path] = None,
        default_language: str = "en"
    ):
        """
        Initialize localization system.

        Args:
            game_id: Game identifier
            localization_dir: Directory containing translation files
            default_language: Default language code
        """
        self.game_id = game_id
        self.logger = get_logger(__name__)

        # Localization directory
        if localization_dir is None:
            localization_dir = Path("localization") / game_id
        self.localization_dir = localization_dir
        self.localization_dir.mkdir(parents=True, exist_ok=True)

        # Current language
        self.current_language = default_language

        # Translations cache
        self.translations: Dict[str, Dict[str, Any]] = {}

        # Metadata
        self.metadata: Dict[str, TranslationMetadata] = {}

        # Load English (fallback)
        self._load_language("en")

        # Load current language if different
        if default_language != "en":
            self._load_language(default_language)

    def _load_language(self, language_code: str):
        """Load translations for a language"""
        lang_file = self.localization_dir / f"{language_code}.json"

        if not lang_file.exists():
            if language_code == "en":
                # Create default English file
                self._create_default_english()
                return
            else:
                self.logger.warning(f"Translation file not found: {lang_file}")
                return

        with error_context(f"loading {language_code} translations"):
            with open(lang_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Store translations
            self.translations[language_code] = data.get('translations', {})

            # Store metadata
            meta = data.get('metadata', {})
            self.metadata[language_code] = TranslationMetadata(
                language_code=language_code,
                language_name=meta.get('language_name', language_code),
                version=meta.get('version', '1.0'),
                author=meta.get('author', 'Unknown'),
                completion_percent=meta.get('completion_percent', 100.0),
                last_updated=meta.get('last_updated', 'Unknown')
            )

            self.logger.info(f"Loaded {language_code} translations")

    def _create_default_english(self):
        """Create default English translation file"""
        default_translations = {
            'metadata': {
                'language_code': 'en',
                'language_name': 'English',
                'version': '1.0',
                'author': 'Default',
                'completion_percent': 100.0,
                'last_updated': '2025-01-01'
            },
            'translations': {
                # Common UI
                'ui.yes': 'Yes',
                'ui.no': 'No',
                'ui.ok': 'OK',
                'ui.cancel': 'Cancel',
                'ui.back': 'Back',
                'ui.next': 'Next',
                'ui.quit': 'Quit',
                'ui.save': 'Save',
                'ui.load': 'Load',
                'ui.settings': 'Settings',
                'ui.help': 'Help',

                # Common game terms
                'game.health': 'Health',
                'game.level': 'Level',
                'game.score': 'Score',
                'game.inventory': 'Inventory',
                'game.pause': 'Pause',
                'game.resume': 'Resume',

                # Messages
                'msg.game_saved': 'Game saved successfully!',
                'msg.game_loaded': 'Game loaded successfully!',
                'msg.error': 'An error occurred',
                'msg.confirm_quit': 'Are you sure you want to quit?',
            }
        }

        lang_file = self.localization_dir / "en.json"
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(default_translations, f, indent=2, ensure_ascii=False)

        self.translations['en'] = default_translations['translations']

    def set_language(self, language_code: str):
        """
        Change current language.

        Args:
            language_code: Language code (e.g., 'es', 'fr')
        """
        if language_code not in self.translations:
            self._load_language(language_code)

        self.current_language = language_code
        self.logger.info(f"Language changed to: {language_code}")

    def get(self, key: str, **kwargs) -> str:
        """
        Get translated string.

        Args:
            key: Translation key (e.g., 'ui.yes')
            **kwargs: Variables to substitute

        Returns:
            Translated string
        """
        # Try current language
        translation = self._get_from_language(self.current_language, key)

        # Fallback to English
        if translation is None and self.current_language != 'en':
            translation = self._get_from_language('en', key)

        # Final fallback: return key
        if translation is None:
            self.logger.warning(f"Missing translation: {key}")
            return key

        # Substitute variables
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError as e:
                self.logger.error(f"Missing variable in translation {key}: {e}")

        return translation

    def _get_from_language(self, language_code: str, key: str) -> Optional[str]:
        """Get translation from specific language"""
        if language_code not in self.translations:
            return None

        # Support nested keys (e.g., 'ui.yes')
        parts = key.split('.')
        value = self.translations[language_code]

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None

        return str(value) if value is not None else None

    def get_plural(
        self,
        key: str,
        count: int,
        **kwargs
    ) -> str:
        """
        Get plural form of translation.

        Args:
            key: Base translation key
            count: Number for pluralization
            **kwargs: Variables to substitute

        Returns:
            Plural ized translation
        """
        # Try plural-specific key first
        if count == 0:
            plural_key = f"{key}.zero"
        elif count == 1:
            plural_key = f"{key}.one"
        else:
            plural_key = f"{key}.other"

        translation = self._get_from_language(self.current_language, plural_key)

        # Fallback to base key
        if translation is None:
            translation = self.get(key, **kwargs)
        else:
            # Add count to kwargs
            kwargs['count'] = count
            if kwargs:
                translation = translation.format(**kwargs)

        return translation

    def get_all_keys(self, language_code: Optional[str] = None) -> List[str]:
        """
        Get all translation keys for a language.

        Args:
            language_code: Language code (uses current if None)

        Returns:
            List of translation keys
        """
        if language_code is None:
            language_code = self.current_language

        if language_code not in self.translations:
            return []

        keys = []
        self._collect_keys(self.translations[language_code], "", keys)
        return keys

    def _collect_keys(self, data: Any, prefix: str, keys: List[str]):
        """Recursively collect all keys"""
        if isinstance(data, dict):
            for key, value in data.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    self._collect_keys(value, new_prefix, keys)
                else:
                    keys.append(new_prefix)

    def get_available_languages(self) -> List[str]:
        """Get list of available language codes"""
        return list(self.translations.keys())

    def get_language_name(self, language_code: str) -> str:
        """Get native name of language"""
        meta = self.metadata.get(language_code)
        if meta:
            return meta.language_name

        # Try to get from Language enum
        for lang in Language:
            if lang.code == language_code:
                return lang.native_name

        return language_code

    def get_completion(self, language_code: str) -> float:
        """Get translation completion percentage"""
        meta = self.metadata.get(language_code)
        if meta:
            return meta.completion_percent
        return 0.0


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_localizations: Dict[str, Localization] = {}


def get_localization(game_id: str) -> Localization:
    """Get localization instance for a game"""
    if game_id not in _localizations:
        _localizations[game_id] = Localization(game_id)
    return _localizations[game_id]


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def t(key: str, game_id: str = "global", **kwargs) -> str:
    """
    Translate a key (shorthand).

    Args:
        key: Translation key
        game_id: Game identifier
        **kwargs: Variables to substitute

    Returns:
        Translated string
    """
    loc = get_localization(game_id)
    return loc.get(key, **kwargs)


def tp(key: str, count: int, game_id: str = "global", **kwargs) -> str:
    """
    Translate with pluralization (shorthand).

    Args:
        key: Translation key
        count: Count for pluralization
        game_id: Game identifier
        **kwargs: Variables to substitute

    Returns:
        Pluralized translation
    """
    loc = get_localization(game_id)
    return loc.get_plural(key, count, **kwargs)


# =============================================================================
# TRANSLATION CREATOR
# =============================================================================

class TranslationCreator:
    """Helper to create new translations"""

    @staticmethod
    def create_template(
        game_id: str,
        language_code: str,
        language_name: str,
        author: str
    ):
        """
        Create a translation template.

        Args:
            game_id: Game identifier
            language_code: Language code (e.g., 'es')
            language_name: Language name (e.g., 'Español')
            author: Translator name
        """
        loc = get_localization(game_id)

        # Get all English keys
        english_keys = loc.get_all_keys('en')

        # Create template with English values
        template = {
            'metadata': {
                'language_code': language_code,
                'language_name': language_name,
                'version': '1.0',
                'author': author,
                'completion_percent': 0.0,
                'last_updated': '2025-01-01'
            },
            'translations': {}
        }

        # Build nested structure
        for key in english_keys:
            english_value = loc.get(key)
            parts = key.split('.')

            current = template['translations']
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    # Last part - set value with English as comment
                    current[part] = f"TODO: translate '{english_value}'"
                else:
                    # Intermediate part - create dict
                    if part not in current:
                        current[part] = {}
                    current = current[part]

        # Save template
        output_file = loc.localization_dir / f"{language_code}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)

        print(f"✅ Translation template created: {output_file}")
        print(f"   {len(english_keys)} strings to translate")


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Localization System Test")
    print("=" * 60)

    # Create localization
    loc = Localization('test_game')

    print(f"Current language: {loc.current_language}")
    print(f"Available languages: {loc.get_available_languages()}")

    # Test translations
    print(f"\nui.yes: {loc.get('ui.yes')}")
    print(f"ui.no: {loc.get('ui.no')}")
    print(f"msg.game_saved: {loc.get('msg.game_saved')}")

    # Test variable substitution
    greeting_key = 'greeting'
    loc.translations['en']['greeting'] = 'Hello, {name}!'
    print(f"\ngreeting: {loc.get('greeting', name='Alice')}")

    # Test pluralization
    loc.translations['en']['items'] = {
        'zero': 'No items',
        'one': '1 item',
        'other': '{count} items'
    }
    print(f"\nitems (0): {loc.get_plural('items', 0)}")
    print(f"items (1): {loc.get_plural('items', 1)}")
    print(f"items (5): {loc.get_plural('items', 5)}")

    # Create Spanish template
    print("\n" + "=" * 60)
    TranslationCreator.create_template(
        game_id='test_game',
        language_code='es',
        language_name='Español',
        author='Test Translator'
    )

    print("\n✅ Localization system test passed!")
