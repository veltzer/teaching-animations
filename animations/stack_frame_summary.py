from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class StackFrameSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. each function call pushes a frame onto the stack", font_size=24),
            Text("2. a frame holds: return address, saved fp, args, locals", font_size=24),
            Text("3. call pushes; return pops, in strict LIFO order", font_size=24),
            Text("4. the stack pointer marks the current top of stack", font_size=24),
            Text("5. nested calls just nest frames — recursion is free", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five points about stack frames."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="One stack, many frames, all governed by push and pop."
        ):
            self.wait(2)
