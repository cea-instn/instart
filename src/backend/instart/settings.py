"""
Django settings for instart-learning project.
"""
import json
import os

from django.utils.translation import ugettext_lazy as _

# pylint: disable=ungrouped-imports
import sentry_sdk
from configurations import Configuration, values
from sentry_sdk.integrations.django import DjangoIntegration

from richie.apps.courses.settings.mixins import RichieCoursesConfigurationMixin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join("/", "data")


def get_release():
    """Get current release of the application

    By release, we mean the release from the version.json file à la Mozilla [1]
    (if any). If this file has not been found, it defaults to "NA".

    [1]
    https://github.com/mozilla-services/Dockerflow/blob/master/docs/version_object.md
    """

    # Try to get the current release from the version.json file generated by the
    # CI during the Docker image build
    try:
        with open(os.path.join(BASE_DIR, "version.json")) as version:
            return json.load(version)["version"]
    except FileNotFoundError:
        pass

    # Default: not available
    return "NA"


class DRFMixin:
    """
    Django Rest Framework configuration mixin.
    NB: DRF picks its settings from the REST_FRAMEWORK namespace on the settings, hence
    the nesting of all our values inside that prop
    """

    REST_FRAMEWORK = {
        "ALLOWED_VERSIONS": ("1.0",),
        "DEFAULT_VERSION": "1.0",
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    }


