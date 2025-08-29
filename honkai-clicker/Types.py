import enum


class TaskType(enum.Enum):
    """
    Тип задания
    """
    DECORATION_EXTRACTION = 1  # Извлечение украшений (TODO: Реализовать)
    SEPAL_GOLD = 2             # Золотой чашелист
    SEPAL_CRIMSON = 3          # Багровый чашелист (TODO: Реализовать)
    STAGNANT_SHADOW = 4        # Застойная тень (TODO: Реализовать)
    CORROSION_CAVE = 5         # Пещера коррозии
    ECHO_OF_WAR = 6            # Эхо войны (TODO: Реализовать)
    VIRTUAL_UNIVERSE = 7       # Виртуальная вселенная (TODO: Реализовать)
    ASSIGNMENTS = 8            # Сбор и повтор поручений
    NAMELESS_HONOR = 9         # Получение наград миссий чести безымянных
    SUPPORT_COLLECTION = 10    # Получение наград поддержки (TODO: Реализовать)
    AWARDS_COLLECTION = 11     # Получение наград ежедневной тренировки


class BaseMaterial(enum.Enum):
    """
    Базовые материалы
    """
    MEMORIES_BUD = 1  # Бутон воспоминаний (опыт для персонажа)
    ETHER_BUD = 2     # Бутон эфира (опыт для конуса)
    TREASURE_BUD = 3  # Бутон сокровищ (деньги)


class TraceMaterial(enum.Enum):
    """
    Материал следов
    """
    HARMONY_A = 1       # Гармония
    HARMONY_B = 2
    DESTRUCTION_A = 3   # Разрушение
    DESTRUCTION_B = 4
    PRESERVATION_A = 5  # Сохранение
    PRESERVATION_B = 6
    HUNT_A = 7          # Охота
    HUNT_B = 8
    ABUNDANCE_A = 9     # Изобилие
    ABUNDANCE_B = 10
    ERUDITION_A = 11    # Эрудиция
    ERUDITION_B = 12
    OBLIVION_A = 13     # Небытие
    OBLIVION_B = 14
    MEMORY_A = 15       # Память


class CharacterMaterial(enum.Enum):
    """
    Материал возвышения персонажа
    """
    NONE = 0


class PlanetaryDecorationChallenge(enum.Enum):
    """
    Испытания извлечения планетарных украшений
    """
    CONTINUOUS_WALLS = 1    # Непрерывные стены
    MOLTEN_CORE = 2         # Расплавленный сердечник
    GENTLE_SPEECHES = 3     # Нежные речи
    PERMAFROST = 4          # Вечная мерзлота
    EVIL_FRUIT = 5          # Плод зла
    BLADES_RAIN = 6         # Дождь клинков
    SLEEPING_TOGETHER = 7   # Совместный сон
    INCESSANT_COMEDY = 8    # Непрекращающаяся комедия
    INCESSANT_STRIFE = 9    # Беспрестанный надзор
    SUBLUNARY_CRIMSON = 10  # Подлунный багрянец
    HUNGRY_OFFICIAL = 11    # Голодный чиновник


class CorrosionCaveChallenge(enum.Enum):
    """
    Испытания реликвий
    """
    ICY_WIND_PATH = 1                   # Путь ледяного ветра
    FAST_FIST_PATH = 2                  # Путь быстрого кулака
    WANDERING_PATH = 3                  # Путь скитаний
    PROVIDENCE_PATH = 4                 # Путь провидения
    SACRED_HYMN_PATH = 5                # Путь священного гимна
    RAGING_FLAMES_PATH = 6              # Путь бушующего пламени
    ELIXIR_SEEKERS_PATH = 7             # Путь искателей эликсира
    DARKNESS_PATH = 8                   # Путь тьмы
    FALLING_ASLEEP_PATH = 9             # Путь погружения в сон
    CAVALRYMAN_PATH = 10                # Путь кавалериста
    SINGING_TO_ACCOMPANIMENT_PATH = 11  # Путь пения под аккомпанемент
    THUNDERCLAP_PATH = 12               # Путь раската грома
    DELUSION_PATH = 13                  # Путь заблуждения


class EchoOfWarChallenge(enum.Enum):
    """
    Боссы эха войны
    """
    DESTRUCTION_BEGINNING = 1    # НАЧАЛО РАЗРУШЕНИЯ
    PERMAFROST_END = 2           # КОНЕЦ ВЕЧНОЙ МЕРЗЛОТЫ
    IMMORTALITY_SEED = 3         # СЕМЯ БЕССМЕРТИЯ
    OLD_WORMHOLE_NIGHTMARES = 4  #
    MORTAL_DREAMS = 5            #
    INNER_BEAST = 6              #
    TWILIGHT_LOOK = 7            #
