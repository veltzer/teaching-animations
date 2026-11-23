import pathlib
import sys

from manim import BOLD, DOWN, LEFT, RIGHT, UP, FadeIn, Text, VGroup, Write
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared" / "shared-themes"))
from manim_themes import apply_defaults

apply_defaults()


class PublicKeyCryptoSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. keys come in pairs: one public, one private", font_size=26),
            Text("2. share the public key freely; the private key never leaves its owner", font_size=26),
            Text("3. encrypt with the public key, only the private key decrypts", font_size=26),
            Text("4. sign with the private key, anyone verifies with the public key", font_size=26),
            Text("5. security rests on a hard problem, e.g. factoring for RSA", font_size=26),
            Text("6. open question: whose public key is this? (certificates)", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap public-key cryptography."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(text="Two keys, two jobs: confidentiality and signatures, without ever sharing a secret in advance."):
            self.wait(2)