class Base(DRFMixin, RichieCoursesConfigurationMixin, Configuration):
    """
    This is the base configuration every configuration (aka environnement) should inherit from. It
    is recommended to configure third-party applications by creating a configuration mixins in
    ./configurations and compose the Base configuration with those mixins.

    It depends on an environment variable that SHOULD be defined:

    * DJANGO_SECRET_KEY

    You may also want to override default configuration by setting the following environment
    variables:

    * DJANGO_SENTRY_DSN
    * RICHIE_ES_HOST
    * DB_NAME
    * DB_USER
    * DB_PASSWORD
    * DB_HOST
    * DB_PORT
    """

    DEBUG = False

    SITE_ID = 1

    # Security
    ALLOWED_HOSTS = []
    SECRET_KEY = values.Value(None)

    # Application definition
    ROOT_URLCONF = "instart.urls"
    WSGI_APPLICATION = "instart.wsgi.application"

    # Database
    DATABASES = {
        "default": {
            "ENGINE": values.Value(
                "django.db.backends.postgresql_psycopg2",
                environ_name="DB_ENGINE",
                environ_prefix=None,
            ),
            "NAME": values.Value(
                "instart", environ_name="DB_NAME", environ_prefix=None
            ),
            "USER": values.Value("instn", environ_name="DB_USER", environ_prefix=None),
            "PASSWORD": values.Value(
                "pass", environ_name="DB_PASSWORD", environ_prefix=None
            ),
            "HOST": values.Value(
                "localhost", environ_name="DB_HOST", environ_prefix=None
            ),
            "PORT": values.Value(5432, environ_name="DB_PORT", environ_prefix=None),
        }
    }
    MIGRATION_MODULES = {}

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(DATA_DIR, "media")
    STATIC_ROOT = os.path.join(DATA_DIR, "static")
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

    # Internationalization
    TIME_ZONE = "Europe/Paris"
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Templates
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "templates")],
            "OPTIONS": {
                "context_processors": [
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.template.context_processors.media",
                    "django.template.context_processors.csrf",
                    "django.template.context_processors.tz",
                    "sekizai.context_processors.sekizai",
                    "django.template.context_processors.static",
                    "cms.context_processors.cms_settings",
                    "richie.apps.core.context_processors.site_metas",
                ],
                "loaders": [
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ],
            },
        }
    ]

    CMS_TEMPLATES = (
        ("courses/cms/course_detail.html", _("Course page")),
        ("courses/cms/course_run_detail.html", _("Course run page")),
        ("courses/cms/organization_list.html", _("Organization list")),
        ("courses/cms/organization_detail.html", _("Organization page")),
        ("courses/cms/category_list.html", _("Category list")),
        ("courses/cms/category_detail.html", _("Category page")),
        ("courses/cms/blogpost_list.html", _("Blog post list")),
        ("courses/cms/blogpost_detail.html", _("Blog post page")),
        ("courses/cms/blogpost_detail_two_columns.html", _("Blog post page with two columns")),
        ("courses/cms/person_detail.html", _("Person page")),
        ("courses/cms/person_list.html", _("Person list")),
        ("search/search.html", _("Search")),
        ("richie/child_pages_list.html", _("List of child pages")),
        ("richie/homepage.html", _("Homepage")),
        ("richie/single_column.html", _("Single column")),
    )

    MIDDLEWARE = (
        "cms.middleware.utils.ApphookReloadMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "dockerflow.django.middleware.DockerflowMiddleware",
        "cms.middleware.user.CurrentUserMiddleware",
        "cms.middleware.page.CurrentPageMiddleware",
        "cms.middleware.toolbar.ToolbarMiddleware",
        "cms.middleware.language.LanguageCookieMiddleware",
    )

    INSTALLED_APPS = (
        # Django
        "djangocms_admin_style",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.admin",
        "django.contrib.sites",
        "django.contrib.sitemaps",
        "django.contrib.staticfiles",
        "django.contrib.messages",
        # Django-cms
        "cms",
        "menus",
        "sekizai",
        "treebeard",
        "djangocms_text_ckeditor",
        "filer",
        "easy_thumbnails",
        "djangocms_link",
        "djangocms_googlemap",
        "djangocms_video",
        "djangocms_picture",
        # Richie stuff
        "richie",
        "richie.apps.core",
        "richie.apps.courses",
        "richie.apps.search",
        "richie.plugins.html_sitemap",
        "richie.plugins.large_banner",
        "richie.plugins.plain_text",
        "richie.plugins.section",
        "richie.plugins.simple_picture",
        "richie.plugins.simple_text_ckeditor",
        # Third party apps
        "dockerflow.django",
        "parler",
        "rest_framework",
        "storages",
    )

    # Languages
    # - Django
    LANGUAGE_CODE = "en"

    # Careful! Languages should be ordered by priority, as this tuple is used to get
    # fallback/default languages throughout the app.
    # Use "en" as default as it is the language that is most likely to be spoken by any visitor
    # when their preferred language, whatever it is, is unavailable
    LANGUAGES = (("en", _("English")), ("fr", _("French")))

    # - Django CMS
    CMS_LANGUAGES = {
        "default": {
            "public": True,
            "hide_untranslated": False,
            "redirect_on_fallback": True,
            "fallbacks": ["en", "fr"],
        },
        1: [
            {
                "public": True,
                "code": "en",
                "hide_untranslated": False,
                "name": _("English"),
                "fallbacks": ["fr"],
                "redirect_on_fallback": True,
            },
            {
                "public": True,
                "code": "fr",
                "hide_untranslated": False,
                "name": _("French"),
                "fallbacks": ["en"],
                "redirect_on_fallback": True,
            },
        ],
    }

    # - Django Parler
    PARLER_LANGUAGES = CMS_LANGUAGES

    # Permisions
    # - Django CMS
    CMS_PERMISSION = True

    # - Django Filer
    FILER_ENABLE_PERMISSIONS = True
    FILER_IS_PUBLIC_DEFAULT = True

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "loggers": {
            "django.db.backends": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            }
        },
    }

    # Elasticsearch
    RICHIE_ES_HOST = values.Value(
        "elasticsearch", environ_name="RICHIE_ES_HOST", environ_prefix=None
    )

    @classmethod
    def post_setup(cls):
        """Post setup configuration.
        This is the place where you can configure settings that require other
        settings to be loaded.
        """
        super().post_setup()

        # The DJANGO_SENTRY_DSN environment variable should be set to activate
        # sentry for an environment
        sentry_dsn = values.Value(None, environ_name="SENTRY_DSN")
        if sentry_dsn is not None:
            sentry_sdk.init(
                dsn=sentry_dsn,
                environment=cls.__name__.lower(),
                release=get_release(),
                integrations=[DjangoIntegration()],
            )


