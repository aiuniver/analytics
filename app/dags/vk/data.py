from enum import Enum
from datetime import datetime
from typing import Tuple, List, Dict, Any, Optional
from pydantic import (
    BaseModel,
    PositiveInt,
    PositiveFloat,
    NonNegativeInt,
    NonNegativeFloat,
)


class DatatypeTitleEnum(Enum):
    URL = "Ссылка"
    String = "Строковое значение"
    Date = "Дата в формате %Y-%m-%d"
    Time = "Время в формате %H:%M:%S"
    Datetime = "Дата и время в формате %Y-%m-%d %H:%M:%S"
    Rate = "Доля в процентах"
    Anchor = "Ссылка на ячейку"
    AnchorList = "Список ссылок на ячейки"
    Integer = "Целое число"
    PositiveInteger = "Натуральное число"
    NonNegativeInteger = "Неотрицательное целое число"
    Float = "Float"
    PositiveFloat = "PositiveFloat"
    NonNegativeFloat = "NonNegativeFloat"


class DatatypeEnum(Enum):
    URL = "URL"
    String = "String"
    Date = "Date"
    Time = "Time"
    Datetime = "Datetime"
    Rate = "Rate"
    Anchor = "Anchor"
    AnchorList = "AnchorList"
    Integer = "Integer"
    PositiveInteger = "PositiveInteger"
    NonNegativeInteger = "NonNegativeInteger"
    Float = "Float"
    PositiveFloat = "PositiveFloat"
    NonNegativeFloat = "NonNegativeFloat"

    @property
    def title(self) -> str:
        return DatatypeTitleEnum[self.name].value

    @classmethod
    def table_data(cls) -> List[Tuple[str, str]]:
        return [("Название", "Описание")] + list(
            map(lambda item: (item.name, item.title), cls)
        )

    @classmethod
    def table_indexes(cls) -> Dict[str, int]:
        return dict((item.name, index + 2) for index, item in enumerate(cls))


class AccountAccessRoleTitleEnum(Enum):
    admin = "Главный администратор"
    manager = "Администратор"
    reports = "Наблюдатель"


class AccountAccessRoleEnum(Enum):
    admin = "admin"
    manager = "manager"
    reports = "reports"

    @property
    def title(self) -> str:
        return AccountAccessRoleTitleEnum[self.name].value


class AccountStatusTitleEnum(Enum):
    _1 = "Активен"
    _0 = "Неактивен"


class AccountStatusEnum(Enum):
    _1 = 1
    _0 = 0

    @property
    def title(self) -> str:
        return AccountStatusTitleEnum[self.name].value


class AccountTypeTitleEnum(Enum):
    general = "Обычный"
    agency = "Агентский"


class AccountTypeEnum(Enum):
    general = "general"
    agency = "agency"

    @property
    def title(self) -> str:
        return AccountTypeTitleEnum[self.name].value


class CampaignTypeTitleEnum(Enum):
    normal = "Обычная кампания, в которой можно создавать любые объявления, кроме описанных в следующих пунктах"
    vk_apps_managed = "Кампания, в которой можно рекламировать только администрируемые Вами приложения и у которой есть отдельный бюджет"
    mobile_apps = "Кампания, в которой можно рекламировать только мобильные приложения"
    promoted_posts = (
        "Кампания, в которой можно рекламировать только записи в сообществе"
    )
    adaptive_ads = (
        "Кампания, в которой можно рекламировать только объявления адаптивного формата"
    )
    stories = "Stories"


class CampaignTypeEnum(Enum):
    normal = "normal"
    vk_apps_managed = "vk_apps_managed"
    mobile_apps = "mobile_apps"
    promoted_posts = "promoted_posts"
    adaptive_ads = "adaptive_ads"
    stories = "stories"

    @property
    def title(self) -> str:
        return CampaignTypeTitleEnum[self.name].value


class CampaignStatusTitleEnum(Enum):
    _0 = "кампания остановлена"
    _1 = "кампания запущена"
    _2 = "кампания удалена"


class CampaignStatusEnum(Enum):
    _0 = 0
    _1 = 1
    _2 = 2

    @property
    def title(self) -> str:
        return CampaignStatusTitleEnum[self.name].value


