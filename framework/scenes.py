from typing import Dict, List


class Scene:
    scene_data = {}

    def show(self):
        pass


class SceneManager:
    def __init__(self, scenes: Dict[str, Scene] = {}, data={}):
        self.current_scene = None
        self.scenes = scenes
        self.data = data
        for scene in self.scenes:
            scene.scene_data = self.data

    def add_scene(self, key: str, scene: Scene):
        self.scenes[key] = scene
        scene.scene_data = self.data

    def switch_to(self, scene_name: str):
        self.current_scene = self.scenes.get(scene_name)
        self.current_scene.show()

    def get_game_objects(self) -> List:
        return list(self.scenes.values())

    def render(self, screen):
        if self.current_scene is not None:
            self.current_scene.render(screen)

    def update(self):
        if self.current_scene is not None:
            self.current_scene.update()
