from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from datetime import datetime

class ChallengeTracker(BoxLayout):
    current_day = StringProperty("")
    status = ListProperty([False, False, False])
    xp = NumericProperty(0)
    level = NumericProperty(1)
    progress_percent = NumericProperty(0)
    log = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_day()
        Clock.schedule_interval(self.check_new_day, 10)

    def update_day(self):
        self.current_day = datetime.now().strftime("%A, %B %d")
        self.status = [False, False, False]

    def mark_done(self, index):
        if not self.status[index]:
            self.status[index] = True
            self.xp += 10
            self.update_progress()
            self.check_level_up()

    def update_progress(self):
        self.progress_percent = (self.xp % 100)

    def check_level_up(self):
        if self.xp >= self.level * 100:
            self.level += 1
            self.xp = 0
            self.log.append(f"Leveled up to Level {self.level} on {self.current_day}!")

    def reset_day(self):
        self.status = [False, False, False]

    def check_new_day(self, dt):
        now = datetime.now().strftime("%A, %B %d")
        if self.current_day != now:
            self.log.append(f"{self.current_day} - Completed: {self.status}")
            self.update_day()

    def get_weekly_summary(self):
        return "\n".join(self.log[-7:])

class SoloLevelingApp(App):
    def build(self):
        return ChallengeTracker()

if __name__ == '__main__':
    SoloLevelingApp().run()
