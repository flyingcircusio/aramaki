from pyramid.config.actions import action_method as action_method
from pyramid.exceptions import ConfigurationError as ConfigurationError
from pyramid.interfaces import ILocaleNegotiator as ILocaleNegotiator, ITranslationDirectories as ITranslationDirectories
from pyramid.path import AssetResolver as AssetResolver

class I18NConfiguratorMixin:
    def set_locale_negotiator(self, negotiator) -> None: ...
    def add_translation_dirs(self, *specs, **kw) -> None: ...
