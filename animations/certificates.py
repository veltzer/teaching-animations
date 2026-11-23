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
    Arrow,
    Circle,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
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

MONO = BASE["font-mono"]


def make_lock(color):
    """A padlock: the picture of a public key, as in public_key_crypto.py."""
    body = RoundedRectangle(width=0.6, height=0.5, corner_radius=0.08, color=color, fill_opacity=0.85)
    shackle = Arc(radius=0.2, start_angle=0, angle=PI, arc_center=[0, 0.4, 0], color=color, stroke_width=6)
    legs = VGroup(
        Line([0.2, 0.4, 0], [0.2, 0.25, 0], color=color, stroke_width=6),
        Line([-0.2, 0.4, 0], [-0.2, 0.25, 0], color=color, stroke_width=6),
    )
    keyhole = Dot([0, 0.0, 0], radius=0.06, color=T.BG)
    return VGroup(body, shackle, legs, keyhole)


def make_key(color):
    """A key: the picture of a private key."""
    bow = Circle(radius=0.14, color=color, stroke_width=6).move_to([-0.3, 0, 0])
    shaft = Line([-0.16, 0, 0], [0.4, 0, 0], color=color, stroke_width=6)
    teeth = VGroup(
        Line([0.28, 0, 0], [0.28, -0.14, 0], color=color, stroke_width=6),
        Line([0.4, 0, 0], [0.4, -0.14, 0], color=color, stroke_width=6),
    )
    return VGroup(bow, shaft, teeth)


def make_seal(color, text="sig"):
    return VGroup(Circle(radius=0.28, color=color, fill_opacity=0.85), Text(text, font_size=14, color=T.BG))


def make_person(name, color, pos):
    icon = Circle(radius=0.45, color=color, fill_opacity=0.6).move_to(pos)
    label = Text(name, font_size=22, color=color).next_to(icon, DOWN, buff=0.15)
    return VGroup(icon, label)


def make_villain(name, pos):
    icon = Triangle(color=T.DANGER, fill_opacity=0.5).scale(0.45).move_to(pos)
    label = Text(name, font_size=20, color=T.DANGER).next_to(icon, DOWN, buff=0.15)
    return VGroup(icon, label)


def make_ca(name, pos):
    box = RoundedRectangle(width=2.6, height=0.9, corner_radius=0.12, color=T.ENTITY_2, fill_opacity=0.25).move_to(pos)
    label = Text(name, font_size=22, weight=BOLD, color=T.ENTITY_2).move_to(box)
    return VGroup(box, label)


def make_cert(subject, key_color, issuer, seal_color, valid="2026-01-01 .. 2027-01-01"):
    """A certificate card. Index: 0 card, 1 header, 2 subject, 3 key row, 4 issuer, 5 validity, 6 signature row."""
    header = Text("CERTIFICATE", font_size=22, weight=BOLD, color=T.TEXT_PRIMARY)
    subj = Text(f"subject:   {subject}", font_size=18, font=MONO, color=T.TEXT_PRIMARY)
    key_lbl = Text("key:      ", font_size=18, font=MONO, color=T.TEXT_PRIMARY)
    key_row = VGroup(key_lbl, make_lock(key_color).scale(0.55)).arrange(RIGHT, buff=0.15)
    iss = Text(f"issuer:    {issuer}", font_size=18, font=MONO, color=T.TEXT_PRIMARY)
    val = Text(f"valid:     {valid}", font_size=18, font=MONO, color=T.TEXT_PRIMARY)
    sig_lbl = Text("signature:", font_size=18, font=MONO, color=T.TEXT_PRIMARY)
    sig_row = VGroup(sig_lbl, make_seal(seal_color).scale(0.8)).arrange(RIGHT, buff=0.2)
    rows = VGroup(header, subj, key_row, iss, val, sig_row).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    header.set_x(rows.get_x())
    card = RoundedRectangle(
        width=rows.width + 0.6, height=rows.height + 0.5, corner_radius=0.15,
        color=T.ENTITY_2, fill_color=T.BG_SURFACE, fill_opacity=1,
    ).move_to(rows)
    return VGroup(card, header, subj, key_row, iss, val, sig_row)


def make_check():
    return MathTex(r"\checkmark", font_size=44, color=T.SUCCESS)


def make_x():
    return MathTex(r"\times", font_size=48, color=T.DANGER)


class CertificatesAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        self.recap_problem()
        self.introduce_ca()
        self.issue_certificate()
        self.anatomy()
        self.verify_certificate()
        self.mallory_attempts()
        self.chain_of_trust()
        self.expiry_and_revocation()

        closing = VGroup(
            Text("public-key cryptography: protects the message", font_size=26),
            Text("certificates: say whose key it is", font_size=26, color=T.ENTITY_2),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover(
            text="Public-key cryptography protects the message. Certificates tell you whose key you are using. "
                 "Every padlock icon in your browser's address bar rests on both."
        ):
            self.play(FadeIn(closing[0], shift=UP))
            self.play(FadeIn(closing[1], shift=UP))
            self.wait(1)

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ── sections ─────────────────────────────────────────────────────────────

    def show_title(self):
        title = Text("Certificates & Certificate Authorities", font_size=40, weight=BOLD)
        subtitle = Text("who does this public key belong to?", font_size=24, color=T.WARNING).next_to(title, DOWN)

        with self.voiceover(
            text="Public-key cryptography lets anyone lock a message for Bob, using Bob's public key. "
                 "But how do you know a public key really is Bob's? "
                 "That is the job of certificates and certificate authorities."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def recap_problem(self):
        alice = make_person("Alice", T.ACCENT, [-5.5, 1.0, 0])
        bob = make_person("Bob", T.SUCCESS, [5.5, 1.0, 0])
        mallory = make_villain("Mallory", [0, 1.0, 0])
        lock = make_lock(T.DANGER).move_to([-3.6, 1.0, 0])
        question = Text("Bob's key?", font_size=18, color=T.TEXT_SECONDARY).next_to(lock, DOWN, buff=0.2)

        with self.voiceover(
            text="Last time, Mallory sat between Alice and Bob and swapped Bob's public key for her own. "
                 "A public key is just a number. Nothing in it says who owns it, so Alice was fooled."
        ):
            self.play(FadeIn(alice), FadeIn(bob), FadeIn(mallory))
            self.play(FadeIn(lock, scale=1.5), Write(question))

        idea = Text("Idea: someone Alice already trusts vouches for the key.", font_size=24, color=T.WARNING).move_to([0, -1.5, 0])
        with self.voiceover(
            text="The fix is to have someone Alice already trusts vouch for the key: "
                 "a trusted third party that states, in a way nobody can forge, that this key belongs to Bob."
        ):
            self.play(Write(idea))

        self.clear_all()

    def introduce_ca(self):
        ca = make_ca("TrustCo CA", [0, 2.7, 0])
        ca_lock = make_lock(T.ENTITY_2).next_to(ca, LEFT, buff=0.5)
        ca_key = make_key(T.ENTITY_2).next_to(ca, RIGHT, buff=0.5)
        lock_lbl = Text("CA public key", font_size=14, color=T.ENTITY_2).next_to(ca_lock, DOWN, buff=0.1)
        key_lbl = Text("CA private key", font_size=14, color=T.ENTITY_2).next_to(ca_key, DOWN, buff=0.15)

        with self.voiceover(
            text="That third party is a certificate authority, or C A. "
                 "Its whole business is checking who owns which key, and saying so."
        ):
            self.play(FadeIn(ca, shift=DOWN))

        with self.voiceover(
            text="Like everyone else, the C A has its own key pair. "
                 "It guards its private key above all else, because everything it signs depends on it."
        ):
            self.play(FadeIn(ca_lock), FadeIn(ca_key))
            self.play(Write(lock_lbl), Write(key_lbl))

        self.ca = VGroup(ca, ca_lock, ca_key, lock_lbl, key_lbl)
        self.ca_key = ca_key

    def issue_certificate(self):
        bob = make_person("Bob (bob.com)", T.SUCCESS, [5.3, 0.6, 0])
        bob_lock = make_lock(T.SUCCESS).move_to([4.8, -0.9, 0])
        bob_key = make_key(T.SUCCESS).move_to([6.0, -0.9, 0])

        with self.voiceover(text="Bob runs the website bob dot com. He generates his key pair, as before."):
            self.play(FadeIn(bob))
            self.play(FadeIn(bob_lock, scale=1.5), FadeIn(bob_key, scale=1.5))

        csr_lbl = Text("request: bob.com", font_size=16, font=MONO, color=T.TEXT_PRIMARY)
        csr_inner = VGroup(csr_lbl, bob_lock.copy().scale(0.55)).arrange(RIGHT, buff=0.2)
        csr_card = RoundedRectangle(width=csr_inner.width + 0.4, height=0.8, corner_radius=0.1,
                                    color=T.SUCCESS, fill_opacity=0.15).move_to(csr_inner)
        csr = VGroup(csr_card, csr_inner).move_to([3.0, -0.9, 0])

        with self.voiceover(
            text="He sends the C A a certificate signing request: his name, bob dot com, and his public key. "
                 "The private key stays at home."
        ):
            self.play(FadeIn(csr, shift=LEFT))
            self.play(csr.animate.move_to([2.6, 1.2, 0]))

        check = make_check().next_to(csr, LEFT, buff=0.3)
        check_lbl = Text("controls bob.com?", font_size=16, color=T.SUCCESS).next_to(check, LEFT, buff=0.2)
        with self.voiceover(
            text="Before signing anything, the C A checks that the requester really controls bob dot com, "
                 "for example by asking Bob to publish a random token on the site."
        ):
            self.play(Write(check_lbl), Write(check))

        cert = make_cert("bob.com", T.SUCCESS, "TrustCo CA", T.ENTITY_2).scale(0.6).move_to([-0.6, -1.2, 0])
        with self.voiceover(
            text="Satisfied, the C A writes Bob's name and public key into a document, and signs it with its own private key. "
                 "That signed document is Bob's certificate."
        ):
            self.play(self.ca_key.animate.next_to(csr, DOWN, buff=0.2))
            self.play(Transform(csr, cert), FadeOut(check), FadeOut(check_lbl))
            self.play(self.ca_key.animate.next_to(self.ca[0], RIGHT, buff=0.5))

        with self.voiceover(text="The certificate goes back to Bob. He will hand it to anyone who connects to his site."):
            self.play(csr.animate.scale(0.7).move_to([2.6, -1.6, 0]))

        self.clear_all()

    def anatomy(self):
        cert = make_cert("bob.com", T.SUCCESS, "TrustCo CA", T.ENTITY_2).scale(1.25).move_to([0, -0.2, 0])
        heading = Text("Inside a certificate", font_size=32, weight=BOLD).to_edge(UP)

        with self.voiceover(text="Let's look inside the certificate."):
            self.play(Write(heading), FadeIn(cert, scale=0.8))

        notes = [
            (cert[2], "The subject: the name this certificate is about, here bob dot com."),
            (cert[3], "The subject's public key: the padlock that belongs to that name."),
            (cert[4], "The issuer: who vouches for it, here TrustCo C A."),
            (cert[5], "The validity period: the certificate is only good between these two dates."),
            (cert[6], ("And the issuer's signature over all of the above. "
                      "Change a single character of the certificate and the signature no longer matches.")),
        ]
        for row, text in notes:
            with self.voiceover(text=text):
                self.play(Indicate(row, color=T.ENTITY_2, scale_factor=1.1))

        with self.voiceover(
            text="Real certificates use a format called X dot 509 and hold a few more fields, "
                 "but these are the ones that matter."
        ):
            self.wait(1)

        self.clear_all()

    def verify_certificate(self):
        alice = make_person("Alice", T.ACCENT, [-5.5, 1.8, 0])
        bob = make_person("bob.com", T.SUCCESS, [5.5, 1.8, 0])
        store_lock = make_lock(T.ENTITY_2)
        store_lbl = Text("TrustCo CA", font_size=14, color=T.ENTITY_2)
        store_items = VGroup(store_lock, store_lbl).arrange(DOWN, buff=0.1)
        store_box = SurroundingRectangle(store_items, color=T.ACCENT, buff=0.25)
        store_title = Text("trust store", font_size=16, color=T.ACCENT).next_to(store_box, UP, buff=0.1)
        store = VGroup(store_box, store_items, store_title).move_to([-5.5, -1.6, 0])

        with self.voiceover(text="Now Alice connects to bob dot com."):
            self.play(FadeIn(alice), FadeIn(bob))

        with self.voiceover(
            text="How can Alice check the C A's signature? She needs the C A's public key, and she already has it. "
                 "Her browser and operating system ship with a trust store: "
                 "a short list of certificate authorities' public keys, installed before she ever went online."
        ):
            self.play(FadeIn(store, shift=UP))

        cert = make_cert("bob.com", T.SUCCESS, "TrustCo CA", T.ENTITY_2).scale(0.6).move_to([3.0, -0.4, 0])
        with self.voiceover(text="Bob's site sends its certificate."):
            self.play(FadeIn(cert, shift=LEFT))
            self.play(cert.animate.move_to([-1.8, -0.4, 0]))

        checks = VGroup(
            Text("1. CA signature matches", font_size=20),
            Text("2. subject is bob.com", font_size=20),
            Text("3. today is within the dates", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([2.8, -0.4, 0])
        marks = VGroup(*[make_check().next_to(c, RIGHT, buff=0.25) for c in checks])

        with self.voiceover(
            text="First, Alice checks the signature on the certificate with TrustCo's public key from her trust store. "
                 "It matches, so TrustCo really issued this certificate, and nobody altered it since."
        ):
            self.play(Indicate(store_lock, color=T.ENTITY_2, scale_factor=1.4), Indicate(cert[6], color=T.ENTITY_2))
            self.play(Write(checks[0]), Write(marks[0]))

        with self.voiceover(text="Second, the subject is bob dot com, the site she meant to visit."):
            self.play(Indicate(cert[2], color=T.ENTITY_2))
            self.play(Write(checks[1]), Write(marks[1]))

        with self.voiceover(text="Third, the certificate has not expired."):
            self.play(Indicate(cert[5], color=T.ENTITY_2))
            self.play(Write(checks[2]), Write(marks[2]))

        with self.voiceover(
            text="All three pass, so Alice knows the padlock inside really belongs to bob dot com, "
                 "and she can use it safely."
        ):
            key_copy = cert[3][1].copy()
            self.play(key_copy.animate.scale(1.8).next_to(alice, RIGHT, buff=0.4))
            self.play(Indicate(key_copy, color=T.SUCCESS, scale_factor=1.3))

        self.play(FadeOut(cert), FadeOut(checks), FadeOut(marks), FadeOut(key_copy))
        self.alice = alice
        self.store = store

    def mallory_attempts(self):
        mallory = make_villain("Mallory", [0, 2.0, 0])
        with self.voiceover(text="What can Mallory do now? She has three options, and all of them fail."):
            self.play(FadeIn(mallory, shift=DOWN))

        attempts = [
            (
                make_cert("bob.com", T.DANGER, "TrustCo CA", T.ENTITY_2),
                3,
                "key swapped: the CA signature no longer matches",
                ("One: take Bob's real certificate and swap in her own public key. "
                "But the C A's signature covered the original key, so the signature check fails."),
            ),
            (
                make_cert("bob.com", T.DANGER, "Mallory CA", T.DANGER),
                4,
                "issuer is not in Alice's trust store",
                ("Two: write a certificate from scratch and sign it herself. "
                "But Alice's trust store has no key for Mallory, so the signature means nothing."),
            ),
            (
                make_cert("mallory.com", T.DANGER, "TrustCo CA", T.ENTITY_2),
                2,
                "genuine, but for the wrong name",
                ("Three: get a perfectly genuine certificate from TrustCo, for her own domain, mallory dot com. "
                "Every signature checks out, but the subject is not bob dot com, so Alice rejects it."),
            ),
        ]

        for cert, row, reason, text in attempts:
            cert.scale(0.6).move_to([0, -0.4, 0])
            bad = make_x().next_to(cert[row], RIGHT, buff=0.2)
            reason_lbl = Text(reason, font_size=20, color=T.DANGER).next_to(cert, DOWN, buff=0.3)
            with self.voiceover(text=text):
                self.play(FadeIn(cert, shift=DOWN))
                self.play(Indicate(cert[row], color=T.DANGER))
                self.play(Write(bad), Write(reason_lbl))
            self.play(FadeOut(cert), FadeOut(bad), FadeOut(reason_lbl))

        with self.voiceover(
            text="To fool Alice, Mallory would need TrustCo's private key, "
                 "or would have to talk TrustCo into vouching for a domain she doesn't control."
        ):
            self.wait(1)

        self.clear_all()

    def chain_of_trust(self):
        heading = Text("Chain of trust", font_size=32, weight=BOLD).to_edge(UP)

        root = make_cert("TrustCo Root", T.ENTITY_2, "TrustCo Root", T.ENTITY_2).scale(0.7)
        inter = make_cert("TrustCo Issuing", T.ENTITY_3, "TrustCo Root", T.ENTITY_2).scale(0.7)
        leaf = make_cert("bob.com", T.SUCCESS, "TrustCo Issuing", T.ENTITY_3).scale(0.7)
        chain = VGroup(root, inter, leaf).arrange(RIGHT, buff=1.1)
        if chain.width > 13.2:
            chain.scale_to_fit_width(13.2)
        chain.move_to([0, 0.9, 0])
        a1 = Arrow(root.get_right(), inter.get_left(), buff=0.1, color=T.ENTITY_2)
        a2 = Arrow(inter.get_right(), leaf.get_left(), buff=0.1, color=T.ENTITY_3)
        s1 = Text("signs", font_size=16, color=T.ENTITY_2).next_to(a1, UP, buff=0.1)
        s2 = Text("signs", font_size=16, color=T.ENTITY_3).next_to(a2, UP, buff=0.1)

        tags = VGroup(
            Text("root: self-signed,\nkey kept offline", font_size=18, color=T.ENTITY_2).next_to(root, DOWN, buff=0.3),
            Text("intermediate:\ndoes the daily signing", font_size=18, color=T.ENTITY_3).next_to(inter, DOWN, buff=0.3),
            Text("leaf:\nthe site's certificate", font_size=18, color=T.SUCCESS).next_to(leaf, DOWN, buff=0.3),
        )

        store_items = VGroup(make_lock(T.ENTITY_2), Text("TrustCo Root", font_size=14, color=T.ENTITY_2)).arrange(DOWN, buff=0.1)
        store_box = SurroundingRectangle(store_items, color=T.ACCENT, buff=0.2)
        store_title = Text("Alice's trust store", font_size=16, color=T.ACCENT).next_to(store_box, RIGHT, buff=0.2)
        store = VGroup(store_box, store_items, store_title)
        store.next_to(tags[0], DOWN, buff=0.35).align_to(root, LEFT)

        with self.voiceover(
            text="In practice there is more than one link. "
                 "A C A's most precious key, its root key, is far too valuable to use every day."
        ):
            self.play(Write(heading))
            self.play(FadeIn(root))

        with self.voiceover(
            text="The root certificate is self-signed: its issuer is itself. "
                 "It is trusted not because of its signature, but because it sits in Alice's trust store. "
                 "The root's private key is locked away offline."
        ):
            self.play(Indicate(VGroup(root[2], root[4]), color=T.ENTITY_2), Write(tags[0]))
            self.play(FadeIn(store, shift=UP))

        with self.voiceover(
            text="The root signs a certificate for an intermediate C A, which does the day-to-day signing."
        ):
            self.play(GrowArrow(a1), Write(s1), FadeIn(inter))
            self.play(Write(tags[1]))

        with self.voiceover(text="The intermediate signs Bob's certificate, the leaf of the chain."):
            self.play(GrowArrow(a2), Write(s2), FadeIn(leaf))
            self.play(Write(tags[2]))

        with self.voiceover(
            text="Bob's server sends the leaf and the intermediate together. "
                 "Alice checks each signature with the key one step up the chain, "
                 "until she reaches a root that is in her trust store."
        ):
            self.play(Indicate(leaf, color=T.SUCCESS, scale_factor=1.05))
            self.play(Indicate(inter, color=T.ENTITY_3, scale_factor=1.05))
            self.play(Indicate(root, color=T.ENTITY_2, scale_factor=1.05))
            self.play(Indicate(store_items, color=T.SUCCESS, scale_factor=1.3))

        with self.voiceover(
            text="If the intermediate's key is ever stolen, the root can cut it off and issue a new one, "
                 "without every browser in the world needing an update."
        ):
            self.wait(1)

        self.clear_all()

    def expiry_and_revocation(self):
        heading = Text("When keys go bad", font_size=32, weight=BOLD).to_edge(UP)
        items = VGroup(
            Text("expiry: certificates last months, not decades", font_size=24),
            Text("revocation: the CA publishes a list of cancelled certificates", font_size=24),
            Text("a stolen private key is only useful until it expires or is revoked", font_size=24, color=T.WARNING),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(heading, DOWN, buff=0.8)

        with self.voiceover(
            text="Finally, what if Bob's private key is stolen? Two safety nets help."
        ):
            self.play(Write(heading))

        with self.voiceover(
            text="Certificates expire. Many websites' certificates are valid for only a few months, "
                 "so a stolen key cannot be abused forever."
        ):
            self.play(FadeIn(items[0], shift=RIGHT))

        with self.voiceover(
            text="And Bob can ask the C A to revoke his certificate early. "
                 "The C A publishes which certificates it has cancelled, and clients can check that list."
        ):
            self.play(FadeIn(items[1], shift=RIGHT))

        with self.voiceover(text="Together they put a time limit on any mistake."):
            self.play(FadeIn(items[2], shift=RIGHT))

        self.clear_all()
