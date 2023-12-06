import threading
import time
import customtkinter
import winsound
from CTkMessagebox import CTkMessagebox


class Pomodoro(customtkinter.CTkTabview):

    def __init__(self):

        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        self.window = customtkinter.CTk()
        self.window.geometry("720x480")
        self.window.title("Pomodoro")
        self.window.resizable(False, False)

        self.tabview = customtkinter.CTkTabview(self.window)
        self.tabview.pack()

        self.pomodoro_tab = self.tabview.add("Pomodoro")
        self.short_break_tab = self.tabview.add("Short Break")
        self.long_break_tab = self.tabview.add("Long Break")

        self.pomodoro_timer_label = customtkinter.CTkLabel(
            self.pomodoro_tab, text="25:00", font=("", 48))
        self.pomodoro_timer_label.pack()

        self.short_break_timer_label = customtkinter.CTkLabel(
            self.short_break_tab, text="05:00", font=("", 48))
        self.short_break_timer_label.pack()

        self.long_break_timer_label = customtkinter.CTkLabel(
            self.long_break_tab, text="30:00", font=("", 48))
        self.long_break_timer_label.pack()

        self.start_button = customtkinter.CTkButton(
            self.window, text="Start", command=self.start_timer_thread)
        self.start_button.pack()

        self.pause_button = customtkinter.CTkButton(
            self.window, text="Pause", command=self.pause_timer)
        self.pause_button.pack()

        self.skip_button = customtkinter.CTkButton(
            self.window, text="Skip", command=self.skip_timer)
        self.skip_button.pack()

        self.reset_button = customtkinter.CTkButton(
            self.window, text="Reset", command=self.reset_timer)
        self.reset_button.pack()

        self.pomodoro_label = customtkinter.CTkLabel(
            self.window, text="Pomodoro: 0")
        self.pomodoro_label.pack()

        self.window.mainloop()

    def start_timer(self):
        self.stopped = False
        self.skipped = False

        tab_selected = self.tabview.get()
        if tab_selected == "Pomodoro":
            full_seconds = 60 * 25
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}")
                self.window.update()
                time.sleep(1)
                full_seconds -= 1

            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_label.configure(
                    text=f"Pomodoros: {self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.tabview.set("Long Break")
                else:
                    self.tabview.set("Short Break")
                self.start_timer()

        elif tab_selected == "Short Break":
            full_seconds = 60 * 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.short_break_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}")
                self.window.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabview.set("Pomodoro")
                self.start_timer()

        elif tab_selected == "Long Break":
            full_seconds = 60 * 30
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.long_break_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}")
                self.window.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabview.set("Pomodoro")
                self.start_timer()

    def start_timer_thread(self):
        if not self.running:
            self.running = True
            t = threading.Thread(target=self.start_timer)
            t.start()

    def reset_timer(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoro_timer_label.configure(text="25:00")
        self.short_break_timer_label.configure(text="05:00")
        self.long_break_timer_label.configure(text="30:00")
        self.pomodoro_label.configure(text="Pomodoros: 0")
        self.running = False

    def pause_timer(self):
        pass

    def skip_timer(self):
        tab_selected = self.tabview.get()
        if tab_selected == "Pomodoro":
            self.pomodoro_timer_label.configure(text="25:00")
        elif tab_selected == "Short Break":
            self.short_break_timer_label.configure(text="05:00")
        elif tab_selected == "Long Break":
            self.long_break_timer_label.configure(text="30:00")

        self.skipped = True
        self.stopped = True

    def settings(self):
        pass


if __name__ == '__main__':
    Pomodoro()
