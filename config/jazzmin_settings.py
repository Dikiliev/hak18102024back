
LOGO_PATH = 'admin_logo.svg'

SETTINGS = {
    'show_ui_builder': True,

    "site_title": "Админ Панель Estech",
    "site_header": "Estech",
    "site_brand": "Estech PC",

    "welcome_sign": "Добро пожаловать в Админ панель Estech",

    # Логотип для вашего сайта, должен быть доступен в статических файлах, используется для бренда в верхнем левом углу
    "site_logo": LOGO_PATH,

    # Логотип для вашего сайта, должен быть доступен в статических файлах, используется для логотипа формы входа (по умолчанию используется site_logo)
    "login_logo": LOGO_PATH,

    # Логотип для формы входа в темных темах (по умолчанию используется login_logo)
    # "login_logo_dark": None,

    # CSS классы, применяемые к логотипу выше
    "site_logo_classes": "custom-logo",
    "custom_css": "css/custom_admin.css",

    # Относительный путь к фавикону для вашего сайта
    "site_icon": LOGO_PATH,

    # Авторское право внизу страницы
    "copyright": "Acme Dashboard Ltd",

    # Список моделей админки для поиска из строки поиска, строка поиска будет отсутствовать, если исключена
    # Если вы хотите использовать одно поисковое поле, вам не нужно использовать список, вы можете использовать простую строку
    "search_model": ["auth.User", "auth.Group"],

    # Имя поля в модели пользователя, которое содержит аватар (ImageField/URLField/CharField) или вызываемую функцию, которая получает пользователя
    "user_avatar": None,

    ############
    # Верхнее меню #
    ############

    # Ссылки для размещения в верхнем меню
    "topmenu_links": [

        # URL, который будет обратным (могут быть добавлены разрешения)
        {"name": "Главная",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # Внешний URL, который открывается в новом окне (могут быть добавлены разрешения)
        {"name": "Поддержка", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # Админка модели для ссылки (права доступа проверяются относительно модели)
        {"model": "auth.User"},

        # Приложение с выпадающим меню ко всем страницам его моделей (права доступа проверяются относительно моделей)
        {"app": "main"},
    ],

    #############
    # Меню пользователя #
    #############

    # Дополнительные ссылки для включения в меню пользователя в правом верхнем углу ("app" URL типа не разрешен)
    "usermenu_links": [
        {"name": "Поддержка", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],

    #############
    # Боковое меню #
    #############

    # Показывать боковое меню
    "show_sidebar": True,

    # Автоматически развернуть меню
    "navigation_expanded": True,

    # Скрыть эти приложения при генерации бокового меню, например (auth)
    "hide_apps": [],

    # Скрыть эти модели при генерации бокового меню, например (auth.user)
    "hide_models": [],

    #################
    # Связанное модальное окно #
    #################

    # Использовать модальные окна вместо всплывающих окон
    "related_modal_active": False,

    #############
    # Настройки интерфейса #
    #############

    # Использовать ли шрифты с fonts.googleapis.com (используйте custom_css для предоставления шрифтов иначе)
    "use_google_fonts_cdn": True,

    ###############
    # Изменить вид #
    ###############

    # Отображать вид изменения как одну форму или в виде вкладок, текущие варианты:
    # - single
    # - horizontal_tabs (по умолчанию)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",


    # Добавить выбор языка в админку
    "language_chooser": False,
}

UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-navy",
    "navbar": "navbar-gray-dark navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}