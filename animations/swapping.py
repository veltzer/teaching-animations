from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class SwappingAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        ram, disk, ram_label, disk_label = self.draw_storage()
        ram_frames, disk_frames = self.draw_frames(ram, disk)
        page_table, pt_rows = self.draw_page_table()
        self.populate_pages(ram_frames, disk_frames, pt_rows)
        self.page_fault(ram_frames, disk_frames, pt_rows)
        self.swap_out_in(ram_frames, disk_frames, pt_rows)
        self.closing()

    def show_title(self):
        title = Text("How Operating Systems Swap Pages", font_size=42, weight=BOLD)
        subtitle = Text(
            "demand paging and the swap area",
            font_size=26,
            color=YELLOW,
        ).next_to(title, DOWN)

        with self.voiceover(
            text="In this video, we will look at how operating systems use swapping "
                 "to give programs the illusion of having more memory than the machine "
                 "actually has."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def draw_storage(self):
        ram_box = Rectangle(width=6, height=3, color=GREEN, fill_opacity=0.12)
        ram_box.shift(LEFT * 3.5 + UP * 0.5)
        ram_lbl = Text("RAM (fast, small)", font_size=22, color=GREEN)
        ram_lbl.next_to(ram_box, UP, buff=0.2)

        disk_box = Rectangle(width=6, height=3, color=ORANGE, fill_opacity=0.12)
        disk_box.shift(RIGHT * 3.5 + UP * 0.5)
        disk_lbl = Text("Disk swap area (slow, large)", font_size=22, color=ORANGE)
        disk_lbl.next_to(disk_box, UP, buff=0.2)

        with self.voiceover(
            text="Every computer has two main places to keep data. "
                 "On the left, RAM. It is fast, but expensive and limited in size."
        ):
            self.play(Create(ram_box), Write(ram_lbl))

        with self.voiceover(
            text="On the right, the disk. It is much slower, "
                 "but it is also much larger and much cheaper. "
                 "The operating system reserves a special region on disk called the swap area."
        ):
            self.play(Create(disk_box), Write(disk_lbl))

        return ram_box, disk_box, ram_lbl, disk_lbl

    def draw_frames(self, ram, disk):
        ram_frames = []
        for i in range(4):
            frame = Rectangle(width=1.1, height=1.1, color=GREEN_C, fill_opacity=0.25)
            frame.move_to(ram.get_center() + LEFT * 1.95 + RIGHT * 1.3 * i)
            ram_frames.append(frame)

        disk_frames = []
        for i in range(8):
            row = i // 4
            col = i % 4
            frame = Rectangle(width=1.1, height=0.55, color=ORANGE, fill_opacity=0.2)
            frame.move_to(
                disk.get_center() + LEFT * 1.95 + RIGHT * 1.3 * col + UP * 0.5 + DOWN * 0.7 * row
            )
            disk_frames.append(frame)

        with self.voiceover(
            text="RAM is divided into fixed size physical frames. "
                 "Here we show four of them. The disk swap area is divided into "
                 "the same size slots, but there are many more of them."
        ):
            self.play(*[Create(f) for f in ram_frames])
            self.play(*[Create(f) for f in disk_frames], run_time=1.2)

        return ram_frames, disk_frames

    def draw_page_table(self):
        pt_box = Rectangle(width=4.5, height=2.8, color=BLUE, fill_opacity=0.1)
        pt_box.move_to(DOWN * 2.7)
        pt_lbl = Text("Page Table (per process)", font_size=20, color=BLUE)
        pt_lbl.next_to(pt_box, UP, buff=0.1)

        header = Text("page    location", font_size=16, font="Monospace", color=BLUE_A)
        header.move_to(pt_box.get_top() + DOWN * 0.3)

        rows_data = [
            ("P0", "RAM frame 0"),
            ("P1", "RAM frame 1"),
            ("P2", "RAM frame 2"),
            ("P3", "RAM frame 3"),
        ]
        rows = []
        for i, (page, loc) in enumerate(rows_data):
            row = Text(f"{page}      {loc}", font_size=15, font="Monospace", color=WHITE)
            row.move_to(pt_box.get_top() + DOWN * (0.7 + 0.45 * i))
            rows.append(row)

        with self.voiceover(
            text="For every process, the operating system keeps a page table. "
                 "Each entry maps a virtual page of the process to its current location, "
                 "either a physical frame in RAM, or a slot in the swap area."
        ):
            self.play(Create(pt_box), Write(pt_lbl))
            self.play(Write(header))
            for row in rows:
                self.play(Write(row), run_time=0.3)

        self.pt_box = pt_box
        self.pt_header = header
        return pt_box, rows

    def populate_pages(self, ram_frames, disk_frames, pt_rows):
        ram_pages = []
        labels = ["P0", "P1", "P2", "P3"]
        colors = [BLUE_C, PURPLE_C, TEAL_C, MAROON_C]
        for i, (lbl, color) in enumerate(zip(labels, colors)):
            page = VGroup(
                Rectangle(width=1.0, height=1.0, color=color, fill_opacity=0.7),
                Text(lbl, font_size=20, weight=BOLD),
            )
            page.move_to(ram_frames[i].get_center())
            ram_pages.append(page)

        with self.voiceover(
            text="Suppose our process has four pages, P zero through P three, "
                 "and they all happen to fit in RAM. Every memory access is fast, "
                 "and the page table simply records the frame number for each page."
        ):
            for page in ram_pages:
                self.play(FadeIn(page, scale=0.7), run_time=0.4)

        self.ram_pages = ram_pages
        self.disk_pages = {}

    def page_fault(self, ram_frames, disk_frames, pt_rows):
        cpu_box = RoundedRectangle(
            width=1.8, height=0.9, corner_radius=0.15, color=YELLOW, fill_opacity=0.3
        )
        cpu_box.move_to(UP * 3.3 + LEFT * 5.5)
        cpu_lbl = Text("CPU", font_size=20, weight=BOLD).move_to(cpu_box.get_center())
        cpu = VGroup(cpu_box, cpu_lbl)

        request = Text("access P4", font_size=20, color=YELLOW)
        request.next_to(cpu, RIGHT, buff=0.4)

        with self.voiceover(
            text="Now the program tries to access a fifth page, P four. "
                 "The CPU asks the memory unit to translate this virtual address."
        ):
            self.play(FadeIn(cpu), Write(request))

        new_row = Text("P4      (not present)", font_size=15, font="Monospace", color=RED)
        new_row.move_to(self.pt_box.get_top() + DOWN * (0.7 + 0.45 * 4))

        fault_flash = Text("PAGE FAULT!", font_size=36, color=RED, weight=BOLD)
        fault_flash.move_to(UP * 0.5)

        with self.voiceover(
            text="But P four has no entry pointing to RAM. "
                 "The hardware raises a page fault, and control jumps into the kernel."
        ):
            self.play(Write(new_row))
            self.play(FadeIn(fault_flash, scale=1.5))
            self.play(Flash(fault_flash.get_center(), color=RED, flash_radius=1.8))
            self.play(FadeOut(fault_flash))

        self.cpu_group = VGroup(cpu, request)
        self.fault_row = new_row

    def swap_out_in(self, ram_frames, disk_frames, pt_rows):
        with self.voiceover(
            text="The kernel needs to bring P four into RAM, but RAM is full. "
                 "It must first choose a victim page to evict. "
                 "Many algorithms exist for this, such as Least Recently Used. "
                 "Let's say the kernel picks P one."
        ):
            self.play(Indicate(self.ram_pages[1], color=RED, scale_factor=1.3))

        victim = self.ram_pages[1]
        target_disk = disk_frames[0]

        small_victim = victim.copy()
        small_victim.generate_target()
        small_victim.target.scale(0.5).move_to(target_disk.get_center())

        with self.voiceover(
            text="Step one. The kernel writes P one out to a free slot in the swap area on disk. "
                 "This is called swapping out, or paging out."
        ):
            self.play(MoveToTarget(small_victim), FadeOut(victim), run_time=2)

        old_p1_row = pt_rows[1]
        new_p1_row = Text("P1      swap slot 0", font_size=15, font="Monospace", color=ORANGE)
        new_p1_row.move_to(old_p1_row.get_center())

        with self.voiceover(
            text="The page table is updated. P one is now marked as living on disk, "
                 "in swap slot zero, not in RAM."
        ):
            self.play(Transform(old_p1_row, new_p1_row))

        new_page = VGroup(
            Rectangle(width=1.0, height=1.0, color=GOLD, fill_opacity=0.7),
            Text("P4", font_size=20, weight=BOLD),
        )
        new_page.scale(0.5).move_to(disk_frames[4].get_center())

        with self.voiceover(
            text="Step two. The kernel reads P four from wherever it lives on disk. "
                 "In a real system this might be the executable file, or another swap slot."
        ):
            self.play(FadeIn(new_page))

        new_page.generate_target()
        new_page.target.scale(2.0).move_to(ram_frames[1].get_center())

        with self.voiceover(
            text="It then loads P four into the now free RAM frame, "
                 "the same one that used to hold P one."
        ):
            self.play(MoveToTarget(new_page), run_time=2)

        new_p4_row = Text("P4      RAM frame 1", font_size=15, font="Monospace", color=GREEN)
        new_p4_row.move_to(self.fault_row.get_center())

        with self.voiceover(
            text="The page table is updated again. P four now points at RAM frame one."
        ):
            self.play(Transform(self.fault_row, new_p4_row))

        with self.voiceover(
            text="Finally, the kernel returns from the page fault handler, "
                 "and the original instruction is re-executed. "
                 "From the program's point of view, the access just worked."
        ):
            self.play(Indicate(self.cpu_group, color=GREEN, scale_factor=1.2))
            self.play(Flash(ram_frames[1].get_center(), color=GREEN, flash_radius=1.5))

        self.ram_pages[1] = new_page

    def closing(self):
        with self.voiceover(
            text="And that is swapping. The operating system silently moves pages "
                 "between RAM and disk, so that programs can use more memory than "
                 "the hardware physically holds. The price is performance: "
                 "a disk access is thousands of times slower than RAM, "
                 "which is why a system that swaps too much, called thrashing, "
                 "feels painfully slow."
        ):
            self.wait(2)


class SwappingSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. memory is split into fixed-size pages and frames", font_size=26),
            Text("2. the page table maps each page to RAM or to swap", font_size=26),
            Text("3. accessing an absent page raises a page fault", font_size=26),
            Text("4. the kernel evicts a victim page out to disk", font_size=26),
            Text("5. the needed page is read in and the access retries", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five steps of swapping."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="That is how the operating system gives every program "
                 "the illusion of nearly unlimited memory."
        ):
            self.wait(2)
