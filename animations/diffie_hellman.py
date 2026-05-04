from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class DiffieHellmanAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        alice, bob, eve = self.draw_actors()
        public = self.show_public_color(alice, bob, eve)
        a_priv, b_priv = self.pick_private_colors(alice, bob)
        a_mix, b_mix = self.mix_with_public(alice, bob, public, a_priv, b_priv)
        self.exchange_in_public(alice, bob, eve, a_mix, b_mix)
        self.derive_shared_secret(alice, bob, eve, a_priv, b_priv, a_mix, b_mix)
        self.show_math()

        with self.voiceover(text="And that is Diffie-Hellman key exchange — a shared secret built in public, with nothing secret ever crossing the wire."):
            self.wait(2)

    def show_title(self):
        title = Text("Diffie-Hellman Key Exchange", font_size=44, weight=BOLD)
        subtitle = Text("a shared secret over a public channel", font_size=24, color=YELLOW).next_to(title, DOWN)

        with self.voiceover(
            text="How can two strangers, talking over a wire that anyone can read, "
                 "agree on a secret key — without ever sending the key itself? "
                 "The answer is Diffie-Hellman key exchange."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def draw_actors(self):
        alice_icon = Circle(radius=0.5, color=BLUE_C, fill_opacity=0.6).move_to(LEFT * 5 + UP * 1.5)
        alice_lbl = Text("Alice", font_size=22, color=BLUE).next_to(alice_icon, DOWN, buff=0.15)
        alice = VGroup(alice_icon, alice_lbl)

        bob_icon = Circle(radius=0.5, color=GREEN_C, fill_opacity=0.6).move_to(RIGHT * 5 + UP * 1.5)
        bob_lbl = Text("Bob", font_size=22, color=GREEN).next_to(bob_icon, DOWN, buff=0.15)
        bob = VGroup(bob_icon, bob_lbl)

        eve_icon = Triangle(color=RED_C, fill_opacity=0.5).scale(0.5).move_to(DOWN * 2.5)
        eve_lbl = Text("Eve (eavesdropper)", font_size=20, color=RED).next_to(eve_icon, DOWN, buff=0.15)
        eve = VGroup(eve_icon, eve_lbl)

        wire = DashedLine(alice_icon.get_right(), bob_icon.get_left(), color=GREY)
        wire_lbl = Text("public channel", font_size=16, color=GREY).next_to(wire, UP, buff=0.1)

        with self.voiceover(
            text="Meet Alice and Bob. They want to share a secret. "
                 "But everything they say travels over a public channel."
        ):
            self.play(FadeIn(alice, shift=RIGHT), FadeIn(bob, shift=LEFT))
            self.play(Create(wire), Write(wire_lbl))

        with self.voiceover(
            text="And listening to that channel is Eve. She sees every byte that flows between them."
        ):
            self.play(FadeIn(eve, shift=UP))

        self.wire = wire
        self.wire_lbl = wire_lbl
        return alice, bob, eve

    def show_public_color(self, alice, bob, eve):
        public = Square(side_length=0.7, color=YELLOW, fill_opacity=0.8).move_to(UP * 0.2)
        public_lbl = Text("public color\n(everyone knows it)", font_size=16, color=YELLOW).next_to(public, UP, buff=0.15)

        with self.voiceover(
            text="The protocol begins with a public color. Alice, Bob, and Eve all know it. "
                 "Think of it as a base paint anyone can buy at the store."
        ):
            self.play(FadeIn(public, scale=1.5), Write(public_lbl))

        self.public_color = public
        self.public_color_lbl = public_lbl
        return public

    def pick_private_colors(self, alice, bob):
        a_priv = Square(side_length=0.6, color=BLUE_E, fill_opacity=0.9).next_to(alice, UP, buff=0.3)
        a_priv_lbl = Text("a (secret)", font_size=16, color=BLUE_E).next_to(a_priv, UP, buff=0.1)

        b_priv = Square(side_length=0.6, color=GREEN_E, fill_opacity=0.9).next_to(bob, UP, buff=0.3)
        b_priv_lbl = Text("b (secret)", font_size=16, color=GREEN_E).next_to(b_priv, UP, buff=0.1)

        with self.voiceover(
            text="Now each one picks a private color. Alice picks hers — call it little a. "
                 "Bob picks his — little b. Neither shows the private color to anyone."
        ):
            self.play(FadeIn(a_priv, scale=1.5), Write(a_priv_lbl))
            self.play(FadeIn(b_priv, scale=1.5), Write(b_priv_lbl))

        self.a_priv_lbl = a_priv_lbl
        self.b_priv_lbl = b_priv_lbl
        return a_priv, b_priv

    def mix_with_public(self, alice, bob, public, a_priv, b_priv):
        a_mix = Square(side_length=0.7, color=PURPLE, fill_opacity=0.9).move_to(LEFT * 3 + UP * 1.5)
        a_mix_lbl = Text("A = mix(public, a)", font_size=16, color=PURPLE).next_to(a_mix, UP, buff=0.1)

        b_mix = Square(side_length=0.7, color=TEAL, fill_opacity=0.9).move_to(RIGHT * 3 + UP * 1.5)
        b_mix_lbl = Text("B = mix(public, b)", font_size=16, color=TEAL).next_to(b_mix, UP, buff=0.1)

        with self.voiceover(
            text="Each of them mixes their private color with the public color. "
                 "Alice gets a new color — capital A. Bob gets capital B. "
                 "These mixes are easy to make, but undoing the mix to recover the private color is hard."
        ):
            self.play(
                Transform(a_priv.copy(), a_mix),
                Transform(public.copy(), a_mix),
                Write(a_mix_lbl),
            )
            self.play(
                Transform(b_priv.copy(), b_mix),
                Transform(public.copy(), b_mix),
                Write(b_mix_lbl),
            )

        self.a_mix_lbl = a_mix_lbl
        self.b_mix_lbl = b_mix_lbl
        return a_mix, b_mix

    def exchange_in_public(self, alice, bob, eve, a_mix, b_mix):
        send_a = a_mix.copy()
        send_b = b_mix.copy()

        with self.voiceover(
            text="Now they exchange the mixes over the public channel. "
                 "Alice sends capital A. Bob sends capital B."
        ):
            self.play(send_a.animate.move_to(RIGHT * 3 + UP * 1.5))
            self.play(send_b.animate.move_to(LEFT * 3 + UP * 1.5))

        eve_a = a_mix.copy().scale(0.6)
        eve_b = b_mix.copy().scale(0.6)
        eve_box = SurroundingRectangle(VGroup(eve_a, eve_b), color=RED, buff=0.15)
        eve_a.move_to(DOWN * 2.5 + LEFT * 0.6)
        eve_b.move_to(DOWN * 2.5 + RIGHT * 0.6)
        eve_box = SurroundingRectangle(VGroup(eve_a, eve_b), color=RED, buff=0.15)
        eve_lbl = Text("Eve sees: public, A, B", font_size=16, color=RED).next_to(eve_box, RIGHT, buff=0.2)

        with self.voiceover(
            text="Eve, listening on the channel, captures both mixes. "
                 "She now knows the public color, and the two mixes."
        ):
            self.play(FadeIn(eve_a, scale=0.6), FadeIn(eve_b, scale=0.6))
            self.play(Create(eve_box), Write(eve_lbl))

        self.eve_extras = VGroup(eve_a, eve_b, eve_box, eve_lbl)
        self.received_b_at_alice = send_b
        self.received_a_at_bob = send_a

    def derive_shared_secret(self, alice, bob, eve, a_priv, b_priv, a_mix, b_mix):
        secret_a = Square(side_length=0.8, color=GOLD, fill_opacity=0.95).move_to(LEFT * 5 + DOWN * 0.3)
        secret_b = Square(side_length=0.8, color=GOLD, fill_opacity=0.95).move_to(RIGHT * 5 + DOWN * 0.3)

        with self.voiceover(
            text="Now the magic. Alice takes the mix she received from Bob — capital B — "
                 "and mixes her own private color into it."
        ):
            self.play(
                Transform(a_priv.copy(), secret_a),
                Transform(self.received_b_at_alice.copy(), secret_a),
            )

        with self.voiceover(
            text="Bob does the same: he takes capital A from Alice and mixes in his private color."
        ):
            self.play(
                Transform(b_priv.copy(), secret_b),
                Transform(self.received_a_at_bob.copy(), secret_b),
            )

        equals = MathTex("=", font_size=64, color=GOLD).move_to(DOWN * 0.3)

        with self.voiceover(
            text="And here is the key insight. Mixing is commutative. "
                 "Public, then a, then b — gives the same color as public, then b, then a. "
                 "So Alice and Bob end up with the exact same shared secret."
        ):
            self.play(Write(equals))
            self.play(Indicate(secret_a, color=GOLD, scale_factor=1.3))
            self.play(Indicate(secret_b, color=GOLD, scale_factor=1.3))

        with self.voiceover(
            text="But Eve cannot make the same secret. She has the public color, capital A, and capital B — "
                 "but never little a or little b. And separating a mix back into its components is computationally hard."
        ):
            cross = Cross(self.eve_extras, color=RED, stroke_width=6)
            self.play(Create(cross))
            self.play(Indicate(self.eve_extras, color=RED, scale_factor=1.05))

        self.secret_a = secret_a
        self.secret_b = secret_b
        self.equals = equals

    def show_math(self):
        with self.voiceover(text="Under the hood, the mixing is modular exponentiation."):
            self.play(
                FadeOut(self.public_color),
                FadeOut(self.public_color_lbl),
                FadeOut(self.eve_extras),
                FadeOut(self.secret_a),
                FadeOut(self.secret_b),
                FadeOut(self.equals),
                FadeOut(self.wire),
                FadeOut(self.wire_lbl),
            )

        eq_public = MathTex(r"\text{public: } g, p", font_size=36, color=YELLOW).move_to(UP * 1.5)
        eq_a = MathTex(r"A = g^a \bmod p", font_size=36, color=BLUE).move_to(UP * 0.7)
        eq_b = MathTex(r"B = g^b \bmod p", font_size=36, color=GREEN).move_to(UP * 0.0)
        eq_secret = MathTex(r"s = B^a = A^b = g^{ab} \bmod p", font_size=40, color=GOLD).move_to(DOWN * 0.9)
        eq_hard = Text("Eve has g, p, A, B but recovering a or b\nis the discrete-log problem — believed to be hard.",
                       font_size=20, color=RED).move_to(DOWN * 2.3)

        with self.voiceover(text="The public color becomes a generator g and a prime p, both publicly agreed."):
            self.play(Write(eq_public))

        with self.voiceover(text="Alice's mix is g raised to her secret a, modulo p. Bob's is g raised to b, modulo p."):
            self.play(Write(eq_a))
            self.play(Write(eq_b))

        with self.voiceover(text="The shared secret is g to the a-times-b. Both sides can compute it from what they have. Eve cannot — recovering a or b from A or B is the discrete logarithm problem."):
            self.play(Write(eq_secret))
            self.play(Write(eq_hard))
