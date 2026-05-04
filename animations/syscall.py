from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
# To swap TTS backends later, replace the import + set_speech_service line:
#   from manim_voiceover.services.openai import OpenAIService
#   self.set_speech_service(OpenAIService(voice="nova"))
#   from manim_voiceover.services.elevenlabs import ElevenLabsService
#   self.set_speech_service(ElevenLabsService(voice_name="Rachel"))
#   from manim_voiceover.services.recorder import RecorderService
#   self.set_speech_service(RecorderService())   # records your own voice


class SyscallAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        boundary = self.draw_spaces()
        user_proc, kernel_box = self.draw_actors()
        self.make_call(user_proc, boundary)
        self.dispatch_in_kernel()
        self.return_to_user(user_proc, boundary)

        with self.voiceover(text="And that, in essence, is how a system call works."):
            self.wait(2)

    def show_title(self):
        title = Text("How a System Call Works", font_size=44, weight=BOLD)
        subtitle = Text("read(fd, buf, count)", font_size=28, color=YELLOW).next_to(title, DOWN)

        with self.voiceover(
            text="In this video, we will look at how a system call works. "
                 "We will use the read system call as our running example."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def draw_spaces(self):
        user_band = Rectangle(width=13, height=3, color=BLUE, fill_opacity=0.15).shift(UP * 1.8)
        kernel_band = Rectangle(width=13, height=3, color=RED, fill_opacity=0.15).shift(DOWN * 1.8)
        user_lbl = Text("User Space (ring 3)", font_size=22, color=BLUE).move_to(user_band.get_corner(UL) + RIGHT * 1.7 + DOWN * 0.3)
        kernel_lbl = Text("Kernel Space (ring 0)", font_size=22, color=RED).move_to(kernel_band.get_corner(UL) + RIGHT * 1.9 + DOWN * 0.3)
        boundary = DashedLine(LEFT * 6.5, RIGHT * 6.5, color=GREY)
        boundary_lbl = Text("privilege boundary", font_size=16, color=GREY).next_to(boundary, RIGHT, buff=0.1)

        with self.voiceover(
            text="Modern processors split memory into two privilege levels. "
                 "On top, user space, where ordinary programs run with limited rights. "
                 "Below, kernel space, where the operating system has full control of the hardware."
        ):
            self.play(Create(user_band), Create(kernel_band))
            self.play(Write(user_lbl), Write(kernel_lbl))

        with self.voiceover(
            text="Between them lies a privilege boundary that user programs cannot simply step over."
        ):
            self.play(Create(boundary), Write(boundary_lbl))

        return boundary

    def draw_actors(self):
        proc_box = RoundedRectangle(width=2.6, height=1.2, corner_radius=0.15, color=BLUE_C, fill_opacity=0.5)
        proc_box.move_to(LEFT * 4 + UP * 1.8)
        proc_lbl = Text("user process", font_size=18).move_to(proc_box.get_center() + UP * 0.2)
        proc_code = Text("read(fd, buf, n)", font_size=16, color=YELLOW).move_to(proc_box.get_center() + DOWN * 0.25)
        proc = VGroup(proc_box, proc_lbl, proc_code)

        kernel_box = RoundedRectangle(width=2.6, height=1.2, corner_radius=0.15, color=RED_C, fill_opacity=0.5)
        kernel_box.move_to(LEFT * 4 + DOWN * 1.8)
        kernel_lbl = Text("syscall handler", font_size=18).move_to(kernel_box.get_center() + UP * 0.2)
        kernel_entry = Text("entry_SYSCALL_64", font_size=14, color=YELLOW).move_to(kernel_box.get_center() + DOWN * 0.25)
        kernel = VGroup(kernel_box, kernel_lbl, kernel_entry)

        with self.voiceover(
            text="Here is our user process. It wants to read some bytes from a file, "
                 "so it calls the read function from the C library."
        ):
            self.play(FadeIn(proc, shift=DOWN))

        with self.voiceover(
            text="Down in the kernel, a piece of code called the system call entry point is waiting. "
                 "On Linux x86-64, this is named entry_SYSCALL_64."
        ):
            self.play(FadeIn(kernel, shift=UP))

        return proc, kernel

    def make_call(self, user_proc, boundary):
        regs_title = Text("1. load registers", font_size=20, color=YELLOW).move_to(RIGHT * 2.5 + UP * 2.6)
        rax = Text("rax = 0   (sys_read)", font_size=18, font="Monospace").move_to(RIGHT * 2.5 + UP * 2.1)
        rdi = Text("rdi = fd", font_size=18, font="Monospace").move_to(RIGHT * 2.5 + UP * 1.65)
        rsi = Text("rsi = buf", font_size=18, font="Monospace").move_to(RIGHT * 2.5 + UP * 1.2)
        rdx = Text("rdx = n", font_size=18, font="Monospace").move_to(RIGHT * 2.5 + UP * 0.75)

        with self.voiceover(
            text="Before crossing into the kernel, the C library places the arguments into specific CPU registers. "
                 "Register rax holds the system call number — zero, for read. "
                 "rdi holds the file descriptor, rsi the buffer address, and rdx the number of bytes to read."
        ):
            self.play(Write(regs_title))
            for r in (rax, rdi, rsi, rdx):
                self.play(Write(r), run_time=0.5)

        instr = Text("syscall", font_size=28, color=YELLOW, weight=BOLD).move_to(LEFT * 4 + UP * 0.6)
        trap_arrow = CurvedArrow(
            start_point=LEFT * 4 + UP * 1.1,
            end_point=LEFT * 4 + DOWN * 1.2,
            color=YELLOW,
            angle=-PI / 3,
        )
        trap_lbl = Text("trap into kernel\n(mode switch ring 3 → 0)", font_size=16, color=YELLOW).move_to(LEFT * 1.5 + UP * 0.0)

        with self.voiceover(
            text="Then it issues a single CPU instruction: syscall. "
                 "This instruction is special. It atomically switches the processor from ring three "
                 "to ring zero and jumps to a fixed address inside the kernel."
        ):
            self.play(FadeIn(instr, scale=1.5))
            self.play(Create(trap_arrow), Write(trap_lbl))
            self.play(Flash(LEFT * 4 + DOWN * 1.8, color=RED, flash_radius=1.5))

        self.regs_group = VGroup(regs_title, rax, rdi, rsi, rdx)
        self.trap_group = VGroup(instr, trap_arrow, trap_lbl)

    def dispatch_in_kernel(self):
        header = Text("syscall table", font_size=18, color=RED).move_to(RIGHT * 2.5 + DOWN * 0.9)
        rows_data = [
            ("0", "sys_read", YELLOW),
            ("1", "sys_write", WHITE),
            ("2", "sys_open", WHITE),
            ("3", "sys_close", WHITE),
        ]
        rows = []
        for i, (num, name, color) in enumerate(rows_data):
            row = Text(f"{num}: {name}", font_size=16, font="Monospace", color=color)
            row.move_to(RIGHT * 2.5 + DOWN * (1.4 + 0.4 * i))
            rows.append(row)

        with self.voiceover(
            text="Now safely inside the kernel, the entry point looks up the system call table. "
                 "Each row maps a number to a kernel function. "
                 "Our number, zero, points to sys_read."
        ):
            self.play(Write(header))
            for row in rows:
                self.play(Write(row), run_time=0.3)

        dispatch_arrow = Arrow(
            start=LEFT * 2.7 + DOWN * 1.8,
            end=RIGHT * 1.4 + DOWN * 1.3,
            color=YELLOW,
            buff=0.1,
        )
        dispatch_lbl = Text("dispatch by rax", font_size=14, color=YELLOW).next_to(dispatch_arrow, UP, buff=0.05)
        work = Text("→ VFS → driver → device", font_size=18, color=RED_A).move_to(DOWN * 2.9)

        with self.voiceover(
            text="The kernel dispatches based on rax, calls sys_read, "
                 "which then walks through the virtual file system layer, "
                 "down to the device driver, and finally talks to the actual hardware."
        ):
            self.play(Create(dispatch_arrow), Write(dispatch_lbl))
            self.play(Write(work))

        self.kernel_extras = VGroup(header, *rows, dispatch_arrow, dispatch_lbl, work)

    def return_to_user(self, user_proc, boundary):
        ret_arrow = CurvedArrow(
            start_point=LEFT * 4 + DOWN * 1.2,
            end_point=LEFT * 4 + UP * 1.1,
            color=GREEN,
            angle=-PI / 3,
        )
        ret_lbl = Text("sysret\n(mode switch ring 0 → 3)", font_size=16, color=GREEN).move_to(LEFT * 6.0 + UP * 0.0)
        ret_val = Text("rax = bytes read", font_size=18, font="Monospace", color=GREEN).move_to(RIGHT * 2.5 + UP * 2.1)

        with self.voiceover(
            text="Once the work is done, the kernel places the return value, "
                 "the number of bytes actually read, into rax. "
                 "It then issues sysret, which switches the CPU back to ring three "
                 "and resumes the user process exactly where it left off."
        ):
            self.play(Create(ret_arrow), Write(ret_lbl))
            self.play(Transform(self.regs_group[1], ret_val))
            self.play(Flash(LEFT * 4 + UP * 1.8, color=BLUE, flash_radius=1.5))

        done = Text("user process resumes", font_size=22, color=BLUE).move_to(UP * 3.4)
        with self.voiceover(
            text="From the program's point of view, read simply returned a number. "
                 "But under the hood, the CPU crossed a privilege boundary, "
                 "ran code in a completely different context, and crossed back."
        ):
            self.play(Write(done))