class CampaignCostTypeTitleEnum(Enum):
    _0 = "Оплата за переходы"
    _1 = "Оплата за показы (включая цель «Максимум показов»)"
    _3 = "Оптимизированная оплата за показы"


class CampaignCostTypeEnum(Enum):
    _0 = 0
    _1 = 1
    _3 = 3

    @property
    def title(self) -> str:
        return CampaignCostTypeTitleEnum[self.name].value


class CampaignAdFormatTitleEnum(Enum):
    _1 = "Изображение и текст"
    _2 = "Большое изображение"
    _4 = "Продвижение сообществ или приложений, квадратное изображение"
    _8 = "Специальный формат сообществ"
    _9 = "Запись в сообществе"
    _11 = "Адаптивный формат"


class CampaignAdFormatEnum(Enum):
    _1 = 1
    _2 = 2
    _4 = 4
    _8 = 8
    _9 = 9
    _11 = 11

    @property
    def title(self) -> str:
        return CampaignAdFormatTitleEnum[self.name].value


class AdFormatTitleEnum(Enum):
    _1 = "Изображение и текст"
    _2 = "Большое изображение"
    _3 = "Эксклюзивный формат"
    _4 = "Продвижение сообществ или приложений, квадратное изображение"
    _5 = "Приложение в новостной ленте(устаревший)"
    _6 = "Мобильное приложение"
    _7 = "Специальный формат приложений"
    _8 = "Специальный формат сообществ"
    _9 = "Запись в сообществе"
    _10 = "Витрина приложений"
    _11 = "Адаптивный формат"
    _12 = "Истории"


class AdFormatEnum(Enum):
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
    _11 = 11
    _12 = 12

    @property
    def title(self) -> str:
        return AdFormatTitleEnum[self.name].value


class AdCostTypeTitleEnum(Enum):
    _0 = "Оплата за переходы"
    _1 = "Оплата за показы"
    _3 = "Оптимизированная оплата за показы"


class AdCostTypeEnum(Enum):
    _0 = 0
    _1 = 1
    _3 = 3

    @property
    def title(self) -> str:
        return AdCostTypeTitleEnum[self.name].value


class AdGoalTypeTitleEnum(Enum):
    _1 = "Показы"
    _2 = "Переходы"
    _3 = "Отправка заявок"
    _5 = "Вступления в сообщество"
    _6 = "Добавление в корзину"
    _7 = "Добавление в список желаний"
    _8 = "Уточнение сведений"
    _9 = "Начало оформления заказа"
    _10 = "Добавление платёжной информации"
    _11 = "Покупка"
    _12 = "Контакт"
    _13 = "Получение потенциального клиента"
    _14 = "Запись на приём"
    _15 = "Регистрация"
    _16 = "Подача заявки"
    _17 = "Использование пробной версии"
    _18 = "Оформление подписки"
    _19 = "Посещение страницы"
    _20 = "Просмотр контента"
    _21 = "Использование поиска"
    _22 = "Поиск местонахождения"
    _23 = "Пожертвование средств"
    _24 = "Конверсия"


class AdGoalTypeEnum(Enum):
    _1 = 1
    _2 = 2
    _3 = 3
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
    _11 = 11
    _12 = 12
    _13 = 13
    _14 = 14
    _15 = 15
    _16 = 16
    _17 = 17
    _18 = 18
    _19 = 19
    _20 = 20
    _21 = 21
    _22 = 22
    _23 = 23
    _24 = 24

    @property
    def title(self) -> str:
        return AdGoalTypeTitleEnum[self.name].value


class AdPlatformTitleEnum(Enum):
    _0 = "ВКонтакте и сайты-партнёры"
    _1 = "Только ВКонтакте"
    all = "Все площадки"
    desktop = "Полная версия сайта"
    mobile = "Мобильный сайт и приложения"
    stories = "Stories"


class AdPlatformEnum(Enum):
    _0 = 0
    _1 = 1
    all = "all"
    desktop = "desktop"
    mobile = "mobile"
    stories = "stories"

    @property
    def title(self) -> str:
        return AdPlatformTitleEnum[self.name].value


class AdPublisherPlatformsTitleEnum(Enum):
    all = "Все площадки (по умолчанию)"
    social = "Все соцсети (ВКонтакте и Одноклассники)"
    vk = "Только ВКонтакте"


