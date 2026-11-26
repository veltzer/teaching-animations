import pathlib
import sys

from manim import (
    BOLD,
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arc,
    Circle,
    Create,
    Cross,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    MathTex,
    RoundedRectangle,
    SurroundingRectangle,
    Text,
    Transform,
    Triangle,
    VGroup,
    Write,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared" / "shared-themes"))
from manim_themes import BASE, T, apply_defaults

apply_defaults()

ACTOR_Y = 1.8
PROP_Y = 0.1


def make_lock(color):
    """An open-or-shut padlock: the picture of a public key (anyone can snap it shut)."""
    body = RoundedRectangle(width=0.6, height=0.5, corner_radius=0.08, color=color, fill_opacity=0.85)
    shackle = Arc(radius=0.2, start_angle=0, angle=PI, arc_center=(0, 0.4, 0), color=color, stroke_width=6)
    legs = VGroup(
        Line((0.2, 0.4, 0), (0.2, 0.25, 0), color=color, stroke_width=6),
        Line((-0.2, 0.4, 0), (-0.2, 0.25, 0), color=color, stroke_width=6),
    )
    keyhole = Dot((0, 0.0, 0), radius=0.06, color=T.BG)
    return VGroup(body, shackle, legs, keyhole)


def make_key(color):
    """A key: the picture of a private key (only it opens the matching padlock)."""
    bow = Circle(radius=0.14, color=color, stroke_width=6).move_to((-0.3, 0, 0))
    shaft = Line((-0.16, 0, 0), (0.4, 0, 0), color=color, stroke_width=6)
    teeth = VGroup(
        Line((0.28, 0, 0), (0.28, -0.14, 0), color=color, stroke_width=6),
        Line((0.4, 0, 0), (0.4, -0.14, 0), color=color, stroke_width=6),
    )
    return VGroup(bow, shaft, teeth)


def make_box(text, color, width=2.2):
    """A message on a card."""
    card = RoundedRectangle(width=width, height=0.7, corner_radius=0.1, color=color, fill_opacity=0.15)
    label = Text(text, font_size=20, font=BASE["font-mono"], color=T.TEXT_PRIMARY).move_to(card)
    return VGroup(card, label)


def make_person(name, color, pos):
    icon = Circle(radius=0.45, color=color, fill_opacity=0.6).move_to(pos)
    label = Text(name, font_size=22, color=color).next_to(icon, DOWN, buff=0.15)
    return VGroup(icon, label)


def make_check():
    return MathTex(r"\checkmark", font_size=56, color=T.SUCCESS)


class PublicKeyCryptoAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        self.props = []

        self.show_title()
        self.draw_actors()
        self.symmetric_problem()
        self.make_key_pair()
        self.publish_public_key()
        self.encrypt_and_send()
        self.sign_and_verify()
        self.show_rsa_math()
        self.show_the_gap()

        with self.voiceover(
            text="That is public-key cryptography: a public key that anyone may hold, "
                 "a private key that never leaves its owner, and one open question — whose key is it?"
        ):
            self.wait(2)

    # ── helpers ──────────────────────────────────────────────────────────────

    def add_props(self, *mobjects):
        self.props.extend(mobjects)

    def clear_props(self):
        if self.props:
            self.play(*[FadeOut(m) for m in self.props])
        self.props = []

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.props = []

    # ── sections ─────────────────────────────────────────────────────────────

    def show_title(self):
        title = Text("Public-Key Cryptography", font_size=44, weight=BOLD)
        subtitle = Text("one key locks, a different key unlocks", font_size=24, color=T.WARNING).next_to(title, DOWN)

        with self.voiceover(
            text="How can you send a secret to someone you have never met, "
                 "without first agreeing on a shared password? "
                 "The answer is public-key cryptography."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def draw_actors(self):
        self.alice = make_person("Alice", T.ACCENT, [-5.5, ACTOR_Y, 0])
        self.bob = make_person("Bob", T.SUCCESS, [5.5, ACTOR_Y, 0])

        eve_icon = Triangle(color=T.DANGER, fill_opacity=0.5).scale(0.45).move_to((0, -2.4, 0))
        eve_lbl = Text("Eve (eavesdropper)", font_size=20, color=T.DANGER).next_to(eve_icon, DOWN, buff=0.15)
        self.eve = VGroup(eve_icon, eve_lbl)

        self.wire = DashedLine(self.alice[0].get_right(), self.bob[0].get_left(), color=T.BORDER)
        self.wire_lbl = Text("public channel", font_size=16, color=T.BORDER).next_to(self.wire, UP, buff=0.1)

        with self.voiceover(
            text="Alice wants to send Bob a private message. Everything they send travels over a public channel, "
                 "and Eve reads every byte of it."
        ):
            self.play(FadeIn(self.alice, shift=RIGHT), FadeIn(self.bob, shift=LEFT))
            self.play(Create(self.wire), Write(self.wire_lbl))
            self.play(FadeIn(self.eve, shift=UP))

    def symmetric_problem(self):
        key = make_key(T.WARNING).move_to((-4.2, ACTOR_Y, 0))
        key_lbl = Text("shared key", font_size=16, color=T.WARNING).next_to(key, DOWN, buff=0.15)

        with self.voiceover(
            text="With ordinary, symmetric encryption, the same key locks and unlocks. "
                 "So Alice and Bob must both hold that key before they can talk privately."
        ):
            self.play(FadeIn(key, scale=1.5), Write(key_lbl))

        eve_copy = key.copy()
        with self.voiceover(
            text="But how does the key get to Bob? If Alice sends it over the wire, Eve simply copies it, "
                 "and every message after that is readable to her."
        ):
            self.play(FadeOut(key_lbl), key.animate.move_to((4.2, ACTOR_Y, 0)), eve_copy.animate.move_to((1.2, -2.4, 0)))
            self.play(Indicate(eve_copy, color=T.DANGER, scale_factor=1.5))

        self.add_props(key, eve_copy)
        self.clear_props()

    def make_key_pair(self):
        lock = make_lock(T.SUCCESS).move_to((4.1, PROP_Y, 0))
        lock_lbl = Text("public key", font_size=16, color=T.SUCCESS).next_to(lock, DOWN, buff=0.15)
        key = make_key(T.SUCCESS).move_to((5.7, PROP_Y, 0))
        key_lbl = Text("private key", font_size=16, color=T.SUCCESS).next_to(key, DOWN, buff=0.2)

        with self.voiceover(
            text="Public-key cryptography uses two keys that are made together, as a matched pair. "
                 "Bob generates his pair."
        ):
            self.play(FadeIn(lock, scale=1.5), FadeIn(key, scale=1.5))

        with self.voiceover(
            text="One half is public. Picture it as an open padlock: anyone can snap it shut on a box."
        ):
            self.play(Write(lock_lbl))
            self.play(Indicate(lock, color=T.SUCCESS, scale_factor=1.3))

        guard = SurroundingRectangle(VGroup(key, key_lbl), color=T.DANGER, buff=0.12)
        guard_lbl = Text("never leaves Bob", font_size=14, color=T.DANGER).next_to(guard, DOWN, buff=0.1)
        with self.voiceover(
            text="The other half is private: the one key that opens that padlock. "
                 "Bob keeps it to himself and never sends it anywhere."
        ):
            self.play(Write(key_lbl))
            self.play(Create(guard), Write(guard_lbl))

        with self.voiceover(
            text="The two are linked by mathematics, yet knowing the public key does not reveal the private one."
        ):
            self.wait(1)

        self.bob_lock = lock
        self.bob_key = key
        self.pair_labels = VGroup(lock_lbl, key_lbl, guard, guard_lbl)

    def publish_public_key(self):
        alice_lock = self.bob_lock.copy()
        eve_lock = self.bob_lock.copy()

        with self.voiceover(
            text="Bob publishes the public key. Alice gets a copy. Eve gets a copy too — and that is fine, "
                 "because a padlock can only lock things, never open them."
        ):
            self.play(alice_lock.animate.move_to((-5.5, PROP_Y, 0)))
            self.play(eve_lock.animate.move_to((1.2, -2.4, 0)))

        self.alice_lock = alice_lock
        self.eve_lock = eve_lock

    def encrypt_and_send(self):
        msg = make_box("meet at 6", T.ACCENT).move_to((-3.2, PROP_Y, 0))
        with self.voiceover(text="Alice writes her message."):
            self.play(FadeIn(msg, shift=UP))

        cipher_text = Text("9f#xQ2!a", font_size=20, font=BASE["font-mono"], color=T.TEXT_PRIMARY).move_to(msg[1])
        with self.voiceover(
            text="She puts it in a box and snaps Bob's padlock shut on it. "
                 "Now the message is ciphertext: scrambled for everyone except the holder of Bob's private key. "
                 "Not even Alice can open it again."
        ):
            self.play(self.alice_lock.animate.scale(0.8).next_to(msg, RIGHT, buff=-0.15))
            self.play(Transform(msg[1], cipher_text), msg[0].animate.set_color(T.SUCCESS))

        locked = VGroup(msg, self.alice_lock)
        eve_copy = locked.copy()
        with self.voiceover(text="Alice sends the locked box across the public channel. Eve copies it on the way."):
            self.play(locked.animate.move_to((2.6, PROP_Y, 0)), eve_copy.animate.scale(0.7).move_to((-1.8, -2.4, 0)))

        cross = Cross(eve_copy, color=T.DANGER, stroke_width=6)
        with self.voiceover(
            text="Eve has the box and she has Bob's padlock. Neither helps her: there is no key in her hands."
        ):
            self.play(Create(cross))

        plain = Text("meet at 6", font_size=20, font=BASE["font-mono"], color=T.TEXT_PRIMARY).move_to(msg[1])
        with self.voiceover(text="Bob uses his private key. The padlock opens, and he reads the message."):
            self.play(self.bob_key.animate.next_to(self.alice_lock, RIGHT, buff=0.05))
            self.play(FadeOut(self.alice_lock, shift=UP), Transform(msg[1], plain), msg[0].animate.set_color(T.ACCENT))
            self.play(self.bob_key.animate.move_to((5.7, PROP_Y, 0)))
            self.play(Indicate(msg, color=T.SUCCESS))

        with self.voiceover(text="Encrypt with the public key, decrypt with the private key. That is confidentiality."):
            self.wait(1)

        self.add_props(msg, eve_copy, self.eve_lock, cross)
        self.clear_props()

    def sign_and_verify(self):
        with self.voiceover(
            text="The pair also works the other way round. "
                 "Something done with the private key can be checked by anyone holding the public key. "
                 "That gives us digital signatures."
        ):
            self.play(Indicate(self.bob_key, color=T.SUCCESS, scale_factor=1.3))

        msg = make_box("price: $100", T.SUCCESS).move_to((2.6, PROP_Y, 0))
        seal = VGroup(
            Circle(radius=0.32, color=T.SUCCESS, fill_opacity=0.8),
            Text("sig", font_size=16, color=T.BG),
        ).next_to(msg, DOWN, buff=0.15)

        with self.voiceover(
            text="Bob writes a message, and runs it through a signing function together with his private key. "
                 "Out comes a signature that fits this exact message, and that only his private key could have made."
        ):
            self.play(FadeIn(msg, shift=UP))
            self.play(self.bob_key.animate.next_to(msg, RIGHT, buff=0.15))
            self.play(FadeIn(seal, scale=1.5))
            self.play(self.bob_key.animate.move_to((5.7, PROP_Y, 0)))

        signed = VGroup(msg, seal)
        with self.voiceover(text="He sends the message and its signature to Alice. Nothing here is secret."):
            self.play(signed.animate.move_to((-3.0, PROP_Y - 0.2, 0)))

        check = make_check().next_to(signed, DOWN, buff=0.2)
        with self.voiceover(
            text="Alice checks the signature using Bob's public key. It matches. "
                 "So the message really came from Bob, and not one character of it was changed."
        ):
            self.play(self.alice_lock.animate.next_to(signed, LEFT, buff=0.2))
            self.play(Write(check))
            self.play(self.alice_lock.animate.move_to((-5.5, PROP_Y, 0)))

        self.play(FadeOut(check), signed.animate.move_to((0, PROP_Y - 0.2, 0)))

        forged = Text("price: $900", font_size=20, font=BASE["font-mono"], color=T.DANGER).move_to(msg[1])
        with self.voiceover(text="Now suppose an attacker on the wire changes the price on the way."):
            self.play(Transform(msg[1], forged), msg[0].animate.set_color(T.DANGER))
            self.play(signed.animate.move_to((-3.0, PROP_Y - 0.2, 0)))

        bad = Cross(seal, color=T.DANGER, stroke_width=6)
        with self.voiceover(
            text="Alice checks again, and this time the signature does not match the message. "
                 "The attacker can't make a new signature either, because that needs Bob's private key."
        ):
            self.play(self.alice_lock.animate.next_to(signed, LEFT, buff=0.2))
            self.play(Create(bad))
            self.play(self.alice_lock.animate.move_to((-5.5, PROP_Y, 0)))

        with self.voiceover(text="Sign with the private key, verify with the public key. That is authenticity and integrity."):
            self.wait(1)

        self.add_props(signed, bad)
        self.clear_props()

    def show_rsa_math(self):
        with self.voiceover(text="Under the hood, the classic way to build such a pair is R S A. Here it is with toy numbers."):
            self.clear_all()

        heading = Text("RSA with toy numbers", font_size=32, weight=BOLD).to_edge(UP)
        rows = VGroup(
            MathTex(r"p = 3,\quad q = 11,\quad n = p \cdot q = 33", font_size=36),
            MathTex(r"\text{public key: } (n, e) = (33,\ 3)", font_size=36, color=T.SUCCESS),
            MathTex(r"\text{private key: } d = 7 \quad (3 \cdot 7 = 21 \equiv 1 \bmod 20)", font_size=36, color=T.DANGER),
            MathTex(r"\text{encrypt } m = 4:\quad c = m^e \bmod n = 4^3 \bmod 33 = 31", font_size=36, color=T.ACCENT),
            MathTex(r"\text{decrypt:}\quad m = c^d \bmod n = 31^7 \bmod 33 = 4", font_size=36, color=T.ACCENT),
        ).arrange(DOWN, buff=0.35).next_to(heading, DOWN, buff=0.5)
        hard = Text("Finding d from (n, e) needs the factors of n.\nFor a 2048-bit n, nobody knows how to do that.",
                    font_size=20, color=T.WARNING).next_to(rows, DOWN, buff=0.45)

        with self.voiceover(text="Bob picks two primes, here 3 and 11, and multiplies them: n is 33."):
            self.play(Write(heading))
            self.play(Write(rows[0]))

        with self.voiceover(text="His public key is n together with an exponent e, here 3."):
            self.play(Write(rows[1]))

        with self.voiceover(
            text="His private key is another exponent, d equals 7, chosen so that e times d is 1, "
                 "modulo a number Bob can only compute because he knows the two primes."
        ):
            self.play(Write(rows[2]))

        with self.voiceover(text="To encrypt the message 4, Alice raises it to the power e, modulo n, and gets 31."):
            self.play(Write(rows[3]))

        with self.voiceover(text="Bob raises 31 to the power d, modulo n, and gets 4 back."):
            self.play(Write(rows[4]))

        with self.voiceover(
            text="Eve sees n and e, but to find d she would have to factor n. "
                 "With real keys, n is over six hundred digits long, and factoring it is out of reach."
        ):
            self.play(Write(hard))

        self.clear_all()

    def show_the_gap(self):
        alice = make_person("Alice", T.ACCENT, [-5.5, ACTOR_Y, 0])
        bob = make_person("Bob", T.SUCCESS, [5.5, ACTOR_Y, 0])
        mal_icon = Triangle(color=T.DANGER, fill_opacity=0.5).scale(0.45).move_to((0, ACTOR_Y, 0))
        mal_lbl = Text("Mallory (in the middle)", font_size=20, color=T.DANGER).next_to(mal_icon, DOWN, buff=0.15)
        mallory = VGroup(mal_icon, mal_lbl)

        with self.voiceover(
            text="There is one hole left. Suppose the attacker can do more than listen: "
                 "Mallory sits in the middle and can change what passes through."
        ):
            self.play(FadeIn(alice), FadeIn(bob))
            self.play(FadeIn(mallory, shift=DOWN))

        bob_lock = make_lock(T.SUCCESS).move_to((4.0, PROP_Y - 0.6, 0))
        mal_lock = make_lock(T.DANGER).move_to((0, PROP_Y - 0.6, 0))
        question = Text("Bob's key?", font_size=18, color=T.TEXT_SECONDARY)

        with self.voiceover(
            text="Bob sends his public key to Alice. Mallory catches it, keeps it, "
                 "and passes on her own public key instead."
        ):
            self.play(FadeIn(bob_lock))
            self.play(bob_lock.animate.move_to((0.9, PROP_Y - 0.6, 0)))
            self.play(FadeIn(mal_lock, scale=1.5), bob_lock.animate.scale(0.7).move_to((1.2, PROP_Y - 1.4, 0)))
            self.play(mal_lock.animate.move_to((-4.0, PROP_Y - 0.6, 0)))
            question.next_to(mal_lock, DOWN, buff=0.2)
            self.play(Write(question))

        env = make_box("meet at 6", T.ACCENT, width=1.8).move_to((-2.2, PROP_Y - 0.6, 0))
        with self.voiceover(
            text="A padlock is just a padlock. Nothing on it says who it belongs to, "
                 "so Alice locks her message with Mallory's key and sends it."
        ):
            self.play(FadeOut(question), FadeIn(env))
            self.play(mal_lock.animate.scale(0.8).next_to(env, RIGHT, buff=-0.15))
            sent = VGroup(env, mal_lock)
            self.play(sent.animate.move_to((-0.4, PROP_Y - 0.6, 0)))

        with self.voiceover(
            text="Mallory opens it with her own private key and reads it. "
                 "Then she locks it again with Bob's real key and forwards it. "
                 "Alice and Bob notice nothing. This is the man-in-the-middle attack."
        ):
            self.play(FadeOut(mal_lock, shift=UP))
            self.play(Indicate(env, color=T.DANGER, scale_factor=1.3))
            self.play(bob_lock.animate.scale(1.15).next_to(env, RIGHT, buff=-0.15))
            self.play(VGroup(env, bob_lock).animate.move_to((3.6, PROP_Y - 0.6, 0)))

        with self.voiceover(
            text="Public-key cryptography by itself cannot tell Alice whose key she is holding. "
                 "Closing that gap is the job of certificates, the subject of the next animation."
        ):
            self.wait(2)
