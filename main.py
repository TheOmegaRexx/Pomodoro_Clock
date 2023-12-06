import threading
import time
import customtkinter
import winsound
from CTkMessagebox import CTkMessagebox


class Pomodoro(customtkinter.CTkTabview):

    def __init__(self):

        # Initialize variables to keep track of pomodoros and timer state
        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        # Create the main window
        self.window = customtkinter.CTk()
        self.window.geometry("720x480")
        self.window.title("Pomodoro")
        self.window.resizable(False, False)

        # Create tabs for Pomodoro, Short Break, and Long Break
        self.tabview = customtkinter.CTkTabview(self.window)
        self.tabview.pack()

        self.pomodoro_tab = self.tabview.add("Pomodoro")
        self.short_break_tab = self.tabview.add("Short Break")
        self.long_break_tab = self.tabview.add("Long Break")

        # Create labels for displaying timer countdowns
        self.pomodoro_timer_label = customtkinter.CTkLabel(
            self.pomodoro_tab, text="25:00", font=("", 48))
        self.pomodoro_timer_label.pack()

        self.short_break_timer_label = customtkinter.CTkLabel(
            self.short_break_tab, text="05:00", font=("", 48))
        self.short_break_timer_label.pack()

        self.long_break_timer_label = customtkinter.CTkLabel(
            self.long_break_tab, text="30:00", font=("", 48))
        self.long_break_timer_label.pack()

        # Create buttons for control (Start, Pause, Skip, Reset)
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

        # Display the number of completed Pomodoros
        self.pomodoro_label = customtkinter.CTkLabel(
            self.window, text="Pomodoros: 0")
        self.pomodoro_label.pack()

        # Start the main event loop
        self.window.mainloop()

    def start_timer(self):
        # Function to handle the countdown logic based on the selected tab

        # Reset flags and get the selected tab
        self.stopped = False
        self.skipped = False
        tab_selected = self.tabview.get()

        if tab_selected == "Pomodoro":
            full_seconds = 60 * 25
            while full_seconds > 0 and not self.stopped:
                # Update and display the timer
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}")
                self.window.update()
                time.sleep(1)
                full_seconds -= 1

            # Check if the timer was not stopped or skipped
            if not self.stopped or self.skipped:
                # Increment Pomodoros count and update the display
                self.pomodoros += 1
                self.pomodoro_label.configure(
                    text=f"Pomodoros: {self.pomodoros}")

                # Switch to either Short Break or Long Break based on the count
                if self.pomodoros % 4 == 0:
                    self.tabview.set("Long Break")
                else:
                    self.tabview.set("Short Break")

                # Start the timer for the next session
                self.start_timer()

        elif tab_selected == "Short Break":
            # Similar logic for Short Break
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
            # Similar logic for Long Break
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
        # Function to start the timer in a separate thread
        if not self.running:
            self.running = True
            t = threading.Thread(target=self.start_timer)
            t.start()

    def reset_timer(self):
        # Function to reset the timer and related variables
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoro_timer_label.configure(text="25:00")
        self.short_break_timer_label.configure(text="05:00")
        self.long_break_timer_label.configure(text="30:00")
        self.pomodoro_label.configure(text="Pomodoros: 0")
        self.running = False

    def pause_timer(self):
        # Placeholder for the pause functionality
        pass

    def skip_timer(self):
        # Function to skip the current session and reset the timer

        # Get the selected tab and reset the timer label accordingly
        tab_selected = self.tabview.get()
        if tab_selected == "Pomodoro":
            self.pomodoro_timer_label.configure(text="25:00")
        elif tab_selected == "Short Break":
            self.short_break_timer_label.configure(text="05:00")
        elif tab_selected == "Long Break":
            self.long_break_timer_label.configure(text="30:00")

        # Set flags to indicate the session was skipped
        self.skipped = True
        self.stopped = True

    def settings(self):
        # Placeholder for the settings functionality
        pass


if __name__ == '__main__':
    # Create an instance of the Pomodoro class and start the application
    Pomodoro()