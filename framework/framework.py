from .scenes import SceneManager
import pygame
from typing import List, Optional, Tuple, Callable, Any
from decorator import decorator
from functools import partial
from dataclasses import dataclass


@dataclass
class EventMetadata:
    """Метаданные обработчиков событий"""
    type: int
    required_fields: dict
    use_event: bool


def is_primitive_type(value) -> bool:
    return not hasattr(value, '__dict__')


def event_handler(event_type: int, use_event=False, **event_data):
    """
        Декоратор, используемый для создания обработчиков событий.
        Аргументы:
            event_type: int - тип события
            use_event: bool - если True, то событие будет передано 
                обработчику в качестве аргумента
            **event_data - значения, которые должен иметь объект события
        Пример:
            @event_handler(pygame.KEYDOWN, key=pygame.K_ENTER)
            def on_enter(self):
                ...
            В данном случае обработчик будет вызван каждый раз, 
            когда просходит событие pygame.KEYDOWN с полем key 
            равным pygame.K_ENTER
    """
    def decorator(handler):
        metadata = EventMetadata(
            type=event_type,
            required_fields=event_data,
            use_event=use_event,
        )
        handler.__dict__['_handler_metadata'] = metadata
        return handler
    return decorator


def get_event_handlers(game_objects: List):
    """Возвращает обработчики событий из списка объектов"""
    for obj in game_objects:
        obj._event_handlers: Dict[int,
                                  List[Tuple[Callable, EventMetadata]]] = {}
        for name, value in obj.__class__.__dict__.items():
            if is_primitive_type(value):
                continue

            if '_handler_metadata' not in value.__dict__:
                continue

            metadata: Optional[EventMetadata] = value.__dict__.pop(
                '_handler_metadata')

            handler_function = partial(value, obj)
            handler = (handler_function, metadata)

            if metadata.type in obj._event_handlers:
                obj._event_handlers[metadata.type].append(handler)
            else:
                obj._event_handlers[metadata.type] = [handler]


def validate_required_fields(event, event_data: dict) -> bool:
    for key, value in event_data.items():
        if event.__dict__.get(key) != value:
            return False
    return True


def handle_events(scene):
    """Обработка событий"""
    if '_event_handlers' not in scene.__dict__:
        return
    handlers = scene._event_handlers
    for event in pygame.event.get():
        event_name = pygame.event.event_name(event.type)

        for handler, metadata in handlers.get(event.type, ()):
            if not validate_required_fields(event, metadata.required_fields):
                continue

            if metadata.use_event:
                handler(event)
            else:
                handler()

        if event.type == pygame.QUIT:
            running = False


def loop(scene_manager: SceneManager, screen: pygame.Surface, fps=60):
    """
        Главный цикл приложения.
        Аргументы:
            scene_manager - менеджер сцен отвечающий за работу с ними
            screen - экран, на котором будет рисоваться изображение
            fps - частота обновления экрана
    """
    clock = pygame.time.Clock()
    game_objects = scene_manager.get_game_objects()
    get_event_handlers(game_objects)
    running = True
    while running:
        screen.fill((255, 255, 255))

        if pygame.event.peek(pygame.QUIT):
            pygame.event.clear()
            running = False

        handle_events(scene_manager.current_scene)

        scene_manager.update()
        scene_manager.render(screen)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)
