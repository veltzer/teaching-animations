import pathlib
import sys

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared" / "shared-themes"))
from manim_themes import BASE, T, apply_defaults

apply_defaults()


class PipesAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        writer, reader, buf, slots = self.draw_actors()
        self.write_some(writer, slots)
        self.read_some(reader, slots)
        self.fill_to_block(writer, buf, slots)
        self.drain_to_block(reader, buf, slots)
        self.closing()

    def show_title(self):
        title = Text("Pipes", font_size=52, weight=BOLD)
        subtitle = Text(
            "a kernel buffer with two ends",
            font_size=26,
            color=T.WARNING,
        ).next_to(title, DOWN)

        with self.voiceover(
            text="A pipe is a fixed-size buffer inside the kernel with two file descriptors — "
                 "one for writing, one for reading. The writer pours bytes in one end, "
                 "the reader takes them out the other."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def draw_actors(self):
        writer_box = RoundedRectangle(width=2.4, height=1.2, corner_radius=0.15, color=T.ACCENT, fill_opacity=0.5)
        writer_box.move_to(LEFT * 5)
        writer_lbl = Text("writer", font_size=20).move_to(writer_box.get_center() + UP * 0.2)
        writer_fd = Text("fd[1]", font_size=18, color=T.WARNING, font=BASE["font-mono"]).move_to(writer_box.get_center() + DOWN * 0.2)
        writer = VGroup(writer_box, writer_lbl, writer_fd)

        reader_box = RoundedRectangle(width=2.4, height=1.2, corner_radius=0.15, color=T.SUCCESS, fill_opacity=0.5)
        reader_box.move_to(RIGHT * 5)
        reader_lbl = Text("reader", font_size=20).move_to(reader_box.get_center() + UP * 0.2)
        reader_fd = Text("fd[0]", font_size=18, color=T.WARNING, font=BASE["font-mono"]).move_to(reader_box.get_center() + DOWN * 0.2)
        reader = VGroup(reader_box, reader_lbl, reader_fd)

        # Buffer in the middle: 8 slots
        slots = VGroup()
        for i in range(8):
            slot = Rectangle(width=0.55, height=0.7, color=T.BORDER, fill_opacity=0.15)
            slot.move_to(LEFT * 1.95 + RIGHT * (i * 0.6))
            slots.add(slot)

        buf_lbl = Text("kernel pipe buffer (capacity = 8)", font_size=18, color=T.BORDER).next_to(slots, UP, buff=0.4)
        buf = VGroup(slots, buf_lbl)

        with self.voiceover(
            text="On the left, the writer process. On the right, the reader. "
                 "In the middle, the kernel's pipe buffer — say, eight slots wide."
        ):
            self.play(FadeIn(writer, shift=RIGHT), FadeIn(reader, shift=LEFT))
            self.play(Create(slots), Write(buf_lbl))

        return writer, reader, buf, slots

    def _fill_slot(self, slot, char, color):
        new_slot = Rectangle(width=slot.width, height=slot.height, color=color, fill_opacity=0.6).move_to(slot.get_center())
        text = Text(char, font_size=22, font=BASE["font-mono"], color=T.TEXT_PRIMARY).move_to(slot.get_center())
        self.play(Transform(slot, new_slot), FadeIn(text, shift=DOWN), run_time=0.25)
        return text

    def _empty_slot(self, slot, text):
        new_slot = Rectangle(width=slot.width, height=slot.height, color=T.BORDER, fill_opacity=0.15).move_to(slot.get_center())
        self.play(Transform(slot, new_slot), FadeOut(text), run_time=0.25)

    def write_some(self, writer, slots):
        with self.voiceover(text="The writer calls write of three bytes — H, I, exclamation."):
            self.play(Indicate(writer, color=T.ACCENT_DIM, scale_factor=1.05))
            t1 = self._fill_slot(slots[0], "H", T.ACCENT)
            t2 = self._fill_slot(slots[1], "i", T.ACCENT)
            t3 = self._fill_slot(slots[2], "!", T.ACCENT)
        self.write_chars = [t1, t2, t3]

    def read_some(self, reader, slots):
        with self.voiceover(text="The reader calls read of three bytes — and gets H, I, exclamation, in order."):
            self.play(Indicate(reader, color=T.SUCCESS_DIM, scale_factor=1.05))
            self._empty_slot(slots[0], self.write_chars[0])
            self._empty_slot(slots[1], self.write_chars[1])
            self._empty_slot(slots[2], self.write_chars[2])

    def fill_to_block(self, writer, buf, slots):
        with self.voiceover(
            text="What if the writer is faster than the reader? It keeps filling the buffer. "
                 "When all eight slots are full, the next write call blocks."
        ):
            chars = list("ABCDEFGH")
            for slot, c in zip(slots, chars):
                self._fill_slot(slot, c, T.ACCENT)

        block_lbl = Text("write() blocks → buffer full", font_size=22, color=T.DANGER).next_to(buf, DOWN, buff=0.4)
        with self.voiceover(
            text="The kernel parks the writer process — it goes to sleep until space appears."
        ):
            self.play(Write(block_lbl))

        self.block_lbl = block_lbl

    def drain_to_block(self, reader, buf, slots):
        with self.voiceover(
            text="The reader catches up by draining the buffer."
        ):
            self.play(FadeOut(self.block_lbl))
            for slot in slots:
                # Each slot's text: it was added by _fill_slot; we need to find and remove it.
                # Use a cheap reset: replace with empty slot directly.
                new_slot = Rectangle(width=slot.width, height=slot.height, color=T.BORDER, fill_opacity=0.15).move_to(slot.get_center())
                self.play(Transform(slot, new_slot), run_time=0.15)

        block_lbl = Text("read() blocks → buffer empty", font_size=22, color=T.DANGER).next_to(buf, DOWN, buff=0.4)
        with self.voiceover(
            text="And the symmetric situation: when the buffer is empty, the next read blocks. "
                 "The reader sleeps until the writer puts something in."
        ):
            self.play(Write(block_lbl))

    def closing(self):
        msg = Text(
            "blocking is the synchronization",
            font_size=26, color=T.WARNING,
        ).to_edge(DOWN, buff=0.7)

        with self.voiceover(
            text="The blocking behavior is what makes pipes useful for synchronization. "
                 "Two processes hand data back and forth, and the kernel's buffer paces them — "
                 "neither outpaces the other for long."
        ):
            self.play(Write(msg))
            self.wait(2)