class AdPublisherPlatformsEnum(Enum):
    all = "all"
    social = "social"
    vk = "vk"

    @property
    def title(self) -> str:
        return AdPublisherPlatformsTitleEnum[self.name].value


class AdAutobiddingTitleEnum(Enum):
    _0 = "Выключено"
    _1 = "Включено (только для целей «Максимум показов» и «Максимум переходов»)"


class AdAutobiddingEnum(Enum):
    _0 = 0
    _1 = 1

    @property
    def title(self) -> str:
        return AdAutobiddingTitleEnum[self.name].value


class AdStatusTitleEnum(Enum):
    _0 = "Объявление остановлено"
    _1 = "Объявление запущено"
    _2 = "Объявление удалено"


class AdStatusEnum(Enum):
    _0 = 0
    _1 = 1
    _2 = 2

    @property
    def title(self) -> str:
        return AdStatusTitleEnum[self.name].value


class AdApprovedTitleEnum(Enum):
    _0 = "Объявление не проходило модерацию"
    _1 = "Объявление ожидает модерации"
    _2 = "Объявление одобрено"
    _3 = "Объявление отклонено"


class AdApprovedEnum(Enum):
    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3

    @property
    def title(self) -> str:
        return AdApprovedTitleEnum[self.name].value


class AdEventsRetargetingGroupsTitleEnum(Enum):
    _1 = "Просмотр промопоста"
    _2 = "Переход по ссылке или переход в сообщество"
    _3 = "Переход в сообщество"
    _4 = "Подписка на сообщество"
    _5 = "Отписка от новостей сообщества"
    _6 = "Скрытие или жалоба"
    _10 = "Запуск видео"
    _11 = "Досмотр видео до 3с"
    _12 = "Досмотр видео до 25%"
    _13 = "Досмотр видео до 50%"
    _14 = "Досмотр видео до 75%"
    _15 = "Досмотр видео до 100%"
    _20 = "Лайк продвигаемой записи"
    _21 = "Репост продвигаемой записи"
    _22 = "Неизвестно"
    _23 = "Неизвестно"
    _24 = "Неизвестно"
    _25 = "Неизвестно"
    _26 = "Неизвестно"


class AdEventsRetargetingGroupsEnum(Enum):
    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _10 = 10
    _11 = 11
    _12 = 12
    _13 = 13
    _14 = 14
    _15 = 15
    _20 = 20
    _21 = 21
    _22 = 22
    _23 = 23
    _24 = 24
    _25 = 25
    _26 = 26

    @property
    def title(self) -> str:
        return AdEventsRetargetingGroupsTitleEnum[self.name].value


class AdRepeatVideoTitleEnum(Enum):
    _0 = "Не зацикливать видео"
    _1 = "Зацикливать видео"


class AdRepeatVideoEnum(Enum):
    _0 = 0
    _1 = 1

    @property
    def title(self) -> str:
        return AdRepeatVideoTitleEnum[self.name].value


class AdLinkButtonTitleEnum(Enum):
    _open_url = "Перейти"
    _open = "Открыть"
    _more = "Подробнее"
    _call = "Позвонить"
    _book = "Забронировать"
    _enroll = "Записаться"
    _register = "Зарегистрироваться"
    _buy = "Купить"
    _buy_ticket = "Купить билет"
    _to_shop = "В магазин"
    _install = "Установить"
    _fill = "Заполнить"
    _order = "Заказать"
    _create = "Создать"
    _contact = "Связаться"
    _choose = "Выбрать"
    _try = "Попробовать"
    _begin = "Начать"
    _get = "Получить"
    _listen = "Слушать"
    _learn = "Узнать"


class AdLinkButtonEnum(Enum):
    _open_url = "open_url"
    _open = "open"
    _more = "more"
    _call = "call"
    _book = "book"
    _enroll = "enroll"
    _register = "register"
    _buy = "buy"
    _buy_ticket = "buy_ticket"
    _to_shop = "to_shop"
    _install = "install"
    _fill = "fill"
    _order = "order"
    _create = "create"
    _contact = "contact"
    _choose = "choose"
    _try = "try"
    _begin = "begin"
    _get = "get"
    _listen = "listen"
    _learn = "learn"

    @property
    def title(self) -> str:
        return AdLinkButtonTitleEnum[self.name].value


