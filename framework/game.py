import pygame
import time
from typing import List

class Game:
    def __init__(self):
        pygame.init()

        self.isRunning = True
        self.screen = pygame.display.set_mode((1000, 800))
        self.font = pygame.font.SysFont("monospace", 16)

        # Rects
        self.story_rect = pygame.Rect(0, 0, 700, 800)
        self.info_rect = pygame.Rect(700, 0, 300, 800)

        # Buffers
        self.story_buffer = []
        self.info_buffer = []

        # Game Values
        self.party: List[character.Character] = []

        # Scroll positions
        self.story_scroll = 0
        self.info_scroll = 0

    def handleLoop(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEWHEEL:
                    mx, _ = pygame.mouse.get_pos()
                    if mx < self.story_rect.width:
                        self.story_scroll += event.y * 20
                        content_h = self.get_story_height()
                        max_scroll = min(0, self.story_rect.height - content_h)
                        self.story_scroll = max(max_scroll, min(0, self.story_scroll))
                    else:
                        self.info_scroll += event.y * 20
                        content_h = self.get_info_height()
                        max_scroll = min(0, self.info_rect.height - content_h)
                        self.info_scroll = max(max_scroll, min(0, self.info_scroll))

        # Similar clamping logic for info

            self.screen.fill((255, 255, 255))

            # Draw panes
            self.draw_pane(self.story_buffer, self.story_rect, self.story_scroll, 0)
            self.draw_pane(self.info_buffer, self.info_rect, self.info_scroll, self.story_rect.width)

            # Draw divider line
            pygame.draw.line(self.screen, (0, 0, 0), 
                             (self.story_rect.width, 0), 
                             (self.story_rect.width, 800))

            pygame.display.flip()
            time.sleep(0.01)

        pygame.quit()

    def quit(self):
        self.isRunning = False

    def writeText(self, text):
        if (len(self.story_buffer) > 0):
            surface = self.font.render("A", True, (0, 0, 0))
            self.story_buffer.append({"type": "text", "content": "", "surface": surface, "height": surface.get_height()})

        wrapped = self.wrap_text(text, self.font, self.story_rect.width - 20)
        for line in wrapped:
            surf = self.font.render(line, True, (0, 0, 0))
            entry = {
                "type": "text",
                "content": line,
                "surface": surf,
                "height": surf.get_height() + 5
            }
            self.story_buffer.append(entry)

    def showImage(self, path):
        image = pygame.image.load(path)
        iw, ih = image.get_size()

        max_width = self.story_rect.width - 20  # padding
        if iw > max_width:
            scale = max_width / iw
            iw, ih = max_width, int(ih * scale)
            image = pygame.transform.smoothscale(image, (iw, ih))

        entry = {
            "type": "image",
            "surface": image,
            "width": iw,
            "height": ih
        }
        self.story_buffer.append(entry)

    def infoText(self, text):
        wrapped = self.wrap_text(text, self.font, self.info_rect.width - 20)
        for line in wrapped:
            surf = self.font.render(line, True, (0, 0, 0))
            entry = {
                "type": "text",
                "content": line,
                "surface": surf,
                "height": surf.get_height() + 5
            }
            self.info_buffer.append(entry)

    def clearStory(self):
        self.story_buffer = []
        self.story_scroll = 0

    def clearInfo(self):
        self.info_buffer = []
        self.info_scroll = 0

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines, line = [], ""
        for word in words:
            test_line = f"{line} {word}".strip()
            if font.size(test_line)[0] <= max_width - 10:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    def draw_pane(self, buffer, rect, scroll, x_offset):
        y = scroll
        for entry in buffer:
            if entry["type"] == "text":
                self.screen.blit(entry["surface"], (x_offset + 10, y))
            elif entry["type"] == "image":
                x = x_offset + (rect.width - entry["width"]) // 2
                self.screen.blit(entry["surface"], (x, y))
            y += entry["height"]

    def get_story_height(self):
        total = 0
        for entry in self.story_buffer:
            if entry["type"] == "text":
                total += self.font.get_height() + 5
            elif entry["type"] == "image":
                total += entry["height"] + 10
        return total

    def get_info_height(self):
        total = 0

        for entry in self.info_buffer:
            if entry["type"] == "text":
                total += self.font.get_height() + 5
            elif entry["type"] == "image":
                total += entry["height"] + 10

        return total

import framework.character as character