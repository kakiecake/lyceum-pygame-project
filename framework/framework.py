import pygame
from typing import List, Optional, Tuple, Callable
from decorator import decorator
from functools import partial
from dataclasses import dataclass


@dataclass
class EventMetadata:
    type: int
    required_fields: dict
    use_event: bool


def is_primitive_type(value) -> bool:
    return not hasattr(value, '__dict__')


def event_handler(event_type: int, use_event=False, **event_data):
    def decorator(handler):
        metadata = EventMetadata(
            type=event_type, required_fields=event_data, use_event=use_event)
        handler.__dict__['_handler_metadata'] = metadata
        return handler
    return decorator


def get_event_handlers(game_objects: List):
    handlers: Dict[int, List[Tuple[Callable, EventMetadata]]] = {}
    for obj in game_objects:
        for name, value in obj.__class__.__dict__.items():
            if is_primitive_type(value):
                continue

            metadata: Optional[EventMetadata] = value.__dict__.get(
                '_handler_metadata')
            if metadata is None:
                continue

            handler_function = partial(value, obj)
            handler = (handler_function, metadata)

            if metadata.type in handlers:
                handlers[metadata.type].append(handler)
            else:
                handlers[metadata.type] = [handler]
    return handlers


def validate_required_fields(event, event_data: dict) -> bool:
    for key, value in event_data.items():
        if event.__dict__.get(key) != value:
            return False
    return True


def handle_events(handlers):
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


def loop(game_objects: List, screen: pygame.Surface, fps=60):
    clock = pygame.time.Clock()
    event_handlers = get_event_handlers(game_objects)
    running = True
    while running:
        screen.fill((255, 255, 255))

        if pygame.event.peek(pygame.QUIT):
            pygame.event.clear()
            running = False

        handle_events(event_handlers)

        for obj in game_objects:
            obj.render(screen)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)


def main(game_objects: List):
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    loop(game_objects, screen)