class StatisticsIdsTypeTitleEnum(Enum):
    ad = "Объявления"
    campaign = "Кампании"
    client = "Клиенты"
    office = "Кабинет"


class StatisticsIdsTypeEnum(Enum):
    ad = "ad"
    campaign = "campaign"
    client = "client"
    office = "office"

    @property
    def title(self) -> str:
        return StatisticsIdsTypeTitleEnum[self.name].value


class SexTitleEnum(Enum):
    _0 = "Любой"
    _1 = "Женский"
    _2 = "Мужской"


class SexEnum(Enum):
    _0 = 0
    _1 = 1
    _2 = 2

    @property
    def title(self) -> str:
        return SexTitleEnum[self.name].value


class BirthdayTitleEnum(Enum):
    _1 = "Сегодня"
    _2 = "Завтра"
    _4 = "В течение недели"


class BirthdayEnum(Enum):
    _1 = 1
    _2 = 2
    _4 = 4

    @property
    def title(self) -> str:
        return BirthdayTitleEnum[self.name].value


class FamilyStatusTitleEnum(Enum):
    _1 = "Не женат или не замужем"
    _2 = "Есть подруга или есть друг"
    _3 = "Помолвлен(а)"
    _4 = "Женат или замужем"
    _5 = "Все сложно"
    _6 = "В активном поиске"
    _7 = "Влюблен(а)"
    _8 = "В гражданском браке"


class FamilyStatusEnum(Enum):
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8

    @property
    def title(self) -> str:
        return FamilyStatusTitleEnum[self.name].value


class AccountData(BaseModel):
    access_role: AccountAccessRoleEnum
    account_id: PositiveInt
    account_status: AccountStatusEnum
    account_type: AccountTypeEnum
    account_name: str
    can_view_budget: bool
    ad_network_allowed_potentially: bool


class ClientData(BaseModel):
    account_id: PositiveInt
    id: PositiveInt
    name: str
    day_limit: NonNegativeInt
    all_limit: NonNegativeInt


class CampaignData(BaseModel):
    account_id: PositiveInt
    client_id: Optional[PositiveInt]
    id: PositiveInt
    type: CampaignTypeEnum
    name: str
    status: CampaignStatusEnum
    day_limit: NonNegativeInt
    all_limit: NonNegativeInt
    start_time: NonNegativeInt
    stop_time: NonNegativeInt


class TargetGroupData(BaseModel):
    account_id: PositiveInt
    client_id: Optional[PositiveInt]
    id: PositiveInt
    name: str
    last_updated: NonNegativeInt
    is_audience: PositiveInt
    is_shared: NonNegativeInt
    audience_count: NonNegativeInt
    lifetime: NonNegativeInt
    file_source: NonNegativeInt
    api_source: NonNegativeInt
    lookalike_source: NonNegativeInt
    pixel: Optional[str]
    domain: Optional[str]


class AdData(BaseModel):
    id: PositiveInt
    account_id: PositiveInt
    client_id: Optional[PositiveInt]
    campaign_id: PositiveInt
    ad_format: AdFormatEnum
    cost_type: AdCostTypeEnum
    cpc: Optional[PositiveInt]
    cpm: Optional[PositiveInt]
    ocpm: Optional[PositiveInt]
    goal_type: AdGoalTypeEnum
    impressions_limit: Optional[PositiveInt]
    impressions_limited: Optional[PositiveInt]
    ad_platform: Optional[AdPlatformEnum]
    ad_platform_no_wall: Optional[PositiveInt]
    ad_platform_no_ad_network: Optional[PositiveInt]
    publisher_platforms: Optional[AdPublisherPlatformsEnum]
    all_limit: NonNegativeInt
    day_limit: NonNegativeInt
    autobidding: Optional[AdAutobiddingEnum]
    autobidding_max_cost: Optional[PositiveInt]
    category1_id: PositiveInt
    category2_id: NonNegativeInt
    status: AdStatusEnum
    name: str
    approved: AdApprovedEnum
    video: Optional[PositiveInt]
    disclaimer_medical: Optional[PositiveInt]
    disclaimer_specialist: Optional[PositiveInt]
    disclaimer_supplements: Optional[PositiveInt]
    weekly_schedule_hours: List[str] = []
    weekly_schedule_use_holidays: Optional[bool]
    events_retargeting_groups: Dict[PositiveInt, List[AdEventsRetargetingGroupsEnum]]


