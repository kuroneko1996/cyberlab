from enum import Enum

class PlayMode(Enum):
    NORMAL = 0
    LOOP = 1


class Animation:
    def __init__(self, frame_duration, play_mode, *keyframes):
        self.frame_duration = frame_duration
        self.play_mode = play_mode

        self.key_frames = []
        for frame in keyframes:
            self.key_frames.append(frame)

    def get_key_frame(self, time):
        return self.key_frames[self.get_key_frame_index(time)]

    def get_key_frame_by_index(self, index):
        return self.key_frames[index]

    def get_key_frame_index(self, time):
        if len(self.key_frames) == 1:
            return 0

        frame_number = int(time / self.frame_duration)
        if self.play_mode == PlayMode.NORMAL:
            frame_number = min(len(self.key_frames) - 1, frame_number)
        elif self.play_mode == PlayMode.LOOP:
            frame_number = frame_number % len(self.key_frames)

        return frame_number
