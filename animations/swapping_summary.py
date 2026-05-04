from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class SwappingSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. memory is split into fixed-size pages and frames", font_size=26),
            Text("2. the page table maps each page to RAM or to swap", font_size=26),
            Text("3. accessing an absent page raises a page fault", font_size=26),
            Text("4. the kernel evicts a victim page out to disk", font_size=26),
            Text("5. the needed page is read in and the access retries", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five steps of swapping."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="That is how the operating system gives every program "
                 "the illusion of nearly unlimited memory."
        ):
            self.wait(2)