class AdLayoutData(BaseModel):
    id: PositiveInt
    repeat_video: Optional[AdRepeatVideoEnum]
    title: str
    description: Optional[str]
    link_url: str
    link_domain: str
    link_title: Optional[str]
    link_button: Optional[AdLinkButtonEnum]
    image_src: str
    image_src_2x: Optional[str]
    icon_src: Optional[str]
    icon_src_2x: Optional[str]


class AdTargetingData(BaseModel):
    id: Optional[PositiveInt]
    sex: Optional[SexEnum]
    age_from: NonNegativeInt = 0
    age_to: NonNegativeInt = 0
    birthday: NonNegativeInt = 0
    country: NonNegativeInt = 0
    cities: List[int] = []
    cities_not: List[int] = []
    statuses: List[FamilyStatusEnum] = []
    groups: List[int] = []
    groups_not: List[int] = []
    apps: List[int] = []
    apps_not: List[int] = []
    districts: List[int] = []
    stations: List[int] = []
    streets: List[int] = []
    schools: List[int] = []
    positions: List[int] = []
    religions: List[int] = []
    interest_categories: List[int] = []
    interests: List[int] = []
    user_devices: List[int] = []
    user_os: List[int] = []
    user_browsers: List[int] = []
    retargeting_groups: List[int] = []
    retargeting_groups_not: List[int] = []
    count: NonNegativeInt = 0


class DemographicBaseData(BaseModel):
    impressions_rate: NonNegativeFloat = 0
    clicks_rate: NonNegativeFloat = 0


class DemographicSexBaseData(DemographicBaseData):
    pass


class DemographicAgeBaseData(DemographicBaseData):
    pass


# class DemographicCitiesBaseData(DemographicBaseData):
#     name: str


class DemographicSexData(BaseModel):
    m: DemographicSexBaseData = DemographicSexBaseData()
    f: DemographicSexBaseData = DemographicSexBaseData()


class DemographicAgeData(BaseModel):
    id_12_18: DemographicAgeBaseData = DemographicAgeBaseData()
    id_18_21: DemographicAgeBaseData = DemographicAgeBaseData()
    id_21_24: DemographicAgeBaseData = DemographicAgeBaseData()
    id_24_27: DemographicAgeBaseData = DemographicAgeBaseData()
    id_27_30: DemographicAgeBaseData = DemographicAgeBaseData()
    id_30_35: DemographicAgeBaseData = DemographicAgeBaseData()
    id_35_45: DemographicAgeBaseData = DemographicAgeBaseData()
    id_45_100: DemographicAgeBaseData = DemographicAgeBaseData()


# class DemographicCitiesData(DemographicCitiesBaseData):
#     pass


class DemographicData(BaseModel):
    id: PositiveInt
    date: datetime
    sex: DemographicSexData = DemographicSexData()
    age: DemographicAgeData = DemographicAgeData()
    # cities: Dict[str, DemographicCitiesData] = {}


class StatisticData(BaseModel):
    id: PositiveInt
    date: datetime
    account_id: PositiveInt
    client_id: Optional[PositiveInt]
    campaign_id: PositiveInt
    spent: Optional[PositiveFloat]
    impressions: Optional[PositiveInt]
    clicks: Optional[PositiveInt]
    ctr: NonNegativeFloat
    effective_cost_per_click: Optional[PositiveFloat]
    effective_cost_per_mille: Optional[PositiveFloat]
    effective_cpf: Optional[PositiveFloat]
    effective_cost_per_message: Optional[PositiveFloat]
    message_sends: Optional[PositiveFloat]


class WallPostData(BaseModel):
    ad_id: PositiveInt
    id: PositiveInt = 1
    owner_id: int = 1
    from_id: int = 1
    date: PositiveInt = 1
    title: str = ""
    text: str = ""
    image: str = ""
    target_url: str = ""
    attachments: List[Dict[str, Any]] = []


class PositionsData(BaseModel):
    id: PositiveInt
    name: str


class InterestCategoriesV2Data(BaseModel):
    id: PositiveInt
    name: str


class CountryData(BaseModel):
    id: PositiveInt
    name: str


class CityData(BaseModel):
    id: PositiveInt
    name: str
