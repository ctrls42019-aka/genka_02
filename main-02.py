# -*- coding: utf-8 -*-

import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk


# PC에서 표시할 모바일 창 크기
WINDOW_WIDTH = 426
WINDOW_HEIGHT = 900

# 이미지가 들어 있는 폴더
IMAGE_DIRS = [
    Path(r"D:\genka-02\image\M-guide"),
    Path(r"D:\genka-02\image"),
]


class EmotionWeb(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("결: 감정의 기록")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg="#6A6257")

        self.current_image = None
        self.current_page = "cover"

        # 이미지 배율 및 위치 기본값
        self.scale = 1
        self.offset_x = 0
        self.offset_y = 0

        self.canvas = tk.Canvas(
            self,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg="#FFF9F1",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # 전시 안내 시작하기 누르면 다음으로
        self.bind(
            "<Escape>",
            lambda event: self.previous_page()
        )

        # 첫 화면 표시
        self.show_cover()

    def find_image(self, 2.jpg):
        """등록된 폴더에서 이미지 파일 찾기"""

        for folder in IMAGE_DIRS:
            image_path = folder / 2.jpg

            if image_path.exists():
                return image_path

        return None

    def show_image(self, filename):
        """이미지를 읽고 창 크기에 맞게 표시"""

        self.canvas.delete("all")

        image_path = self.find_image(filename)

        if image_path is None:
            searched_folders = "\n".join(
                str(folder) for folder in IMAGE_DIRS
            )

            self.canvas.create_text(
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
                text=(
                    "이미지를 찾을 수 없습니다.\n\n"
                    f"파일 이름: {filename}\n\n"
                    f"검색한 폴더:\n{searched_folders}"
                ),
                fill="#6A6257",
                font=("맑은 고딕", 12),
                justify="center"
            )
            return False

        # with를 사용하면 이미지 파일이 안전하게 닫힘
        with Image.open(image_path) as opened_image:
            original = opened_image.convert("RGB")

            width_ratio = WINDOW_WIDTH / original.width
            height_ratio = WINDOW_HEIGHT / original.height

            # 원본 비율 유지
            self.scale = min(width_ratio, height_ratio)

            display_width = round(original.width * self.scale)
            display_height = round(original.height * self.scale)

            resized = original.resize(
                (display_width, display_height),
                Image.Resampling.LANCZOS
            )

        self.current_image = ImageTk.PhotoImage(
            resized,
            master=self
            )

        # 이미지 가운데 정렬
        self.offset_x = (WINDOW_WIDTH - display_width) // 2
        self.offset_y = (WINDOW_HEIGHT - display_height) // 2

        self.canvas.create_image(
            self.offset_x,
            self.offset_y,
            image=self.current_image,
            anchor="nw"
        )

        return True

    def add_touch_area(
        self,
        x1,
        y1,
        x2,
        y2,
        command,
        debug=False
    ):
        """원본 이미지 좌표를 기준으로 터치 영역 생성"""

        screen_x1 = self.offset_x + x1 * self.scale
        screen_y1 = self.offset_y + y1 * self.scale
        screen_x2 = self.offset_x + x2 * self.scale
        screen_y2 = self.offset_y + y2 * self.scale

        area = self.canvas.create_rectangle(
            screen_x1,
            screen_y1,
            screen_x2,
            screen_y2,
            fill="",
            outline="red" if debug else "",
            width=2
        )

        self.canvas.tag_bind(
            area,
            "<Button-1>",
            lambda event: command()
        )

        self.canvas.tag_bind(
            area,
            "<Enter>",
            lambda event: self.canvas.configure(cursor="hand2")
        )

        self.canvas.tag_bind(
            area,
            "<Leave>",
            lambda event: self.canvas.configure(cursor="")
        )

    # 1번 화면
    def show_cover(self):
        self.current_page = "cover"

        if not self.show_image("1.jpg"):
            return

        # 원본 이미지 기준 시작 버튼 영역
        self.add_touch_area(
            180, 1750,
            900, 2050,
            self.show_exhibition,
            debug=True
        )

    # 2번 화면
    def show_exhibition(self):
        self.current_page = "exhibition"

        # 실제 두 번째 이미지 이름으로 수정
        if not self.show_image("2.jpg"):
            return

        # 이전 버튼
        self.add_touch_area(
            40, 60,
            250, 250,
            self.show_cover,
            debug=True
        )

        # 다음 버튼
        self.add_touch_area(
            180, 1750,
            900, 2050,
            self.show_guide,
            debug=True
        )

    # 3번 화면
    def show_guide(self):
        self.current_page = "guide"

        # 실제 세 번째 이미지 이름으로 수정
        if not self.show_image("3.jpg"):
            return

        # 이전 버튼
        self.add_touch_area(
            40, 60,
            250, 250,
            self.show_exhibition,
            debug=True
        )

        # 표지로 돌아가기
        self.add_touch_area(
            180, 1750,
            900, 2050,
            self.show_cover,
            debug=True
        )

    def previous_page(self):
        """Esc 키를 눌렀을 때 이전 화면으로 이동"""

        if self.current_page == "exhibition":
            self.show_cover()

        elif self.current_page == "guide":
            self.show_exhibition()


if __name__ == "__main__":
    app = EmotionWeb()
    app.mainloop()