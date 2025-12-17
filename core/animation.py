import pygame

class Animation:
    def __init__(self, frames, frame_duration):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_time = 0
        self.current_frame_index = 0

    def update(self, dt):
        """
        Updates the animation state based on delta time (dt in milliseconds).
        """
        self.current_time += dt
        if self.current_time >= self.frame_duration:
            self.current_time = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame_index]

def load_sprite_sheet(path, frame_width, frame_height, scale=None):
    """
    Loads a sprite sheet and returns a list of surfaces (frames).
    """
    try:
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        frames = []
        for x in range(0, sheet_width, frame_width):
            # If the remaining width is less than frame_width, stop (avoids partial frames)
            if x + frame_width > sheet_width:
                break
            rect = pygame.Rect(x, 0, frame_width, frame_height)
            frame = sheet.subsurface(rect)
            if scale:
                frame = pygame.transform.scale(frame, scale)
            frames.append(frame)
        return frames
    except Exception as e:
        print(f"[ERROR] Failed to load sprite sheet {path}: {e}")
        return []
