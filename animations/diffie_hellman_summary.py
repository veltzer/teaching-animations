from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class DiffieHellmanSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. agree on public values g and p", font_size=26),
            Text("2. each side picks a private exponent (a, b)", font_size=26),
            Text("3. each side sends g^x mod p", font_size=26),
            Text("4. each side raises the received value to its own exponent", font_size=26),
            Text("5. both arrive at g^(ab) mod p — the shared secret", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five steps of Diffie-Hellman."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(text="The secret is built in public, but its security rests on a single hard problem: the discrete logarithm."):
            self.wait(2)
