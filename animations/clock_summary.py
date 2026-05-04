from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class ClockSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. hardware timer fires at a fixed frequency", font_size=26),
            Text("2. each tick is an unmaskable interrupt", font_size=26),
            Text("3. scheduler hands the CPU to a process for one slice", font_size=26),
            Text("4. the tick forces a trap back into the kernel", font_size=26),
            Text("5. scheduler picks the next process and resumes it", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five steps of preemptive scheduling."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(text="The user program never asked to be paused — the kernel takes control by force, on every tick of the clock."):
            self.wait(2)
