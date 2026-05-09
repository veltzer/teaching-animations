from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared" / "shared-themes"))
from manim_themes import T, BASE, apply_defaults
apply_defaults()


class TcpHandshakeAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        client, server = self.draw_endpoints()
        self.syn(client, server)
        self.syn_ack(client, server)
        self.ack(client, server)
        self.connection_open(client, server)
        self.closing()

    def show_title(self):
        title = Text("TCP three-way handshake", font_size=44, weight=BOLD)
        subtitle = Text(
            "SYN, SYN-ACK, ACK",
            font_size=26,
            color=T.WARNING,
            font=BASE["font-mono"],
        ).next_to(title, DOWN)

        with self.voiceover(
            text="Before any data flows over a TCP connection, the two endpoints exchange "
                 "three small packets to agree on starting sequence numbers and confirm "
                 "they can both send and receive. This is the three-way handshake."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def draw_endpoints(self):
        client_box = RoundedRectangle(width=2.4, height=1.2, corner_radius=0.15, color=T.ACCENT, fill_opacity=0.5)
        client_box.move_to(LEFT * 5 + UP * 2.5)
        client_lbl = Text("client", font_size=22).move_to(client_box.get_center() + UP * 0.2)
        client_state = Text("CLOSED", font_size=16, color=T.BORDER, font=BASE["font-mono"]).move_to(client_box.get_center() + DOWN * 0.2)
        client = VGroup(client_box, client_lbl, client_state)

        server_box = RoundedRectangle(width=2.4, height=1.2, corner_radius=0.15, color=T.SUCCESS, fill_opacity=0.5)
        server_box.move_to(RIGHT * 5 + UP * 2.5)
        server_lbl = Text("server", font_size=22).move_to(server_box.get_center() + UP * 0.2)
        server_state = Text("LISTEN", font_size=16, color=T.SUCCESS, font=BASE["font-mono"]).move_to(server_box.get_center() + DOWN * 0.2)
        server = VGroup(server_box, server_lbl, server_state)

        # Vertical timelines
        client_line = DashedLine(client_box.get_bottom(), client_box.get_bottom() + DOWN * 5.5, color=T.ACCENT, dash_length=0.15)
        server_line = DashedLine(server_box.get_bottom(), server_box.get_bottom() + DOWN * 5.5, color=T.SUCCESS, dash_length=0.15)

        with self.voiceover(
            text="On the left, the client. On the right, the server, already listening on a port."
        ):
            self.play(FadeIn(client, shift=DOWN), FadeIn(server, shift=DOWN))
            self.play(Create(client_line), Create(server_line))

        # Stash state texts so we can mutate them
        client.state = client_state
        server.state = server_state
        client.line_top = client_box.get_bottom()
        server.line_top = server_box.get_bottom()
        return client, server

    def _packet(self, src, dst, y_offset, label_text, color):
        start = src.line_top + DOWN * y_offset
        end = dst.line_top + DOWN * (y_offset + 0.8)
        arrow = Arrow(start=start, end=end, color=color, buff=0.05, stroke_width=4)
        # Place label near the arrow midpoint
        mid = (start + end) / 2
        label = Text(label_text, font_size=18, color=color, font=BASE["font-mono"]).move_to(mid + UP * 0.05)
        # Slight offset so it doesn't overlap the arrow
        label.shift(UP * 0.25)
        return arrow, label

    def _set_state(self, endpoint, new_text, color):
        new_state = Text(new_text, font_size=16, color=color, font=BASE["font-mono"]).move_to(endpoint.state.get_center())
        self.play(Transform(endpoint.state, new_state), run_time=0.4)

    def syn(self, client, server):
        arrow, label = self._packet(client, server, 0.5, "SYN  seq=100", T.ACCENT)

        with self.voiceover(
            text="The client sends a SYN — short for synchronize. "
                 "It picks a random starting sequence number — say, one hundred — and sends it."
        ):
            self.play(GrowArrow(arrow), Write(label))
            self._set_state(client, "SYN_SENT", T.WARNING)

    def syn_ack(self, client, server):
        arrow, label = self._packet(server, client, 1.6, "SYN  seq=500\nACK  ack=101", T.SUCCESS)

        with self.voiceover(
            text="The server replies with a single packet that has both flags set — SYN and ACK. "
                 "The SYN carries the server's own random sequence number, five hundred. "
                 "The ACK acknowledges the client's SYN by acking sequence one-oh-one — "
                 "the next byte the server expects."
        ):
            self.play(GrowArrow(arrow), Write(label))
            self._set_state(server, "SYN_RECVD", T.WARNING)

    def ack(self, client, server):
        arrow, label = self._packet(client, server, 2.8, "ACK  ack=501", T.ACCENT)

        with self.voiceover(
            text="The client acknowledges the server's SYN with a final ACK. "
                 "It acks five-oh-one — the next byte it expects from the server."
        ):
            self.play(GrowArrow(arrow), Write(label))
            self._set_state(client, "ESTABLISHED", T.SUCCESS)

    def connection_open(self, client, server):
        with self.voiceover(
            text="When the server receives that final ACK, it transitions to ESTABLISHED too. "
                 "Now the connection is fully open in both directions."
        ):
            self._set_state(server, "ESTABLISHED", T.SUCCESS)

        banner = Text("connection open — data may flow", font_size=22, color=T.WARNING).to_edge(DOWN, buff=0.6)
        with self.voiceover(text="Either side can now send data."):
            self.play(Write(banner))

    def closing(self):
        with self.voiceover(
            text="Three packets, two random numbers, both sides confirmed. "
                 "From here on, every byte has a sequence number, and every received byte "
                 "gets acknowledged. That is how TCP keeps two endpoints in sync."
        ):
            self.wait(2)
