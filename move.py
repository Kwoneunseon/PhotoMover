import os
import shutil

class Move:
    def __init__(self, dest_folder, image_list):
        self.dest_folder = dest_folder #목적지 폴더
        self.image_list = image_list #파일 이미지 
   
    
    def move_image_to_folder(self, image_path, year, month):
        try:
            """
            주어진 연/월 정보를 기반으로 목적지 폴더 내에 폴더를 생성하고 이미지를 이동합니다.
            이미지가 이동된 후 원본 이미지를 삭제합니다.

            :param image_path: 이미지 파일 경로
            :param year: 연도 (예: 2023)
            :param month: 월 (예: 6)
            :param dest_folder: 목적지 폴더 경로
            """
            # 연/월 폴더 경로 생성
            year_folder = os.path.join(self.dest_folder, str(year))
            month_folder = os.path.join(year_folder, f"{month:02d}")
            
            # 연/월 폴더가 존재하지 않으면 생성
            if not os.path.exists(year_folder):
                os.makedirs(year_folder)
            if not os.path.exists(month_folder):
                os.makedirs(month_folder)
            
            # 이미지 파일 이름 추출
            image_name = os.path.basename(image_path)
            
            # 목적지 파일 경로
            dest_path = os.path.join(month_folder, image_name)
            
            # 이미지 이동
            shutil.move(image_path, dest_path)
            print(f"Moved {image_path} to {dest_path}")
        except Exception as e:
            print(f"오류발생 : {e}")
        

    def process(self):
        for image_path, year, month in self.image_list:
            self.move_image_to_folder(image_path, year, month)