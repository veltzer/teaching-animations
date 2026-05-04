from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class BitcoinLedgerSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. the ledger is a chain of blocks of transactions", font_size=26),
            Text("2. every full node stores its own copy", font_size=26),
            Text("3. transactions are signed and gossiped peer-to-peer", font_size=26),
            Text("4. miners append new blocks via proof of work", font_size=26),
            Text("5. each block hashes the previous, locking history", font_size=26),
            Text("6. nodes follow the chain with the most work", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(title, DOWN, buff=0.5)

        with self.voiceover(text="To recap the key ideas behind the Bitcoin ledger."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="That is how a global, decentralized, tamper-resistant "
                 "record of money can exist without a central authority."
        ):
            self.wait(2)
