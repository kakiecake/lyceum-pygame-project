import pygame
from typing import List
from decorator import decorator
from functools import partial


def is_primitive_type(value) -> bool:
    return not hasattr(value, '__dict__')


def event_handler(event_type: int, use_event=False, **event_data):
    def decorator(handler):
        handler.__dict__['_handler_metadata'] = {
            "type": event_type,
            "data": event_data,
            "use_event": use_event
        }
        return handler
    return decorator


def get_event_handlers(game_objects: List):
    handlers = {}
    for obj in game_objects:
        for name, value in obj.__class__.__dict__.items():
            if is_primitive_type(value):
                continue

            metadata = value.__dict__.get('_handler_metadata')
            if not metadata:
                continue

            handler_function = partial(value, obj)
            handler = (handler_function, metadata)

            if metadata["type"] in handlers:
                handlers[metadata["type"]].append(handler)
            else:
                handlers[metadata["type"]] = [handler]
    return handlers


def valid_event_data(event, event_data: dict) -> bool:
    for key, value in event_data.items():
        if event.__dict__.get(key) != value:
            return False
    return True


def main(game_objects: List):
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    FPS = 30
    clock = pygame.time.Clock()

    event_handlers = get_event_handlers(game_objects)

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            event_name = pygame.event.event_name(event.type)

            for handler, metadata in event_handlers.get(event.type, ()):
                if not valid_event_data(event, metadata["data"]):
                    continue

                if metadata['use_event']:
                    handler(event)
                else:
                    handler()

            if event.type == pygame.QUIT:
                running = False

        for obj in game_objects:
            obj.render(screen)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(FPS)
