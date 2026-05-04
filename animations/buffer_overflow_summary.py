from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class BufferOverflowSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. local arrays live on the stack, next to the return address", font_size=24),
            Text("2. strcpy and friends do not check the destination size", font_size=24),
            Text("3. an over-long input writes past the buffer", font_size=24),
            Text("4. the saved return address gets overwritten", font_size=24),
            Text("5. on return, the CPU jumps wherever the attacker chose", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five steps of a classic stack buffer overflow."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="The bug is one missing bounds check. The consequence is full control over the program."
        ):
            self.wait(2)
