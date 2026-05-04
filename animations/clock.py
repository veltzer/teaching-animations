from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class ClockAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        self.show_timer_hardware()
        user_proc, kernel_box = self.draw_actors()
        self.give_time_slice(user_proc)
        self.tick_fires(user_proc)
        self.scheduler_decides(kernel_box)
        self.return_to_next_process()

        with self.voiceover(text="And that is how the operating system stays in charge of the CPU."):
            self.wait(2)

    def show_title(self):
        title = Text("How the OS Keeps Control", font_size=44, weight=BOLD)
        subtitle = Text("the timer interrupt and the time slice", font_size=26, color=YELLOW).next_to(title, DOWN)

        with self.voiceover(
            text="Once a user program is running on the CPU, how does the operating system "
                 "ever get control back? The answer is the timer interrupt."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def show_timer_hardware(self):
        chip = RoundedRectangle(width=2.6, height=1.4, corner_radius=0.15, color=GREEN_C, fill_opacity=0.4)
        chip.to_edge(LEFT, buff=1.2)
        chip_lbl = Text("programmable timer", font_size=18).move_to(chip.get_center() + UP * 0.25)
        freq_lbl = Text("1000 Hz", font_size=20, color=YELLOW, font="Monospace").move_to(chip.get_center() + DOWN * 0.25)
        self.timer_chip = VGroup(chip, chip_lbl, freq_lbl)

        ticks = VGroup()
        for i in range(8):
            t = Text("tick", font_size=16, color=GREEN).move_to(chip.get_right() + RIGHT * (0.7 + i * 0.9))
            ticks.add(t)

        with self.voiceover(
            text="Inside the computer there is a small piece of hardware called a programmable timer. "
                 "The kernel sets it up to fire many times per second — a thousand times in this example."
        ):
            self.play(FadeIn(self.timer_chip, shift=RIGHT))

        with self.voiceover(
            text="Each tick is a hardware signal that the CPU cannot ignore."
        ):
            for t in ticks:
                self.play(FadeIn(t, shift=LEFT), run_time=0.18)

        self.play(FadeOut(ticks))

    def draw_actors(self):
        user_band = Rectangle(width=13, height=2.4, color=BLUE, fill_opacity=0.12).shift(UP * 2.0)
        kernel_band = Rectangle(width=13, height=2.4, color=RED, fill_opacity=0.12).shift(DOWN * 2.0)
        user_lbl = Text("User Space", font_size=20, color=BLUE).move_to(user_band.get_corner(UL) + RIGHT * 1.3 + DOWN * 0.3)
        kernel_lbl = Text("Kernel Space", font_size=20, color=RED).move_to(kernel_band.get_corner(UL) + RIGHT * 1.5 + DOWN * 0.3)
        boundary = DashedLine(LEFT * 6.5, RIGHT * 6.5, color=GREY)

        proc_box = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.15, color=BLUE_C, fill_opacity=0.5)
        proc_box.move_to(RIGHT * 2.5 + UP * 2.0)
        proc_lbl = Text("process A", font_size=18).move_to(proc_box.get_center())
        proc = VGroup(proc_box, proc_lbl)

        kernel_box = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.15, color=RED_C, fill_opacity=0.5)
        kernel_box.move_to(RIGHT * 2.5 + DOWN * 2.0)
        kernel_lbl = Text("scheduler", font_size=18).move_to(kernel_box.get_center())
        kernel = VGroup(kernel_box, kernel_lbl)

        with self.voiceover(
            text="Up here in user space, an application wants to run. "
                 "Down in kernel space lives the scheduler — the part of the OS that decides "
                 "which process gets the CPU next."
        ):
            self.play(Create(user_band), Create(kernel_band))
            self.play(Write(user_lbl), Write(kernel_lbl), Create(boundary))
            self.play(FadeIn(proc, shift=DOWN), FadeIn(kernel, shift=UP))

        self.user_band = user_band
        self.kernel_band = kernel_band
        self.boundary = boundary
        return proc, kernel

    def give_time_slice(self, user_proc):
        slice_lbl = Text("time slice = 10 ms", font_size=20, color=YELLOW, font="Monospace")
        slice_lbl.move_to(LEFT * 2.5 + UP * 0.3)
        arrow_up = Arrow(start=RIGHT * 2.5 + DOWN * 1.4, end=RIGHT * 2.5 + UP * 1.4, color=YELLOW, buff=0.1)
        run_lbl = Text("running", font_size=18, color=BLUE).next_to(user_proc, RIGHT, buff=0.3)

        with self.voiceover(
            text="The scheduler picks process A, programs the timer for a short interval — "
                 "say ten milliseconds — and hands the CPU to the user program."
        ):
            self.play(Write(slice_lbl))
            self.play(GrowArrow(arrow_up))
            self.play(Write(run_lbl))

        with self.voiceover(
            text="Process A is now running freely. The kernel is asleep. "
                 "But the timer is silently counting down."
        ):
            self.play(Indicate(user_proc, color=BLUE_A, scale_factor=1.1))
            self.play(Indicate(self.timer_chip, color=GREEN, scale_factor=1.05))

        self.slice_lbl = slice_lbl
        self.arrow_up = arrow_up
        self.run_lbl = run_lbl

    def tick_fires(self, user_proc):
        irq_arrow = Arrow(
            start=self.timer_chip.get_right(),
            end=user_proc.get_left() + LEFT * 0.1,
            color=RED,
            buff=0.1,
        )
        irq_lbl = Text("IRQ 0", font_size=18, color=RED).next_to(irq_arrow, UP, buff=0.1)

        with self.voiceover(
            text="Ten milliseconds later, the timer fires. It raises an interrupt request — "
                 "IRQ zero on x86 — directly to the CPU."
        ):
            self.play(GrowArrow(irq_arrow), Write(irq_lbl))
            self.play(Flash(user_proc.get_center(), color=RED, flash_radius=1.5))

        trap = CurvedArrow(
            start_point=RIGHT * 2.5 + UP * 1.5,
            end_point=RIGHT * 2.5 + DOWN * 1.5,
            color=YELLOW,
            angle=-PI / 3,
        )
        trap_lbl = Text("forced trap\ninto kernel", font_size=16, color=YELLOW).move_to(RIGHT * 5 + UP * 0.0)

        with self.voiceover(
            text="The CPU stops whatever process A was doing — mid-instruction if it has to — "
                 "saves its registers, switches from ring three to ring zero, "
                 "and jumps into the kernel's interrupt handler."
        ):
            self.play(Create(trap), Write(trap_lbl))
            self.play(FadeOut(self.run_lbl))

        self.irq_group = VGroup(irq_arrow, irq_lbl)
        self.trap_group = VGroup(trap, trap_lbl)

    def scheduler_decides(self, kernel_box):
        ready_q = Text("ready queue: [A, B, C]", font_size=18, color=RED_A, font="Monospace")
        ready_q.move_to(LEFT * 3 + DOWN * 0.5)
        decision = Text("pick next: B", font_size=20, color=YELLOW, weight=BOLD)
        decision.move_to(LEFT * 3 + DOWN * 1.2)

        with self.voiceover(
            text="Now the scheduler runs. It looks at its ready queue — "
                 "the list of processes waiting for the CPU — "
                 "and decides who should run next."
        ):
            self.play(Write(ready_q))
            self.play(Indicate(kernel_box, color=RED_A, scale_factor=1.1))

        with self.voiceover(
            text="It might pick a different process — say, process B — to enforce fairness, "
                 "or it might give another slice to process A. Either way, the choice is the kernel's."
        ):
            self.play(Write(decision))

        self.scheduler_extras = VGroup(ready_q, decision)

    def return_to_next_process(self):
        proc_b = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.15, color=BLUE_C, fill_opacity=0.5)
        proc_b.move_to(RIGHT * 2.5 + UP * 2.0)
        proc_b_lbl = Text("process B", font_size=18).move_to(proc_b.get_center())
        proc_b_group = VGroup(proc_b, proc_b_lbl)

        ret_arrow = CurvedArrow(
            start_point=RIGHT * 2.5 + DOWN * 1.5,
            end_point=RIGHT * 2.5 + UP * 1.5,
            color=GREEN,
            angle=-PI / 3,
        )
        ret_lbl = Text("iret\n(restore B's regs)", font_size=16, color=GREEN).move_to(RIGHT * 5 + UP * 0.0)

        with self.voiceover(
            text="The kernel reprograms the timer for another slice, "
                 "loads process B's saved registers, "
                 "and issues iret — switching back to ring three."
        ):
            self.play(FadeOut(self.trap_group))
            self.play(Create(ret_arrow), Write(ret_lbl))
            self.play(FadeIn(proc_b_group, shift=DOWN))

        with self.voiceover(
            text="Process B has no idea any of this happened. "
                 "From its point of view, it just got a turn on the CPU. "
                 "And in another ten milliseconds, the timer will fire again."
        ):
            self.play(Indicate(proc_b_group, color=BLUE_A, scale_factor=1.1))
