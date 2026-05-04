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


class SyscallSummary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title = Text("Recap", font_size=44, weight=BOLD).to_edge(UP)
        bullets = VGroup(
            Text("1. user code calls into libc", font_size=28),
            Text("2. registers carry the syscall number and arguments", font_size=28),
            Text("3. syscall instruction switches ring 3 to ring 0", font_size=28),
            Text("4. kernel dispatches via the syscall table", font_size=28),
            Text("5. sysret returns control to user space", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)

        with self.voiceover(text="To recap the five steps of a system call."):
            self.play(Write(title))

        for bullet in bullets:
            with self.voiceover(text=bullet.text):
                self.play(FadeIn(bullet, shift=RIGHT))

        with self.voiceover(text="That is the full round trip, from user space to the kernel and back."):
            self.wait(2)
