from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class RaceConditionAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        counter, counter_lbl = self.draw_shared_counter()
        t1, t2 = self.draw_threads()
        self.show_source_code()
        self.show_machine_code()
        self.good_interleaving(counter, counter_lbl, t1, t2)
        self.reset_counter(counter, counter_lbl)
        self.bad_interleaving(counter, counter_lbl, t1, t2)
        self.closing()

    def show_title(self):
        title = Text("The Race Condition", font_size=44, weight=BOLD)
        subtitle = Text(
            "why two threads sharing one variable is dangerous",
            font_size=26,
            color=YELLOW,
        ).next_to(title, DOWN)

        with self.voiceover(
            text="When two threads update the same variable at the same time, "
                 "the result depends on exactly how their instructions are interleaved. "
                 "This is called a race condition."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def draw_shared_counter(self):
        box = RoundedRectangle(width=2.0, height=1.2, corner_radius=0.15, color=YELLOW, fill_opacity=0.3)
        box.move_to(UP * 2.5)
        value = Text("0", font_size=40, font="Monospace", color=YELLOW).move_to(box.get_center())
        label = Text("counter (shared)", font_size=20, color=YELLOW).next_to(box, UP, buff=0.2)

        with self.voiceover(
            text="Here is the shared counter. It lives in memory and starts at zero. "
                 "Both threads can read it and both threads can write it."
        ):
            self.play(FadeIn(box), Write(label))
            self.play(Write(value))

        self.counter_box = box
        return box, value

    def draw_threads(self):
        t1_box = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, color=BLUE_C, fill_opacity=0.5)
        t1_box.move_to(LEFT * 4 + UP * 0.3)
        t1_lbl = Text("Thread 1", font_size=22).move_to(t1_box.get_center())
        t1 = VGroup(t1_box, t1_lbl)

        t2_box = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, color=GREEN_C, fill_opacity=0.5)
        t2_box.move_to(RIGHT * 4 + UP * 0.3)
        t2_lbl = Text("Thread 2", font_size=22).move_to(t2_box.get_center())
        t2 = VGroup(t2_box, t2_lbl)

        with self.voiceover(
            text="And here are our two threads. Each one wants to add one to the counter."
        ):
            self.play(FadeIn(t1, shift=RIGHT), FadeIn(t2, shift=LEFT))

        return t1, t2

    def show_source_code(self):
        code = Text("counter = counter + 1;", font_size=24, font="Monospace", color=WHITE)
        code.move_to(DOWN * 1.0)
        bracket = SurroundingRectangle(code, color=GREY, buff=0.2)

        with self.voiceover(
            text="In C, this looks like one harmless line: counter equals counter plus one. "
                 "Both threads run exactly this line."
        ):
            self.play(Write(code))
            self.play(Create(bracket))

        self.play(FadeOut(code), FadeOut(bracket))

    def show_machine_code(self):
        title = Text("but the CPU sees three steps:", font_size=22, color=GREY).move_to(DOWN * 0.5)
        steps = VGroup(
            Text("1.  LOAD  counter  -> register", font_size=22, font="Monospace", color=BLUE_A),
            Text("2.  ADD   register, 1", font_size=22, font="Monospace", color=BLUE_A),
            Text("3.  STORE register  -> counter", font_size=22, font="Monospace", color=BLUE_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(title, DOWN, buff=0.3)

        with self.voiceover(
            text="But the CPU does not see one operation. It sees three. "
                 "Load the value into a register. Add one. Store the register back into memory."
        ):
            self.play(Write(title))
            for step in steps:
                self.play(Write(step), run_time=0.6)

        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(steps))

    def _make_reg(self, color, position, name):
        box = Rectangle(width=1.6, height=0.7, color=color, fill_opacity=0.2).move_to(position)
        lbl = Text(name, font_size=16, color=color).next_to(box, UP, buff=0.1)
        val = Text("?", font_size=24, font="Monospace", color=color).move_to(box.get_center())
        return VGroup(box, lbl), val

    def _set_counter(self, counter_lbl, new_text, color=YELLOW):
        new_val = Text(new_text, font_size=40, font="Monospace", color=color).move_to(counter_lbl.get_center())
        self.play(Transform(counter_lbl, new_val), run_time=0.4)

    def _set_reg(self, reg_val, new_text, color):
        new_val = Text(new_text, font_size=24, font="Monospace", color=color).move_to(reg_val.get_center())
        self.play(Transform(reg_val, new_val), run_time=0.4)

    def good_interleaving(self, counter, counter_lbl, t1, t2):
        heading = Text("Case 1: lucky interleaving", font_size=26, color=GREEN).move_to(DOWN * 0.3)

        with self.voiceover(
            text="Let us first see a lucky interleaving where things go right."
        ):
            self.play(Write(heading))

        reg1_group, reg1_val = self._make_reg(BLUE, LEFT * 4 + DOWN * 1.6, "T1 register")
        reg2_group, reg2_val = self._make_reg(GREEN, RIGHT * 4 + DOWN * 1.6, "T2 register")
        self.play(FadeIn(reg1_group), FadeIn(reg2_group))

        with self.voiceover(text="Thread 1 loads counter, which is zero, into its register."):
            arrow = Arrow(counter.get_left(), reg1_group[0].get_top(), color=BLUE, buff=0.1)
            self.play(GrowArrow(arrow))
            self._set_reg(reg1_val, "0", BLUE)
            self.play(FadeOut(arrow))

        with self.voiceover(text="Thread 1 adds one in its register."):
            self._set_reg(reg1_val, "1", BLUE)

        with self.voiceover(text="Thread 1 stores its register back into counter. Counter is now one."):
            arrow = Arrow(reg1_group[0].get_top(), counter.get_left(), color=BLUE, buff=0.1)
            self.play(GrowArrow(arrow))
            self._set_counter(counter_lbl, "1")
            self.play(FadeOut(arrow))

        with self.voiceover(text="Now thread 2 takes its turn. It loads counter, which is one."):
            arrow = Arrow(counter.get_right(), reg2_group[0].get_top(), color=GREEN, buff=0.1)
            self.play(GrowArrow(arrow))
            self._set_reg(reg2_val, "1", GREEN)
            self.play(FadeOut(arrow))

        with self.voiceover(text="It adds one, and stores back. Counter is now two — exactly what we expected."):
            self._set_reg(reg2_val, "2", GREEN)
            arrow = Arrow(reg2_group[0].get_top(), counter.get_right(), color=GREEN, buff=0.1)
            self.play(GrowArrow(arrow))
            self._set_counter(counter_lbl, "2", color=GREEN)
            self.play(FadeOut(arrow))

        check = Text("✓ correct: 0 + 1 + 1 = 2", font_size=22, color=GREEN).move_to(DOWN * 3.0)
        with self.voiceover(text="Two increments, final value two. Everyone is happy."):
            self.play(Write(check))

        self.wait(0.5)
        self.play(
            FadeOut(heading), FadeOut(reg1_group), FadeOut(reg2_group),
            FadeOut(reg1_val), FadeOut(reg2_val), FadeOut(check),
        )

    def reset_counter(self, counter, counter_lbl):
        self._set_counter(counter_lbl, "0")

    def bad_interleaving(self, counter, counter_lbl, t1, t2):
        heading = Text("Case 2: unlucky interleaving", font_size=26, color=RED).move_to(DOWN * 0.3)

        with self.voiceover(
            text="Now watch what happens when the scheduler interleaves the two threads "
                 "in a different order."
        ):
            self.play(Write(heading))

        reg1_group, reg1_val = self._make_reg(BLUE, LEFT * 4 + DOWN * 1.6, "T1 register")
        reg2_group, reg2_val = self._make_reg(GREEN, RIGHT * 4 + DOWN * 1.6, "T2 register")
        self.play(FadeIn(reg1_group), FadeIn(reg2_group))

        with self.voiceover(text="Thread 1 loads counter, which is zero, into its register."):
            arrow = Arrow(counter.get_left(), reg1_group[0].get_top(), color=BLUE, buff=0.1)
            self.play(GrowArrow(arrow))
            self._set_reg(reg1_val, "0", BLUE)
            self.play(FadeOut(arrow))

        preempt = Text("← preempted!", font_size=20, color=RED).next_to(t1, UP, buff=0.2)
        with self.voiceover(
            text="But before thread 1 can finish, the scheduler preempts it. "
                 "Thread 2 starts running instead."
        ):
            self.play(Write(preempt))
            self.play(Indicate(t2, color=GREEN_A, scale_factor=1.1))

        with self.voiceover(text="Thread 2 loads counter — which is still zero — into its own register."):
            arrow = Arrow(counter.get_right(), reg2_group[0].get_top(), color=GREEN, buff=0.1)
            self.play(GrowArrow(arrow))
            self._set_reg(reg2_val, "0", GREEN)
            self.play(FadeOut(arrow))

        with self.voiceover(text="Thread 2 adds one and stores back. Counter is now one."):
            self._set_reg(reg2_val, "1", GREEN)
            arrow = Arrow(reg2_group[0].get_top(), counter.get_right(), color=GREEN, buff=0.1)
            self.play(GrowArrow(arrow))
            self._set_counter(counter_lbl, "1")
            self.play(FadeOut(arrow))

        resume = Text("resumes →", font_size=20, color=BLUE).next_to(t1, UP, buff=0.2)
        with self.voiceover(
            text="Eventually thread 1 gets the CPU back. But it never re-read counter. "
                 "Its register still holds the stale value zero."
        ):
            self.play(FadeOut(preempt))
            self.play(Write(resume))

        with self.voiceover(text="Thread 1 adds one to its stale zero, and stores one back into counter."):
            self._set_reg(reg1_val, "1", BLUE)
            arrow = Arrow(reg1_group[0].get_top(), counter.get_left(), color=BLUE, buff=0.1)
            self.play(GrowArrow(arrow))
            self._set_counter(counter_lbl, "1", color=RED)
            self.play(FadeOut(arrow))

        cross = Text("✗ wrong: two increments, final value 1", font_size=22, color=RED).move_to(DOWN * 3.0)
        with self.voiceover(
            text="Two increments, but the counter only went up by one. "
                 "Thread 2's update was silently lost. This is the lost-update problem."
        ):
            self.play(Write(cross))

        self.wait(1)
        self.play(
            FadeOut(heading), FadeOut(reg1_group), FadeOut(reg2_group),
            FadeOut(reg1_val), FadeOut(reg2_val), FadeOut(cross), FadeOut(resume),
        )

    def closing(self):
        msg = Text(
            "the bug appears only on certain interleavings",
            font_size=26, color=YELLOW,
        ).move_to(DOWN * 1.0)
        msg2 = Text(
            "→ tests pass, production fails",
            font_size=24, color=RED,
        ).next_to(msg, DOWN, buff=0.3)

        with self.voiceover(
            text="The terrifying thing about a race condition is that it only shows up "
                 "for some interleavings. Your tests can pass a thousand times, "
                 "and then in production, the scheduler picks the bad order — "
                 "and your counter is wrong."
        ):
            self.play(Write(msg))
            self.play(Write(msg2))

        with self.voiceover(
            text="The fix is to make the read, modify, and write happen atomically — "
                 "with a mutex, or a hardware atomic instruction. "
                 "But that is a story for another video."
        ):
            self.wait(2)


class RaceConditionSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. one C statement = three machine instructions", font_size=26),
            Text("2. the scheduler can preempt between any two of them", font_size=26),
            Text("3. two threads can both read the old value", font_size=26),
            Text("4. one thread's write overwrites the other's", font_size=26),
            Text("5. fix: make read-modify-write atomic", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five points about race conditions."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(
            text="A race condition is not a bug in your code — it is a bug in your assumption "
                 "that one line of source code is one indivisible step. It is not."
        ):
            self.wait(2)
