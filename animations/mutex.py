from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class MutexAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.show_title()
        lock, lock_state, t1, t2, t3 = self.draw_actors()
        self.first_acquire(lock, lock_state, t1)
        self.second_tries(lock, t2, t3)
        self.first_releases(lock, lock_state, t1, t2)
        self.closing()

    def show_title(self):
        title = Text("Mutex", font_size=52, weight=BOLD)
        subtitle = Text(
            "the lock that fixes the race",
            font_size=26,
            color=YELLOW,
        ).next_to(title, DOWN)

        with self.voiceover(
            text="A mutex — short for mutual exclusion — is the simplest tool for keeping "
                 "threads from stepping on each other. Only one thread holds the lock at a time. "
                 "Everyone else waits."
        ):
            self.play(Write(title))
            self.play(FadeIn(subtitle, shift=UP))

        self.play(FadeOut(title), FadeOut(subtitle))

    def draw_actors(self):
        # Lock in the center
        lock_box = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.15, color=YELLOW, fill_opacity=0.3)
        lock_box.move_to(ORIGIN)
        lock_lbl = Text("mutex", font_size=20).move_to(lock_box.get_center() + UP * 0.2)
        lock_state = Text("UNLOCKED", font_size=18, color=GREEN, font="Monospace").move_to(lock_box.get_center() + DOWN * 0.2)
        lock = VGroup(lock_box, lock_lbl)

        # Three threads
        positions = [LEFT * 4.5 + UP * 1.5, LEFT * 4.5, LEFT * 4.5 + DOWN * 1.5]
        colors = [BLUE_C, GREEN_C, PURPLE_C]
        threads = []
        for i, (pos, color) in enumerate(zip(positions, colors)):
            box = RoundedRectangle(width=2.0, height=0.9, corner_radius=0.15, color=color, fill_opacity=0.5)
            box.move_to(pos)
            lbl = Text(f"thread {i+1}", font_size=18).move_to(box.get_center())
            threads.append(VGroup(box, lbl))

        with self.voiceover(
            text="Here is the mutex, currently unlocked. On the left, three threads — "
                 "all of them want access to a shared resource that the mutex protects."
        ):
            self.play(FadeIn(lock), Write(lock_state))
            for t in threads:
                self.play(FadeIn(t, shift=RIGHT), run_time=0.3)

        return lock, lock_state, *threads

    def first_acquire(self, lock, lock_state, t1):
        op = Text("lock()", font_size=22, font="Monospace", color=BLUE).move_to(LEFT * 1.2 + UP * 1.5)
        arrow = Arrow(t1.get_right(), lock.get_left(), color=BLUE, buff=0.1)

        with self.voiceover(
            text="Thread one calls lock. Internally this is an atomic test-and-set: "
                 "the CPU swaps in a locked value and tells the thread what was there before. "
                 "It was unlocked, so thread one wins."
        ):
            self.play(GrowArrow(arrow), Write(op))

        new_state = Text("LOCKED by T1", font_size=18, color=RED, font="Monospace").move_to(lock_state.get_center())
        with self.voiceover(text="The mutex is now locked, owned by thread one."):
            self.play(Transform(lock_state, new_state))
            self.play(t1.animate.set_color(BLUE_A))

        self.play(FadeOut(arrow), FadeOut(op))
        self.first_lock_op = None

    def second_tries(self, lock, t2, t3):
        op2 = Text("lock()", font_size=22, font="Monospace", color=GREEN).move_to(LEFT * 1.2)
        arrow2 = Arrow(t2.get_right(), lock.get_left(), color=GREEN, buff=0.1)

        with self.voiceover(
            text="Thread two now calls lock. Test-and-set finds the mutex already locked. "
                 "Thread two does not get it."
        ):
            self.play(GrowArrow(arrow2), Write(op2))

        # Show queue forming
        queue_lbl = Text("waiters: [T2]", font_size=18, color=GREY, font="Monospace").to_edge(DOWN, buff=0.8)
        with self.voiceover(
            text="Instead of busy-spinning, the kernel parks thread two in a wait queue and "
                 "puts it to sleep."
        ):
            self.play(t2.animate.set_opacity(0.4))
            self.play(Write(queue_lbl))

        # Thread three also tries
        op3 = Text("lock()", font_size=22, font="Monospace", color=PURPLE).move_to(LEFT * 1.2 + DOWN * 1.5)
        arrow3 = Arrow(t3.get_right(), lock.get_left(), color=PURPLE, buff=0.1)
        new_queue = Text("waiters: [T2, T3]", font_size=18, color=GREY, font="Monospace").move_to(queue_lbl.get_center())

        with self.voiceover(
            text="Thread three calls lock too. Same outcome — it joins the queue behind thread two."
        ):
            self.play(GrowArrow(arrow3), Write(op3))
            self.play(t3.animate.set_opacity(0.4))
            self.play(Transform(queue_lbl, new_queue))

        self.play(FadeOut(arrow2), FadeOut(op2), FadeOut(arrow3), FadeOut(op3))
        self.queue_lbl = queue_lbl

    def first_releases(self, lock, lock_state, t1, t2):
        op = Text("unlock()", font_size=22, font="Monospace", color=BLUE).move_to(LEFT * 1.2 + UP * 1.5)
        arrow = Arrow(t1.get_right(), lock.get_left(), color=BLUE, buff=0.1)

        with self.voiceover(
            text="Thread one finishes its critical section and calls unlock."
        ):
            self.play(GrowArrow(arrow), Write(op))

        # Hand-off to T2
        new_state = Text("LOCKED by T2", font_size=18, color=RED, font="Monospace").move_to(lock_state.get_center())
        new_queue = Text("waiters: [T3]", font_size=18, color=GREY, font="Monospace").move_to(self.queue_lbl.get_center())

        with self.voiceover(
            text="The kernel does not just mark the mutex unlocked. "
                 "It hands the lock directly to the next waiter — thread two — and wakes it up. "
                 "Thread two never has to retry."
        ):
            self.play(FadeOut(arrow), FadeOut(op))
            self.play(t1.animate.set_color(BLUE_C))
            self.play(t2.animate.set_opacity(1.0).set_color(GREEN_A))
            self.play(Transform(lock_state, new_state))
            self.play(Transform(self.queue_lbl, new_queue))

    def closing(self):
        msg = Text(
            "atomic test-and-set + a wait queue = mutual exclusion",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.4)

        with self.voiceover(
            text="That is the whole mutex. An atomic instruction that the hardware guarantees "
                 "happens indivisibly, plus a kernel-managed queue of sleepers waiting for "
                 "their turn."
        ):
            self.play(Write(msg))
            self.wait(2)
