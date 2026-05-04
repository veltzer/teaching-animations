from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class BufferOverflowAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        self.show_source_code()
        frame_cells, frame_labels = self.draw_stack_frame()
        self.benign_input(frame_cells, frame_labels)
        self.reset_frame(frame_cells)
        self.malicious_input(frame_cells, frame_labels)
        self.closing()

    def show_title(self):
        title = Text("The Buffer Overflow", font_size=44, weight=BOLD)
        subtitle = Text(
            "smashing the stack to hijack control flow",
            font_size=26,
            color=YELLOW,
        ).next_to(title, DOWN)

        with self.voiceover(
            text="A buffer overflow is what happens when a program writes past the end of an array. "
                 "On the stack, that overwrites whatever sits next to the array — "
                 "and what sits next to it can be very valuable."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def show_source_code(self):
        code_lines = VGroup(
            Text("void greet(char *name) {", font_size=22, font="Monospace", color=WHITE),
            Text("    char buf[8];", font_size=22, font="Monospace", color=BLUE_A),
            Text("    strcpy(buf, name);   // no bounds check!", font_size=22, font="Monospace", color=RED_A),
            Text("    printf(\"hi %s\", buf);", font_size=22, font="Monospace", color=WHITE),
            Text("}", font_size=22, font="Monospace", color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        with self.voiceover(
            text="Here is our victim function. It declares an eight-byte buffer on the stack, "
                 "and copies a string into it using strcpy — which has no idea how big the destination is. "
                 "If the input is longer than eight bytes, strcpy will happily keep writing."
        ):
            for line in code_lines:
                self.play(Write(line), run_time=0.5)

        self.wait(0.5)
        self.play(FadeOut(code_lines))

    def draw_stack_frame(self):
        title = Text("stack frame of greet()", font_size=22, color=GREY).to_edge(UP, buff=0.5)

        grow_lbl = Text("stack grows ↓", font_size=18, color=GREY).to_edge(LEFT, buff=0.5).shift(UP * 0.5)
        addr_lbl_high = Text("high address", font_size=16, color=GREY).to_edge(RIGHT, buff=0.5).shift(UP * 2.2)
        addr_lbl_low = Text("low address", font_size=16, color=GREY).to_edge(RIGHT, buff=0.5).shift(DOWN * 2.6)

        cells = VGroup()
        labels = VGroup()
        positions_y = [2.0, 1.3, 0.6, -0.1, -0.8, -1.5, -2.2]
        cell_specs = [
            ("saved return addr", "0x401abc", YELLOW, 1.5),
            ("saved frame ptr",   "0x7ffe10", PURPLE, 1.5),
            ("buf[6..7]", "?", BLUE, 1.0),
            ("buf[4..5]", "?", BLUE, 1.0),
            ("buf[2..3]", "?", BLUE, 1.0),
            ("buf[0..1]", "?", BLUE, 1.0),
        ]

        for i, (lbl_text, val_text, color, _w) in enumerate(cell_specs):
            box = Rectangle(width=2.6, height=0.6, color=color, fill_opacity=0.25).move_to(UP * positions_y[i])
            val = Text(val_text, font_size=18, font="Monospace", color=color).move_to(box.get_center())
            cell = VGroup(box, val)
            lbl = Text(lbl_text, font_size=16, color=color).next_to(box, LEFT, buff=0.4)
            cells.add(cell)
            labels.add(lbl)

        with self.voiceover(
            text="When greet is called, the CPU sets up a stack frame that looks like this. "
                 "At the bottom of the frame is buf — eight bytes of room for our string. "
                 "Just above buf is the saved frame pointer. "
                 "And just above that is the saved return address — "
                 "the place the CPU will jump to when greet returns."
        ):
            self.play(Write(title), Write(grow_lbl), Write(addr_lbl_high), Write(addr_lbl_low))
            for cell, lbl in zip(cells, labels):
                self.play(FadeIn(cell), Write(lbl), run_time=0.3)

        self.frame_title = title
        self.grow_lbl = grow_lbl
        self.addr_lbl_high = addr_lbl_high
        self.addr_lbl_low = addr_lbl_low
        return cells, labels

    def _set_cell(self, cell, new_text, color):
        box = cell[0]
        new_val = Text(new_text, font_size=18, font="Monospace", color=color).move_to(box.get_center())
        new_box = Rectangle(width=box.width, height=box.height, color=color, fill_opacity=0.45).move_to(box.get_center())
        self.play(Transform(cell[0], new_box), Transform(cell[1], new_val), run_time=0.35)

    def benign_input(self, cells, labels):
        heading = Text("Case 1: input = \"Alice\" (5 bytes + null)", font_size=22, color=GREEN)
        heading.to_edge(DOWN, buff=0.5)

        with self.voiceover(
            text="First, a benign input. The user types Alice — five characters plus a null terminator, "
                 "six bytes total. That fits comfortably inside the eight-byte buffer."
        ):
            self.play(Write(heading))

        # cells order: 0=ret, 1=fp, 2=buf[6..7], 3=buf[4..5], 4=buf[2..3], 5=buf[0..1]
        self._set_cell(cells[5], "'A' 'l'", BLUE)
        self._set_cell(cells[4], "'i' 'c'", BLUE)
        self._set_cell(cells[3], "'e' \\0", BLUE)
        # cells[2] (buf[6..7]) untouched

        check = Text("✓ saved return address intact", font_size=22, color=GREEN).next_to(heading, UP, buff=0.3)
        with self.voiceover(
            text="The buffer holds the string, the saved return address up top is untouched, "
                 "and when greet returns, control flow goes back to the caller — exactly as intended."
        ):
            self.play(Indicate(cells[0], color=GREEN, scale_factor=1.1))
            self.play(Write(check))

        self.wait(0.5)
        self.play(FadeOut(heading), FadeOut(check))
        self.benign_check = None

    def reset_frame(self, cells):
        self._set_cell(cells[5], "?", BLUE)
        self._set_cell(cells[4], "?", BLUE)
        self._set_cell(cells[3], "?", BLUE)
        self._set_cell(cells[2], "?", BLUE)
        # restore the saved fp and return addr to their original values
        self._set_cell(cells[1], "0x7ffe10", PURPLE)
        self._set_cell(cells[0], "0x401abc", YELLOW)

    def malicious_input(self, cells, labels):
        heading = Text("Case 2: input = 24 bytes of attacker-chosen data", font_size=22, color=RED)
        heading.to_edge(DOWN, buff=0.5)

        with self.voiceover(
            text="Now the attacker sends a much longer input. Twenty-four bytes — "
                 "carefully chosen, byte by byte."
        ):
            self.play(Write(heading))

        # First 8 bytes: fill the buffer with junk
        with self.voiceover(text="The first eight bytes fill the buffer."):
            self._set_cell(cells[5], "AA AA", RED)
            self._set_cell(cells[4], "AA AA", RED)
            self._set_cell(cells[3], "AA AA", RED)
            self._set_cell(cells[2], "AA AA", RED)

        # Next 8 bytes: clobber the saved frame pointer
        with self.voiceover(
            text="The next eight bytes spill upward and overwrite the saved frame pointer. "
                 "Strcpy does not stop — it has no idea anything is wrong."
        ):
            self._set_cell(cells[1], "BB BB BB BB", RED)

        # Final 8 bytes: clobber the return address with attacker's address
        with self.voiceover(
            text="And the final bytes overwrite the saved return address — "
                 "with the address of code the attacker wants to run."
        ):
            self._set_cell(cells[0], "0x7fffd000", RED)
            arrow = Arrow(
                start=cells[0][0].get_right() + RIGHT * 0.4,
                end=cells[0][0].get_right(),
                color=RED, buff=0.05,
            )
            shellcode_lbl = Text("→ attacker's shellcode", font_size=18, color=RED).next_to(arrow, RIGHT, buff=0.1)
            self.play(GrowArrow(arrow), Write(shellcode_lbl))

        with self.voiceover(
            text="When greet finally returns, the CPU pops what it believes is the saved return address — "
                 "and obediently jumps there. Except it is not the caller anymore. "
                 "It is the attacker's code, executing with the privileges of the victim process."
        ):
            self.play(Indicate(cells[0], color=RED, scale_factor=1.15))
            self.play(Flash(cells[0].get_center(), color=RED, flash_radius=1.0))

        cross = Text("✗ control flow hijacked", font_size=22, color=RED).next_to(heading, UP, buff=0.3)
        self.play(Write(cross))

        self.wait(0.5)
        self.play(FadeOut(heading), FadeOut(cross), FadeOut(arrow), FadeOut(shellcode_lbl))

    def closing(self):
        msg = Text(
            "no separation between data and control",
            font_size=26, color=YELLOW,
        ).to_edge(DOWN, buff=1.5)
        msg2 = Text(
            "user input + saved return address share one stack",
            font_size=22, color=GREY,
        ).next_to(msg, DOWN, buff=0.3)

        with self.voiceover(
            text="The root cause is simple. The same stack holds both data — the buffer — "
                 "and control — the return address. There is no boundary between them. "
                 "If you can write past the end of the buffer, you can rewrite where the program goes next."
        ):
            self.play(Write(msg))
            self.play(Write(msg2))

        with self.voiceover(
            text="Defenses you will see in later videos — stack canaries, non-executable stacks, "
                 "address space layout randomization — all exist because of this one mistake."
        ):
            self.wait(2)
