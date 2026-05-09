from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared" / "shared-themes"))
from manim_themes import apply_defaults
apply_defaults()


class TcpHandshakeSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. SYN: client picks a random seq and sends it", font_size=24),
            Text("2. SYN-ACK: server picks its own seq, acks the client's", font_size=24),
            Text("3. ACK: client acks the server's seq", font_size=24),
            Text("4. both sides land in ESTABLISHED", font_size=24),
            Text("5. random initial seqs make blind injection harder", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five points about the TCP handshake."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="Three packets, two random numbers, one open connection."
        ):
            self.wait(2)
