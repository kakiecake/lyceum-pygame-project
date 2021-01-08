from typing import Dict, List


class SceneManager:
    def __init__(self, scenes={}):
        self.current_scene = None
        self.scenes = scenes

    def add_scene(self, key: str, scene):
        self.scenes[key] = scene

    def switch_to(self, scene_name: str):
        self.current_scene = self.scenes.get(scene_name)

    def get_game_objects(self) -> List:
        return list(self.scenes.values())

    def render(self, screen):
        if self.current_scene is not None:
            self.current_scene.render(screen)

    def update(self):
        if self.current_scene is not None:
            self.current_scene.update()
