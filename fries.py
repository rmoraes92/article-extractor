# TODO why is this named fries?
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class TestRunnerHandler(FileSystemEventHandler):
    def __init__(self, test_command):
        super().__init__()
        self.test_command = test_command

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            print(f"File modified: {event.src_path} - Running tests...")
            self.run_tests()

    def run_tests(self):
        try:
            subprocess.run(self.test_command, check=True, shell=True)
            # print("Tests passed!")
        except subprocess.CalledProcessError as e:
            print(f"Tests failed!:\n{e}")
        except Exception as e:
            print(f"An error occurred while running tests:\n{e}")


if __name__ == "__main__":
    # Define the directory to watch and the test command
    watch_directory = "."  # Watch the current directory
    test_command = "poetry run python -m unittest discover"
    # Or "pytest"
    event_handler = TestRunnerHandler(test_command)
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=True)
    observer.start()

    print(f"Watching directory: {watch_directory} for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

