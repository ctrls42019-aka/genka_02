# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 09:31:57 2026

@author: alalf
"""

#%%

"""오늘의 감정 기록하기 - 1080 x 2280 고정형 전시 프로그램."""

from __future__ import annotations

import shutil
import tkinter as tk
from datetime import datetime
from pathlib import Path


WIDTH, HEIGHT = 1080, 2280
ROOT = Path(__file__).resolve().parent
IMAGE_DIR = ROOT / "images"
RECORD_DIR = ROOT / "records"

EMOTIONS = [
    ("불안", "04-anxiety.png"),
    ("긴장", "05-tension.png"),
    ("혼란", "06-confusion.png"),
    ("마주함", "07-facing.png"),
    ("해방", "08-release.png"),
    ("안정", "09-calm.png"),
    ("회복", "10-recovery.png"),
]

SHAPES = [
    ("계속 맴돌고 있어요.", "14-loop.png"),
    ("복잡하게 엉켜 있어요.", "15-tangle.png"),
    ("단단히 묶여 있어요.", "17-knot.png"),
    ("조금씩 풀리고 있어요.", "18-untying.png"),
    ("자연스럽게 흘러가고 있어요.", "19-flow.png"),
]


class EmotionKiosk:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("오늘의 감정 기록하기")
        self.root.geometry(f"{WIDTH}x{HEIGHT}+0+0")
        self.root.resizable(False, False)
        self.root.configure(bg="#fbf6ee")

        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH,
            height=HEIGHT,
            bg="#fbf6ee",
            highlightthickness=0,
            cursor="hand2",
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Escape>", lambda _e: self.root.destroy())
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Home>", lambda _e: self.reset())

        self.images: dict[str, tk.PhotoImage] = {}
        self.screen = "intro"
        self.emotion_index: int | None = None
        self.density = 2
        self.shape_index: int | None = None
        self.fullscreen = False
        self.notice_id: int | None = None
        self.show("02-intro.png")

    def image(self, filename: str) -> tk.PhotoImage:
        if filename not in self.images:
            path = IMAGE_DIR / filename
            if not path.exists():
                raise FileNotFoundError(f"화면 이미지가 없습니다: {path}")
            self.images[filename] = tk.PhotoImage(file=path)
        return self.images[filename]

    def show(self, filename: str) -> None:
        self.current_file = filename
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.image(filename), anchor="nw")

    @staticmethod
    def inside(x: int, y: int, box: tuple[int, int, int, int]) -> bool:
        left, top, right, bottom = box
        return left <= x <= right and top <= y <= bottom

    def on_click(self, event: tk.Event) -> None:
        x, y = int(event.x), int(event.y)

        if self.screen == "intro":
            if self.inside(x, y, (245, 1570, 835, 1685)):
                self.screen = "emotion"
                self.show("04-emotion.png")
            return

        if self.screen == "emotion":
            for index in range(7):
                top = 690 + index * 135
                if self.inside(x, y, (235, top, 815, top + 100)):
                    self.emotion_index = index
                    self.show(EMOTIONS[index][1])
                    return
            if self.emotion_index is not None and self.inside(x, y, (280, 1700, 800, 1830)):
                self.screen = "density"
                self.show("12-density.png")
            return

        if self.screen == "density":
            if self.inside(x, y, (180, 710, 900, 900)):
                self.density = max(1, min(5, round((x - 180) / 180) + 1))
                self.show("12-density.png")
                self.draw_density_marker()
                return
            if self.inside(x, y, (280, 1030, 800, 1160)):
                self.screen = "shape"
                self.show("13-shape.png")
            return

        if self.screen == "shape":
            for index in range(5):
                top = 700 + index * 108
                if self.inside(x, y, (155, top, 900, top + 80)):
                    self.shape_index = index
                    self.show(SHAPES[index][1])
                    return
            if self.shape_index is not None and self.inside(x, y, (260, 1300, 820, 1430)):
                self.screen = "result"
                self.show("21-result.png")
            return

        if self.screen == "result":
            if self.inside(x, y, (365, 1815, 500, 2010)):
                self.save_record()
            elif self.inside(x, y, (520, 1815, 670, 2010)):
                self.copy_share_text()

    def draw_density_marker(self) -> None:
        x = 200 + (self.density - 1) * 165
        self.canvas.create_oval(x - 43, 746, x + 43, 832, fill="white", outline="")
        self.canvas.create_text(x, 788, text="✓", fill="#c68284", font=("Arial", 42, "bold"))
        self.canvas.create_text(
            WIDTH // 2,
            665,
            text=f"오늘의 감정 밀도: {self.density}단계",
            fill="#c68284",
            font=("Malgun Gothic", 28),
        )

    def save_record(self) -> None:
        RECORD_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = RECORD_DIR / f"emotion-record-{timestamp}.png"
        shutil.copy2(IMAGE_DIR / self.current_file, target)
        self.notice(f"기록을 저장했습니다\n{target.name}")

    def copy_share_text(self) -> None:
        emotion = EMOTIONS[self.emotion_index or 0][0]
        shape = SHAPES[self.shape_index or 0][0]
        text = f"오늘의 감정 기록: {emotion}, 밀도 {self.density}단계, {shape}"
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.notice("공유 문구를 복사했습니다.")

    def notice(self, text: str) -> None:
        if self.notice_id:
            self.canvas.delete(self.notice_id)
        self.notice_id = self.canvas.create_text(
            WIDTH // 2,
            1060,
            text=text,
            width=760,
            justify="center",
            fill="#5f5a52",
            font=("Malgun Gothic", 28),
        )
        self.root.after(2200, self.clear_notice)

    def clear_notice(self) -> None:
        if self.notice_id:
            self.canvas.delete(self.notice_id)
            self.notice_id = None

    def toggle_fullscreen(self, _event: tk.Event | None = None) -> None:
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def reset(self) -> None:
        self.screen = "intro"
        self.emotion_index = None
        self.density = 2
        self.shape_index = None
        self.show("02-intro.png")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    EmotionKiosk().run()
