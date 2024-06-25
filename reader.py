import os
from PIL import Image
from PIL.ExifTags import TAGS
import datetime
import pillow_heif

class Reader:
    def __init__(self, folder_path, count):
        self.folder_path = folder_path
        self.count = count
        self.image_list = []

    def get_exif_data(self, image):
        exif_data = {}
        try:
            info = image._getexif()
            if info is not None:
                for tag, value in info.items():
                    tag_name = TAGS.get(tag, tag)
                    exif_data[tag_name] = value
        except AttributeError:
            pass
        return exif_data

    def get_creation_date(self,exif_data):
        creation_date = exif_data.get("DateTimeOriginal")
        if creation_date:
            return datetime.datetime.strptime(creation_date, "%Y:%m:%d %H:%M:%S")
        return None

    def get_file_creation_date(self,file_path):
        return datetime.datetime.fromtimestamp(os.path.getctime(file_path))

    def process_images(self,):
        for file_name in os.listdir(self.folder_path):
            if len(self.image_list) > self.count:
                return self.image_list
            if len(self.image_list)!= 0 and len(self.image_list) % 100 == 0:
                print(f"{len(self.image_list)}개 파일 읽기 진행중")
            try:
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    file_path = os.path.join(self.folder_path, file_name)                
                    with Image.open(file_path) as img:
                        exif_data = self.get_exif_data(img)
                        exif_creation_date = self.get_creation_date(exif_data)
                        file_creation_date = self.get_file_creation_date(file_path)
                        
                        if exif_creation_date:
                            year = exif_creation_date.year
                            month = exif_creation_date.month
                        else:
                            #print("EXIF Creation Date: Not available")
                            year = file_creation_date.year
                            month = file_creation_date.month

                        self.image_list.append((file_path, year, month))
                elif file_name.lower().endswith(('.mp4','.mov')):
                    file_path = os.path.join(self.folder_path, file_name) 
                    creation_time = os.path.getctime(file_path)
                    creation_date = datetime.datetime.fromtimestamp(creation_time)
                    year = creation_date.year
                    month = creation_date.month    

                    self.image_list.append((file_path, year, month))     
                elif file_name.lower().endswith(('.heic')):
                    file_path = os.path.join(self.folder_path, file_name)                    
                    jpeg_file = os.path.join(self.folder_path, os.path.splitext(file_name)[0]) +".jpeg"
                    heif_file = pillow_heif.read_heif(file_path)
                    image = Image.frombytes(
                        heif_file.mode,
                        heif_file.size,
                        heif_file.data,
                        "raw",
                    ) 
                    image.save(jpeg_file, format("jpeg"))
                    creation_time = os.path.getctime(file_path)
                    creation_date = datetime.datetime.fromtimestamp(creation_time)
                    year = creation_date.year
                    month = creation_date.month    

                    os.remove(file_path)
                    self.image_list.append((jpeg_file, year, month))    
                   
            except Exception as e:
                print(f"Could not process file {file_name}: {e}")
        
        return self.image_list
    
        

