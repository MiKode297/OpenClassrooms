from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SnippetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "appz.snippets"
    verbose_name = _("Snippets")
