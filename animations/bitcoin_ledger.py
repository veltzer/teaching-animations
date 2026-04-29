from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class BitcoinLedgerAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        self.traditional_ledger()
        self.distributed_ledger()
        peers = self.draw_peers()
        self.broadcast_transaction(peers)
        chain = self.build_chain()
        self.tamper_attempt(chain)
        self.closing()

    def show_title(self):
        title = Text("The Bitcoin Ledger", font_size=46, weight=BOLD)
        subtitle = Text(
            "a public, append-only chain of blocks",
            font_size=26,
            color=YELLOW,
        ).next_to(title, DOWN)

        with self.voiceover(
            text="In this video, we will look at the heart of Bitcoin: "
                 "its ledger. We will see what it is, who keeps it, "
                 "and why it cannot easily be cheated."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def traditional_ledger(self):
        bank_box = RoundedRectangle(
            width=3, height=1.5, corner_radius=0.2, color=BLUE, fill_opacity=0.3
        )
        bank_box.move_to(UP * 1.0)
        bank_lbl = Text("Bank", font_size=24, weight=BOLD).move_to(bank_box.get_center())
        bank = VGroup(bank_box, bank_lbl)

        ledger_box = Rectangle(width=3.6, height=2.0, color=BLUE_A, fill_opacity=0.15)
        ledger_box.move_to(DOWN * 1.5)
        ledger_lbl = Text("private ledger", font_size=20, color=BLUE_A)
        ledger_lbl.next_to(ledger_box, UP, buff=0.1)
        rows = VGroup(
            Text("Alice  -> Bob   10", font_size=16, font="Monospace"),
            Text("Bob    -> Carol  3", font_size=16, font="Monospace"),
            Text("Carol  -> Dave   7", font_size=16, font="Monospace"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ledger_box.get_center())

        with self.voiceover(
            text="Traditionally, a ledger is a book of accounts kept by a single trusted party, "
                 "such as a bank. The bank decides what is in the book, "
                 "and everyone has to trust the bank."
        ):
            self.play(FadeIn(bank, shift=DOWN))
            self.play(Create(ledger_box), Write(ledger_lbl))
            self.play(Write(rows))

        with self.voiceover(
            text="If the bank makes a mistake, or behaves dishonestly, "
                 "the customers have very little recourse."
        ):
            self.play(Indicate(bank, color=RED, scale_factor=1.2))

        self.play(FadeOut(bank), FadeOut(ledger_box), FadeOut(ledger_lbl), FadeOut(rows))

    def distributed_ledger(self):
        headline = Text(
            "Bitcoin replaces the bank with a network",
            font_size=30,
            color=YELLOW,
        ).move_to(UP * 0.3)
        sub = Text(
            "every participant keeps a copy of the same ledger",
            font_size=22,
        ).next_to(headline, DOWN, buff=0.4)

        with self.voiceover(
            text="Bitcoin replaces this central bookkeeper with a peer-to-peer network. "
                 "Every participant keeps their own copy of the ledger, "
                 "and the network agrees on which copy is the real one."
        ):
            self.play(Write(headline))
            self.play(FadeIn(sub, shift=UP))

        self.play(FadeOut(headline), FadeOut(sub))

    def draw_peers(self):
        positions = [
            UP * 2.5 + LEFT * 4.5,
            UP * 2.5 + RIGHT * 4.5,
            DOWN * 2.5 + LEFT * 4.5,
            DOWN * 2.5 + RIGHT * 4.5,
            UP * 0.0 + LEFT * 5.5,
            UP * 0.0 + RIGHT * 5.5,
        ]
        names = ["N1", "N2", "N3", "N4", "N5", "N6"]
        peers = []
        for pos, name in zip(positions, names):
            node_box = Circle(radius=0.55, color=GREEN_C, fill_opacity=0.4)
            node_box.move_to(pos)
            node_lbl = Text(name, font_size=18, weight=BOLD).move_to(pos)
            peers.append(VGroup(node_box, node_lbl))

        with self.voiceover(
            text="Here are six nodes in the network. In reality there are thousands, "
                 "scattered around the world. Each one runs the same Bitcoin software."
        ):
            for peer in peers:
                self.play(FadeIn(peer, scale=0.6), run_time=0.25)

        edges = []
        for i in range(len(peers)):
            for j in range(i + 1, len(peers)):
                line = Line(
                    peers[i][0].get_center(),
                    peers[j][0].get_center(),
                    color=GREY,
                    stroke_width=1,
                    stroke_opacity=0.4,
                )
                edges.append(line)

        with self.voiceover(
            text="The nodes are connected to each other and constantly gossip new information."
        ):
            self.play(*[Create(e) for e in edges], run_time=1.5)

        self.peer_edges = VGroup(*edges)
        return peers

    def broadcast_transaction(self, peers):
        tx_box = RoundedRectangle(
            width=3.0, height=1.0, corner_radius=0.15, color=YELLOW, fill_opacity=0.3
        )
        tx_box.move_to(ORIGIN)
        tx_lbl = Text("Alice -> Bob : 5 BTC", font_size=18, font="Monospace")
        tx_lbl.move_to(tx_box.get_center() + UP * 0.15)
        tx_sig = Text("signed by Alice", font_size=14, color=YELLOW_A)
        tx_sig.move_to(tx_box.get_center() + DOWN * 0.2)
        tx = VGroup(tx_box, tx_lbl, tx_sig)

        with self.voiceover(
            text="Suppose Alice wants to pay Bob five Bitcoin. "
                 "She creates a transaction and signs it with her private key. "
                 "The signature proves the transaction came from her, "
                 "and that nobody changed it on the way."
        ):
            self.play(FadeIn(tx, scale=1.2))

        with self.voiceover(
            text="Alice sends the signed transaction to a few nodes she is connected to."
        ):
            copies = [tx.copy() for _ in peers[:2]]
            anims = [
                copies[0].animate.scale(0.5).move_to(peers[0].get_center() + DOWN * 0.9),
                copies[1].animate.scale(0.5).move_to(peers[1].get_center() + DOWN * 0.9),
            ]
            self.play(*anims, run_time=1.5)

        remote_copies = []
        for peer in peers[2:]:
            copy = tx.copy().scale(0.5)
            copy.move_to(peer.get_center() + DOWN * 0.9)
            remote_copies.append(copy)

        with self.voiceover(
            text="Those nodes verify the signature, and if it is valid, "
                 "they pass the transaction along to their neighbours. "
                 "Within seconds, every node in the network has a copy."
        ):
            self.play(*[FadeIn(c) for c in remote_copies], run_time=1.5)

        all_tx_copies = VGroup(tx, *copies, *remote_copies)
        peers_group = VGroup(*peers)
        self.play(
            FadeOut(all_tx_copies),
            FadeOut(peers_group),
            FadeOut(self.peer_edges),
        )

    def build_chain(self):
        title = Text("The Blockchain", font_size=32, weight=BOLD, color=YELLOW)
        title.to_edge(UP)
        with self.voiceover(
            text="But pending transactions are not yet part of the ledger. "
                 "To become permanent, they must be packed into a block "
                 "and added to the blockchain."
        ):
            self.play(Write(title))

        blocks = []
        for i in range(4):
            block_box = Rectangle(width=2.0, height=2.2, color=BLUE_C, fill_opacity=0.25)
            block_box.move_to(LEFT * 4.5 + RIGHT * 3.0 * i)
            num = Text(f"Block {i}", font_size=18, weight=BOLD, color=BLUE_A)
            num.move_to(block_box.get_top() + DOWN * 0.3)
            prev = Text(
                f"prev: {'000...' if i == 0 else 'h' + str(i - 1)}",
                font_size=12, font="Monospace",
            ).move_to(block_box.get_center() + UP * 0.5)
            txs = Text(
                "txs:\n a->b\n c->d",
                font_size=12, font="Monospace",
            ).move_to(block_box.get_center() + DOWN * 0.05)
            h = Text(f"hash: h{i}", font_size=12, font="Monospace", color=GOLD)
            h.move_to(block_box.get_bottom() + UP * 0.25)
            block = VGroup(block_box, num, prev, txs, h)
            blocks.append(block)

        with self.voiceover(
            text="A block contains a batch of transactions, "
                 "and a reference to the previous block, called its hash. "
                 "The very first block, called the genesis block, points at nothing."
        ):
            self.play(FadeIn(blocks[0], shift=UP))

        for i in range(1, 4):
            arrow = Arrow(
                blocks[i - 1].get_right(),
                blocks[i].get_left(),
                color=YELLOW,
                buff=0.1,
                stroke_width=4,
            )
            with self.voiceover(
                text=f"Block {i} contains new transactions, and references the hash of block {i - 1}. "
                     f"This linkage is what makes it a chain."
            ):
                self.play(FadeIn(blocks[i], shift=UP))
                self.play(Create(arrow))

        with self.voiceover(
            text="Adding a new block requires solving a costly mathematical puzzle, "
                 "called proof of work. The node that solves it first earns a reward "
                 "and gets to append the block. This is what miners do."
        ):
            self.play(Indicate(blocks[-1], color=GOLD, scale_factor=1.1))

        self.play(FadeOut(title))
        return blocks

    def tamper_attempt(self, blocks):
        attacker = Text("Attacker tries to change Block 1", font_size=24, color=RED)
        attacker.to_edge(UP)

        with self.voiceover(
            text="Now suppose an attacker tries to rewrite history "
                 "by changing a transaction in block one."
        ):
            self.play(Write(attacker))
            self.play(Indicate(blocks[1], color=RED, scale_factor=1.1))

        with self.voiceover(
            text="Changing the contents of block one changes its hash. "
                 "But block two still points at the old hash. The chain is now broken."
        ):
            broken = Cross(stroke_color=RED, stroke_width=6).scale(0.5)
            broken.move_to(
                (blocks[1].get_right() + blocks[2].get_left()) / 2
            )
            self.play(Create(broken))

        with self.voiceover(
            text="To fix the link, the attacker would have to redo the proof of work "
                 "for block one, then for block two, then for block three, "
                 "and keep up with all the honest miners working on new blocks. "
                 "In practice, this is computationally infeasible."
        ):
            self.play(Indicate(VGroup(*blocks[1:]), color=RED, scale_factor=1.05))

        with self.voiceover(
            text="And even if the attacker managed it on their own machine, "
                 "the other nodes would simply reject their longer-but-different chain, "
                 "because the network always trusts the chain with the most accumulated work "
                 "that they themselves have verified."
        ):
            self.play(FadeOut(broken), FadeOut(attacker))

    def closing(self):
        with self.voiceover(
            text="And that is the Bitcoin ledger. "
                 "A public, append-only chain of blocks, "
                 "replicated across thousands of nodes, "
                 "secured by cryptographic signatures and proof of work. "
                 "No bank, no central authority, just math and consensus."
        ):
            self.wait(2)


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
