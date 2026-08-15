import pathlib
import sys

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared" / "shared-themes"))
from manim_themes import apply_defaults

apply_defaults()


class ForkSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. fork creates an almost-identical copy of the calling process", font_size=24),
            Text("2. it returns twice — once in the parent, once in the child", font_size=24),
            Text("3. parent gets the child's PID; child gets zero", font_size=24),
            Text("4. memory is shared copy-on-write — never copied unless written", font_size=24),
            Text("5. fork + exec is how every Unix program gets started", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five points about fork."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="One call, two processes, branching on the return value. "
                 "That is the whole trick."
        ):
            self.wait(2)
