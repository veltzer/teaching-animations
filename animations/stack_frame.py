from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class StackFrameAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        self.show_source()
        cells = self.draw_main_frame()
        self.call_foo(cells)
        self.return_from_foo(cells)
        self.closing()

    def show_title(self):
        title = Text("The Stack Frame", font_size=48, weight=BOLD)
        subtitle = Text(
            "what a function call looks like in memory",
            font_size=26,
            color=YELLOW,
        ).next_to(title, DOWN)

        with self.voiceover(
            text="Every time a function is called, the CPU pushes a chunk of bookkeeping onto "
                 "the stack — locals, the return address, the saved frame pointer. "
                 "That chunk is the function's stack frame."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def show_source(self):
        code_lines = VGroup(
            Text("int foo(int x) {", font_size=22, font="Monospace", color=WHITE),
            Text("    int y = x + 1;", font_size=22, font="Monospace", color=BLUE_A),
            Text("    return y;", font_size=22, font="Monospace", color=BLUE_A),
            Text("}", font_size=22, font="Monospace", color=WHITE),
            Text("", font_size=22),
            Text("int main() {", font_size=22, font="Monospace", color=WHITE),
            Text("    int z = foo(7);", font_size=22, font="Monospace", color=GREEN_A),
            Text("    return 0;", font_size=22, font="Monospace", color=WHITE),
            Text("}", font_size=22, font="Monospace", color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        with self.voiceover(
            text="Here is a tiny C program. Main calls foo with the argument seven. "
                 "Foo adds one and returns. Let us watch what the stack does."
        ):
            for line in code_lines:
                self.play(Write(line), run_time=0.3)

        self.wait(0.5)
        self.play(FadeOut(code_lines))

    def _make_cell(self, label, value, color, position):
        box = Rectangle(width=3.0, height=0.55, color=color, fill_opacity=0.25).move_to(position)
        val = Text(value, font_size=18, font="Monospace", color=color).move_to(box.get_center())
        lbl = Text(label, font_size=16, color=color).next_to(box, LEFT, buff=0.4)
        return VGroup(box, val), lbl

    def draw_main_frame(self):
        title = Text("stack (grows downward)", font_size=20, color=GREY).to_edge(UP, buff=0.5)
        high = Text("high addresses", font_size=14, color=GREY).to_edge(LEFT, buff=0.4).shift(UP * 2.5)
        low = Text("low addresses", font_size=14, color=GREY).to_edge(LEFT, buff=0.4).shift(DOWN * 2.5)

        # Main's frame
        c_ret, l_ret = self._make_cell("return addr (caller)", "0x4011a0", YELLOW, UP * 1.8)
        c_fp, l_fp = self._make_cell("saved frame ptr", "0x7ffe40", PURPLE, UP * 1.2)
        c_z, l_z = self._make_cell("z (local)", "?", GREEN, UP * 0.6)

        sp = Arrow(LEFT * 4 + UP * 0.6, c_z[0].get_left() + LEFT * 0.05, color=YELLOW, buff=0.05, stroke_width=5)
        sp_lbl = Text("rsp", font_size=18, font="Monospace", color=YELLOW).next_to(sp, LEFT, buff=0.1)

        with self.voiceover(
            text="Main has its own stack frame. At the top sits the return address — "
                 "where to jump back when main itself returns. Below that, the saved frame pointer. "
                 "Below that, main's local variable z, currently uninitialized."
        ):
            self.play(Write(title), Write(high), Write(low))
            for cell, label in [(c_ret, l_ret), (c_fp, l_fp), (c_z, l_z)]:
                self.play(FadeIn(cell), Write(label), run_time=0.35)

        with self.voiceover(text="The stack pointer points to the top — meaning the lowest address — of main's frame."):
            self.play(GrowArrow(sp), Write(sp_lbl))

        return {
            "title": title, "high": high, "low": low,
            "main_ret": (c_ret, l_ret),
            "main_fp": (c_fp, l_fp),
            "main_z": (c_z, l_z),
            "sp": sp, "sp_lbl": sp_lbl,
        }

    def call_foo(self, cells):
        # Push return address, then saved fp, then arg x and local y
        c_ret, l_ret = self._make_cell("return addr (in main)", "0x40120f", RED, ORIGIN)
        c_fp, l_fp = self._make_cell("saved frame ptr", "0x7ffe28", PURPLE, DOWN * 0.6)
        c_x, l_x = self._make_cell("x (arg)", "7", BLUE, DOWN * 1.2)
        c_y, l_y = self._make_cell("y (local)", "8", BLUE, DOWN * 1.8)

        with self.voiceover(
            text="Main calls foo. The call instruction pushes the return address — "
                 "the instruction in main right after the call — onto the stack."
        ):
            self.play(FadeIn(c_ret), Write(l_ret))

        with self.voiceover(
            text="Foo's prologue pushes main's frame pointer, allocates space for the argument x, "
                 "and the local y. The stack pointer moves down to the new top of the stack."
        ):
            self.play(FadeIn(c_fp), Write(l_fp), run_time=0.4)
            self.play(FadeIn(c_x), Write(l_x), run_time=0.4)
            self.play(FadeIn(c_y), Write(l_y), run_time=0.4)

        new_sp = Arrow(LEFT * 4 + DOWN * 1.8, c_y[0].get_left() + LEFT * 0.05, color=YELLOW, buff=0.05, stroke_width=5)
        new_sp_lbl = Text("rsp", font_size=18, font="Monospace", color=YELLOW).next_to(new_sp, LEFT, buff=0.1)

        with self.voiceover(
            text="The stack pointer now points to the bottom — the top of foo's frame. "
                 "Foo's locals are live; main's are still there above, untouched."
        ):
            self.play(Transform(cells["sp"], new_sp), Transform(cells["sp_lbl"], new_sp_lbl))

        cells["foo_ret"] = (c_ret, l_ret)
        cells["foo_fp"] = (c_fp, l_fp)
        cells["foo_x"] = (c_x, l_x)
        cells["foo_y"] = (c_y, l_y)

    def return_from_foo(self, cells):
        with self.voiceover(
            text="When foo executes its return, the epilogue pops y, x, the saved frame pointer, "
                 "and finally the return address — which the CPU jumps to. "
                 "Foo's frame is gone."
        ):
            for key in ["foo_y", "foo_x", "foo_fp", "foo_ret"]:
                cell, label = cells[key]
                self.play(FadeOut(cell), FadeOut(label), run_time=0.25)

        # Restore sp
        c_z, _ = cells["main_z"]
        new_sp = Arrow(LEFT * 4 + UP * 0.6, c_z[0].get_left() + LEFT * 0.05, color=YELLOW, buff=0.05, stroke_width=5)
        new_sp_lbl = Text("rsp", font_size=18, font="Monospace", color=YELLOW).next_to(new_sp, LEFT, buff=0.1)
        self.play(Transform(cells["sp"], new_sp), Transform(cells["sp_lbl"], new_sp_lbl))

        # Update z's value
        new_z_val = Text("8", font_size=18, font="Monospace", color=GREEN).move_to(c_z[1].get_center())
        with self.voiceover(text="Foo's return value — eight — lands in main's local z."):
            self.play(Transform(c_z[1], new_z_val))

    def closing(self):
        msg = Text(
            "the stack is just a stack — push to call, pop to return",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.5)

        with self.voiceover(
            text="The stack frame is the entire mechanism behind nested function calls. "
                 "The same memory region is reused over and over — push when you call, "
                 "pop when you return. Recursion, locals, return addresses — all of it lives here."
        ):
            self.play(Write(msg))
            self.wait(2)
