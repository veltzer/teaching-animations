from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class ForkAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        parent = self.draw_parent()
        child = self.do_fork(parent)
        self.show_return_values(parent, child)
        self.show_cow(parent, child)
        self.closing()

    def show_title(self):
        title = Text("fork()", font_size=56, weight=BOLD, font="Monospace")
        subtitle = Text(
            "how Unix duplicates a process",
            font_size=26,
            color=YELLOW,
        ).next_to(title, DOWN)

        with self.voiceover(
            text="The fork system call creates a new process by duplicating the calling one. "
                 "Two processes — the parent and the child — leave fork in nearly identical states. "
                 "Almost. The return value is what tells them apart."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def _make_proc(self, label, color, position):
        box = RoundedRectangle(width=3.0, height=1.5, corner_radius=0.15, color=color, fill_opacity=0.4)
        box.move_to(position)
        lbl = Text(label, font_size=22).move_to(box.get_center() + UP * 0.25)
        pid = Text("pid 100", font_size=18, color=YELLOW, font="Monospace").move_to(box.get_center() + DOWN * 0.25)
        return VGroup(box, lbl, pid)

    def draw_parent(self):
        proc = self._make_proc("parent", BLUE_C, ORIGIN)

        with self.voiceover(
            text="We start with one process. The kernel knows it as PID one hundred."
        ):
            self.play(FadeIn(proc, shift=DOWN))

        call = Text("rc = fork();", font_size=24, font="Monospace", color=YELLOW).move_to(DOWN * 2.5)
        with self.voiceover(
            text="It calls fork."
        ):
            self.play(Write(call))

        self.fork_call = call
        return proc

    def do_fork(self, parent):
        # Move parent left, create child on the right
        with self.voiceover(
            text="The kernel makes a near-perfect copy. Same code, same heap, same open files, same "
                 "register state. The only difference is the new PID."
        ):
            self.play(parent.animate.shift(LEFT * 3.5))

        child = RoundedRectangle(width=3.0, height=1.5, corner_radius=0.15, color=GREEN_C, fill_opacity=0.4)
        child.move_to(RIGHT * 3.5)
        child_lbl = Text("child", font_size=22).move_to(child.get_center() + UP * 0.25)
        child_pid = Text("pid 101", font_size=18, color=YELLOW, font="Monospace").move_to(child.get_center() + DOWN * 0.25)
        child_group = VGroup(child, child_lbl, child_pid)

        self.play(FadeIn(child_group, shift=RIGHT))
        return child_group

    def show_return_values(self, parent, child):
        rc_parent = Text("rc = 101", font_size=22, font="Monospace", color=BLUE).next_to(parent, DOWN, buff=0.4)
        rc_child = Text("rc = 0", font_size=22, font="Monospace", color=GREEN).next_to(child, DOWN, buff=0.4)

        with self.voiceover(
            text="Now both processes run the very next instruction after fork. "
                 "The parent's fork returned the child's PID — one hundred and one. "
                 "The child's fork returned zero."
        ):
            self.play(Write(rc_parent), Write(rc_child))

        with self.voiceover(
            text="That single integer is how each process knows which one it is. "
                 "Code after fork branches on the return value: zero means I am the child, "
                 "non-zero means I am the parent and that number is my child."
        ):
            self.play(Indicate(rc_parent, color=BLUE_A, scale_factor=1.2))
            self.play(Indicate(rc_child, color=GREEN_A, scale_factor=1.2))

        self.play(FadeOut(self.fork_call))

    def show_cow(self, parent, child):
        page1 = Rectangle(width=2.0, height=0.8, color=YELLOW, fill_opacity=0.4).move_to(DOWN * 1.6)
        page1_lbl = Text("page X", font_size=18, font="Monospace").move_to(page1.get_center())
        page = VGroup(page1, page1_lbl)

        arrow_p = Arrow(parent.get_bottom(), page.get_top() + LEFT * 0.5, color=BLUE, buff=0.1)
        arrow_c = Arrow(child.get_bottom(), page.get_top() + RIGHT * 0.5, color=GREEN, buff=0.1)
        cow_lbl = Text("copy-on-write (read only)", font_size=18, color=GREY).next_to(page, DOWN, buff=0.3)

        with self.voiceover(
            text="Copying every page of memory would be slow, so the kernel cheats. "
                 "Both processes share the original physical pages — marked read-only. "
                 "This is called copy-on-write."
        ):
            self.play(FadeIn(page))
            self.play(GrowArrow(arrow_p), GrowArrow(arrow_c))
            self.play(Write(cow_lbl))

        # Now the child writes; kernel splits the page
        write_lbl = Text("child writes →", font_size=18, color=RED).next_to(arrow_c, RIGHT, buff=0.1)
        page2 = Rectangle(width=2.0, height=0.8, color=GREEN, fill_opacity=0.5).move_to(DOWN * 1.6 + RIGHT * 2.5)
        page2_lbl = Text("page X'", font_size=18, font="Monospace").move_to(page2.get_center())
        page_copy = VGroup(page2, page2_lbl)

        with self.voiceover(
            text="The moment one of them tries to write, the CPU traps. "
                 "The kernel duplicates that one page and lets the writer modify the copy. "
                 "Pages that are never written stay shared forever."
        ):
            self.play(Write(write_lbl))
            new_arrow_c = Arrow(child.get_bottom(), page_copy.get_top(), color=GREEN, buff=0.1)
            self.play(
                Transform(arrow_c, new_arrow_c),
                FadeIn(page_copy, shift=RIGHT),
            )

    def closing(self):
        msg = Text(
            "one syscall returns twice — to two different processes",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.7)

        with self.voiceover(
            text="Fork is the only system call that returns twice — once in each process. "
                 "Combined with exec, it is the foundation of every shell, every server, "
                 "every Unix process you have ever started."
        ):
            self.play(Write(msg))
            self.wait(2)
