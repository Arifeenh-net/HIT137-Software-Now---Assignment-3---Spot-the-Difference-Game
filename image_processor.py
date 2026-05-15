import cv2 as cv
import numpy as np
from PIL import Image, ImageTk
import random

class ImageProcessor:
    def __init__(self, copy_img_label, ori_img_label):
        # label we draw the altered image onto
        self.copy_img_label = copy_img_label
        self.ori_img_label = ori_img_label

    def create_copy(self, original):
        # convert PIL image to numpy (OpenCV format)
        self.img = np.array(original)

        # OpenCV uses BGR instead of RGB
        self.img_bgr = cv.cvtColor(self.img, cv.COLOR_RGB2BGR)

        # working copy so original stays unchanged
        self.modified = self.img_bgr.copy()
        self.original_display = self.img_bgr.copy()

        self.generate_differences(self.modified)
        self.refresh_display()
        self.refresh_original()

    def generate_differences(self, modified_image, n=5, min_separation=80):
        self.differences = []
        h, w = modified_image.shape[:2]
        placed = []

        for i in range(n):

            # ensure differences aren't too close together
            while True:
                cx = random.randint(50, w - 50)
                cy = random.randint(50, h - 50)

                if not any(
                    abs(cx - px) < min_separation and abs(cy - py) < min_separation
                    for px, py in placed
                ):
                    break

            placed.append((cx, cy))

            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

            # create different types of visual changes
            if i == 0:
                radius = random.randint(5, 8)
                cv.circle(modified_image, (cx, cy), radius, color, -1)
                self.differences.append(("circle", cx, cy, radius))

            elif i == 1:
                rw = random.randint(5, 15)
                rh = random.randint(5, 15)
                cv.rectangle(modified_image, (cx, cy), (cx + rw, cy + rh), color, -1)
                self.differences.append(("rectangle", cx, cy, rw, rh))

            elif i == 2:
                # blur region
                size = 20
                x1, y1 = max(0, cx - size), max(0, cy - size)
                x2, y2 = min(w, cx + size), min(h, cy + size)

                region = modified_image[y1:y2, x1:x2]
                modified_image[y1:y2, x1:x2] = cv.GaussianBlur(region, (15, 15), 0)

                self.differences.append(("blur", cx, cy, size))

            elif i == 3:
                # blacked out region
                size = 10
                x1, y1 = max(0, cx - size), max(0, cy - size)
                x2, y2 = min(w, cx + size), min(h, cy + size)

                modified_image[y1:y2, x1:x2] = 0
                self.differences.append(("blackout", cx, cy, size))

            elif i == 4:
                # flipped patch
                size = 16
                x1, y1 = max(0, cx - size), max(0, cy - size)
                x2, y2 = min(w, cx + size), min(h, cy + size)

                region = modified_image[y1:y2, x1:x2].copy()
                modified_image[y1:y2, x1:x2] = cv.flip(region, 0)

                self.differences.append(("flip", cx, cy, size))

    def find_hit(self, x, y, exclude: set) -> int | None:
        # check if click matches any unresolved difference
        for i, diff in enumerate(self.differences):

            if i in exclude:
                continue

            name = diff[0]

            if name == "circle":
                _, cx, cy, radius = diff
                hit = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 <= radius + 15

            elif name == "rectangle":
                _, cx, cy, rw, rh = diff
                hit = (cx - 15 < x < cx + rw + 15) and (cy - 15 < y < cy + rh + 15)

            else:
                _, cx, cy, size = diff
                hit = abs(x - cx) < size + 15 and abs(y - cy) < size + 15

            if hit:
                return i

        return None

    def get_center(self, index: int) -> tuple[int, int]:
        # return stored center position of a difference
        _, cx, cy = self.differences[index][:3]
        return cx, cy

    def mark_difference(self, cx, cy, color=(0, 0, 255)):
        # draw green circle where difference was found
        cv.circle(self.modified, (cx, cy), 20, color, 2)
        self.refresh_display()
    def mark_original(self, cx, cy, color=(0, 0, 255)):
        # draw matching circle on the original image display
        cv.circle(self.original_display, (cx, cy), 20, color, 2)
        self.refresh_original()
    def refresh_display(self):
        # update Tkinter image
        img_rgb = cv.cvtColor(self.modified, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img)

        self.copy_img_label.configure(image=img_tk)
        self.copy_img_label.image = img_tk
    def refresh_original(self):
        # update Tkinter original image
        img_rgb = cv.cvtColor(self.original_display, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img)

        self.ori_img_label.configure(image=img_tk)
        self.ori_img_label.image = img_tk