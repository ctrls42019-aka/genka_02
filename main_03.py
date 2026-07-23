# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 08:42:43 2026

@author: alalf
"""

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

    def find_image(self, filename):
        """등록된 폴더에서 이미지 파일 찾기"""

        for folder in IMAGE_DIRS:
            image_path = folder / filename

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
#%%


    # Home
    def show_cover(self):
        self.current_page = "cover"

        if not self.show_image("1.jpg"):
            return

        # 전시 안내 시작하기 버튼(전시 소개로)
        self.add_touch_area(
            260, 1730,
            820, 1833,
            self.show_exhibition,
            debug=False
        )
        
        
#%%


    # Sub_01-1
    def show_exhibition(self):
        self.current_page = "exhibition"

        # 안내페이지
        if not self.show_image("2.jpg"):
            return

        # home 버튼
        self.add_touch_area(
            126, 173,
            412, 357,
            self.show_cover,
            debug=False
        )

        # 다음 버튼(재료 소개로)
        self.add_touch_area(
           313, 1728,
           767, 1831,
            self.show_Material,
            debug=False
        )
        
        
#%%


    # Sub_02-1
    def show_Material(self):
        self.current_page = "Material"

        # Sub_02-1
        if not self.show_image("3.jpg"):
            return

        # home 버튼
        self.add_touch_area(
            126, 173,
            412, 357,
            self.show_cover,
            debug=False
        )

        # 다음 버튼(관람 안내로)
        self.add_touch_area(
            313, 1728,
            767, 1831,
            self.show_guide_01,
            debug=False
        )
        
        
#%%

    # Sub_03-1
    def show_guide_01(self):
        self.current_page = "guide_01"

        # Sub_03-1
        if not self.show_image("6_02.jpg"):
            return

        # home 버튼
        self.add_touch_area(
            126, 173,
            412, 357,
            self.show_cover,
            debug=False
        )

        # 다음 버튼(프롤로그로)
        self.add_touch_area(
            313, 1183,
            767, 1287,
            self.show_prolog,
            debug=False
        )
        

#%%


    # prolog
    def show_prolog(self):
        self.current_page = "prolog"

        # Sub_04-1
        if not self.show_image("7_02.jpg"):
            return

        # home 버튼
        self.add_touch_area(
            126, 173,
            412, 357,
            self.show_cover,
            debug=False
        )

        # 감정 기록 시작 버튼
        # 임시로 전시 지도 버튼으로 사용
        self.add_touch_area(
            313, 1992,
            767, 2095,
            
            # 여기서 map_01로 안넘어가요
            self.show_map_01,
            debug=lseFa
        )
        
        
        

#%%



# 모르겠어요...ㅜㅠ
# 스크롤 형식 구현...
"""
    # prolog_1_2
    def show_prolog_1_2(self):
        self.current_page = "prolog_1_2"

        # Sub_04-1
        if not self.show_image("7.jpg"):
            return

        # home 버튼
        self.add_touch_area(
            126, 173,
            412, 357,
            self.show_cover,
            debug=False
        )

        # 감정 기록 시작 버튼
        self.add_touch_area(
            313, 1992,
            767, 2095,
            self.show_map_01,
            debug=False
        )
        
     """
     
     
#%%

# 여기도요...
# ai이용한 결과값 띄우기 구현...

"""
"""

#%%

    
    # map_01
    def show_map_01(self):
        self.current_page = "map_01"

        # Sub_04-1
        if not self.show_image("11.jpg"):
            return

        # home 버튼
        self.add_touch_area(
            126, 173,
            412, 357,
            self.show_cover,
            debug=False
        )
        
        
#%%
# 전시지도 페이지 위치버튼


        # 01흔들리다 버튼_1
        self.add_touch_area(
            173, 1451,
            517, 1557,
            self.show_map_02_1,
            debug=False
        )
        
        
        # 02조여들다 버튼_1
        self.add_touch_area(
            173, 1589,
            517, 1692,
            self.show_map_02_2,
            debug=False
        )
        
        
          # 03마주보다 버튼_1
        self.add_touch_area(
            173, 1724,
            517, 1827,
            self.show_map_02_3,
            debug=False
        )
        
         # 04고르다 버튼_1
        self.add_touch_area(
            173, 1859,
            517, 1962,
            self.show_map_02_4,
            debug=False
        )
        
        
         # 05만들다 버튼_1
        self.add_touch_area(
            563, 1454,
            907, 1557,
            self.show_map_02_5,
            debug=False
        )
        
        
          # 06머무르다 버튼_1
        self.add_touch_area(
            563, 1589,
            907, 1692,
            self.show_map_02_6,
            debug=False
        )
        
        
         # 07비추다 버튼_1
        self.add_touch_area(
            563, 1724,
            907, 1827,
            self.show_map_02_7,
            debug=False
        )
        
        
         # 08기록하다 버튼_1
        self.add_touch_area(
            563, 1859,
            907, 1962,
            self.show_map_02_8,
            debug=False
        )
        
        #%%
        # 지도 맵 그림 이동 버튼
        
        
         # 01흔들리다 버튼_2
        self.add_touch_area(
            449, 686,
            559, 739,
            self.show_map_02_1,
            debug=False
        )
        # 02조여들다 버튼_2
        self.add_touch_area(
            339, 686,
            449, 817,
            self.show_map_02_2,
            debug=False
        )
        
      
        
        # 03마주보다 버튼_2
        self.add_touch_area(
            449, 742,
            614, 968,
            self.show_map_02_3,
            debug=False
        )
        
       
        
        # 04고르다 버튼_2
        self.add_touch_area(
            229, 818,
            449, 914,
            self.show_map_02_4,
            debug=False
        )
        
        # 04고르다 버튼_3
        self.add_touch_area(
            229, 914,
            339, 979,
            self.show_map_02_4,
            debug=False
        )
        
       
        
        # 05만들다 버튼_2
        self.add_touch_area(
            229, 979,
            336, 1130,
            self.show_map_02_5,
            debug=False
        )
        
        # 05만들다 버튼_3
        self.add_touch_area(
            339, 1027,
            449, 1130,
            self.show_map_02_5,
            debug=False
        )
        
      
        
        # 06머무르다 버튼_2
        self.add_touch_area(
            339, 914,
            449, 1024,
            self.show_map_02_6,
            debug=False
        )
        
        # 06머무르다 버튼_3
        self.add_touch_area(
            449, 968,
            614, 1024,
            self.show_map_02_6,
            debug=False
        )
        
        # 06머무르다 버튼_4
        self.add_touch_area(
            614, 854,
            708, 1024,
            self.show_map_02_6,
            debug=False
        )
        
       
        
        # 07비추다 버튼_2
        self.add_touch_area(
            614, 739,
            779, 854,
            self.show_map_02_7,
            debug=False
        )
        
       
        
        # 08기록하다 버튼_2
        self.add_touch_area(
            708, 854,
            851, 1125,
            self.show_map_02_8,
            debug=False
        )
        
#%%


    # map_02_1
    def show_map_02_1(self):
        self.current_page = "map_02_1"

        # Sub_04-1
        if not self.show_image("11.jpg"):
            return
        
        # home 버튼
        self.add_touch_area(
            126, 173,
            412, 357,
            self.show_cover,
            debug=False
        )
#%%


    def previous_page(self):
        """Esc 키를 눌렀을 때 이전 화면으로 이동"""

        if self.current_page == "exhibition":
            self.show_cover()

        elif self.current_page == "guide":
            self.show_exhibition()

#%%


if __name__ == "__main__":
    app = EmotionWeb()
    app.mainloop()