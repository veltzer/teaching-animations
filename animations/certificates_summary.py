import pathlib
import sys
from typing import override

from manim import BOLD, DOWN, LEFT, RIGHT, UP, FadeIn, Text, VGroup, Write
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared" / "shared-themes"))
from manim_themes import apply_defaults

apply_defaults()


class CertificatesSummary(VoiceoverScene):
    @override
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. a certificate binds a name to a public key", font_size=26),
            Text("2. a CA checks the name, then signs the certificate with its private key", font_size=26),
            Text("3. clients ship with a trust store of CA public keys", font_size=26),
            Text("4. verify: signature, name, dates - then use the key inside", font_size=26),
            Text("5. chain: root (trust store) signs intermediate signs leaf", font_size=26),
            Text("6. expiry and revocation limit the damage of a stolen key", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap certificates and certificate authorities."):
            self.play(Write(title))

        for bullet in bullets:
            if not isinstance(bullet, Text):
                raise TypeError(f"a bullet that is not a Text: {bullet!r}")
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(text="Trust starts with a short list of keys you already have, and is passed down the chain by signatures."):
            self.wait(2)