class Development(Base):
    """
    Development environment settings

    We set DEBUG to True and configure the server to respond from all hosts.
    """

    DEBUG = True
    ALLOWED_HOSTS = ["*"]


class Test(Base):
    """Test environment settings"""


class ContinuousIntegration(Test):
    """
    Continous Integration environment settings

    nota bene: it should inherit from the Test environment.
    """


class Production(Base):
    """Production environment settings

    You must define the DJANGO_ALLOWED_HOSTS environment variable in Production
    configuration (and derived configurations):

    DJANGO_ALLOWED_HOSTS="foo.com,foo.fr"
    """

    # Security
    ALLOWED_HOSTS = values.ListValue(None)
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    # System check reference:
    # https://docs.djangoproject.com/en/2.2/ref/checks/#security
    SILENCED_SYSTEM_CHECKS = values.ListValue(
        [
            # Allow the X_FRAME_OPTIONS to be set to "SAMEORIGIN"
            "security.W019"
        ]
    )
    # The X_FRAME_OPTIONS value should be set to "SAMEORIGIN" to display
    # DjangoCMS frontend admin frames. Dockerflow raises a system check security
    # warning with this setting, one should add "security.W019" to the
    # SILENCED_SYSTEM_CHECKS setting (see above).
    X_FRAME_OPTIONS = "SAMEORIGIN"

    DEFAULT_FILE_STORAGE = "instart.storage.MediaStorage"

    # For static files in production, we want to use a backend that includes a hash in
    # the filename, that is calculated from the file content, so that browsers always
    # get the updated version of each file.
    STATICFILES_STORAGE = values.Value(
        "instart.storage.ConfigurableManifestS3Boto3Storage"
    )

    # The mapping between the names of the original files and the names of the files distributed
    # by the backend is stored in a file.
    # The best practice is to allow this manifest file's name to change for each deployment so
    # that several versions of the app can run in parallel without interfering with each other.
    # We make it configurable so that it can be versioned with a deployment stamp in our CI/CD:
    STATICFILES_MANIFEST_NAME = values.Value("staticfiles.json")

    AWS_ACCESS_KEY_ID = values.SecretValue()
    AWS_SECRET_ACCESS_KEY = values.SecretValue()

    AWS_S3_OBJECT_PARAMETERS = {
        "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
        "CacheControl": "max-age=94608000",
    }
    AWS_S3_REGION_NAME = values.Value("eu-west-1")

    AWS_STATIC_BUCKET_NAME = values.Value("production-instart-static")
    AWS_MEDIA_BUCKET_NAME = values.Value("production-instart-media")

    AWS_CLOUDFRONT_DOMAIN = values.Value()

    @property
    def CDN_DOMAIN(self):
        """CDN_DOMAIN is used to load frontend built chunks; it should match the AWS CloudFront
        domain used as a CDN. As other configurations will inherit from this setting, it should
        be lazily evaluated via the @property pattern."""
        return self.AWS_CLOUDFRONT_DOMAIN


class Feature(Production):
    """
    Feature environment settings

    nota bene: it should inherit from the Production environment.
    """

    AWS_STATIC_BUCKET_NAME = values.Value("feature-instart-static")
    AWS_MEDIA_BUCKET_NAME = values.Value("feature-instart-media")


class Staging(Production):
    """
    Staging environment settings

    nota bene: it should inherit from the Production environment.
    """

    AWS_STATIC_BUCKET_NAME = values.Value("staging-instart-static")
    AWS_MEDIA_BUCKET_NAME = values.Value("staging-instart-media")


class PreProduction(Production):
    """
    Pre-production environment settings

    nota bene: it should inherit from the Production environment.
    """

    AWS_STATIC_BUCKET_NAME = values.Value("preprod-instart-static")
    AWS_MEDIA_BUCKET_NAME = values.Value("preprod-instart-media")
