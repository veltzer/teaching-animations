import pathlib
import sys

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared" / "shared-themes"))
from manim_themes import apply_defaults

apply_defaults()


class MutexSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. only one thread can hold the mutex at a time", font_size=24),
            Text("2. lock() uses an atomic test-and-set instruction", font_size=24),
            Text("3. the loser is parked in a wait queue and sleeps", font_size=24),
            Text("4. unlock() hands the lock to the next waiter", font_size=24),
            Text("5. correctness comes from the hardware atomic, not from the OS", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five points about mutexes."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="A mutex is the cheapest way to turn a race condition into a queue."
        ):
            self.wait(2)
