from dataclasses import dataclass
from typing import override, Callable, Any

from manim import *


@dataclass(frozen=True)
class Updater:
    func: Callable[[], Any]
    priority: float


@dataclass(frozen=True)
class SceneState:
    updaters: set[Updater]
    to_track: Mobject | None


class OrderedUpdateScene(MovingCameraScene):

    def __init__(self, **kwargs):
        self._updaters: set[Updater] = set()
        super().__init__(**kwargs)
        updater_mob = Mobject()
        updater_mob.add_updater(lambda _: self.update())
        self.add(updater_mob)
        self._to_track: Mobject | None = None
        self._tracking_margin: float = .1
        self._enables_track: bool = False

    def update(self):
        updaters_sorted = sorted(self._updaters, key=lambda ud: ud.priority, reverse=True)
        for u in updaters_sorted:
            u.func()
        if self._enables_track:
            self._track()

    @override
    def add_updater(self, func: Callable[[], Any], priority: float = 0) -> None:
        self._updaters.add(Updater(func=func, priority=priority))

    @override
    def remove_updater(self, func: Callable[[], Any]) -> None:
        for u in self._updaters:
            if u.func == func:
                self._updaters.remove(u)
                return
        else:
            raise ValueError("Given function isn't registered")

    def clear_updaters(self):
        self._updaters: set[Updater] = set()

    def _track(self):
        if self._to_track.get_width() / self._to_track.get_height() >= 3 / 2:
            self.camera.frame.set_width(self._to_track.get_width() * (1 + self._tracking_margin))
        else:
            self.camera.frame.set_height(self._to_track.get_height() * (1 + self._tracking_margin))
        self.camera.frame.move_to(self._to_track)

    def start_tracking(self, mobject_to_track: Mobject, margin: float = None, run_time: float = 1):
        self._tracking_margin = margin if margin else self._tracking_margin
        self._enables_track = False
        if mobject_to_track.get_width() / mobject_to_track.get_height() >= 3 / 2:
            self.play(
                self.camera.frame.animate
                .set_width(mobject_to_track.get_width() * (1 + self._tracking_margin)).move_to(mobject_to_track),
                run_time=run_time
            )
        else:
            self.play(
                self.camera.frame.animate
                .set_height(mobject_to_track.get_height() * (1 + self._tracking_margin)).move_to(mobject_to_track),
                run_time=run_time
            )
        self._to_track = mobject_to_track
        self._enables_track = True

    def save_state(self):
        return SceneState(self._updaters, self._to_track)

    def restore_state(self, scene_state: SceneState):
        self._updaters = scene_state.updaters
        if scene_state.to_track is not None:
            self.start_tracking(scene_state.to_track)
