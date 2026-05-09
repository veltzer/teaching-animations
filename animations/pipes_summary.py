from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared" / "shared-themes"))
from manim_themes import T, BASE, apply_defaults
apply_defaults()


class PipesSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. a pipe is a fixed-size kernel buffer", font_size=24),
            Text("2. fd[1] is the write end, fd[0] is the read end", font_size=24),
            Text("3. bytes come out in the same order they went in", font_size=24),
            Text("4. write() blocks when the buffer is full", font_size=24),
            Text("5. read() blocks when the buffer is empty", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five points about pipes."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="One byte stream, two file descriptors, and the kernel keeping the producer "
                 "and consumer in lockstep through blocking."
        ):
            self.wait(2)
