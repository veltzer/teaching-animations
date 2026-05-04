from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class RaceConditionSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. one C statement = three machine instructions", font_size=26),
            Text("2. the scheduler can preempt between any two of them", font_size=26),
            Text("3. two threads can both read the old value", font_size=26),
            Text("4. one thread's write overwrites the other's", font_size=26),
            Text("5. fix: make read-modify-write atomic", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five points about race conditions."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="A race condition is not a bug in your code — it is a bug in your assumption "
                 "that one line of source code is one indivisible step. It is not."
        ):
            self.wait(2)
