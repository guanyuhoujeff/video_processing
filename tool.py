import os
import cv2
from zipfile import ZipFile
import shutil
from google.colab import files

def checkAndMkdirs(the_path):
    if os.path.isdir(os.path.join(the_path)):
        shutil.rmtree(the_path)
    os.makedirs(the_path)


def video2Image(file_name, freq, sub_file_name = 'png'):
    folder_name = file_name.split('.')[0]
    output_path = 'image-%s'%folder_name
    checkAndMkdirs(output_path)
    cap = cv2.VideoCapture(os.path.join(os.getcwd(), file_name))
    counter = 0
    frame_idx = 0
    successed, frame = cap.read()
    if successed:
        cv2.imwrite(os.path.join(os.getcwd(), output_path, f'{folder_name}_{counter}.{sub_file_name}'), frame)
        while successed:
            successed, frame = cap.read()
            counter +=1
            if successed and (counter % freq ==0):
                frame_idx +=1
                cv2.imwrite(os.path.join(os.getcwd(), output_path, f'{folder_name}_{frame_idx}.{sub_file_name}'), frame)
    cap.release()

def zipImage(file_name, sub_file_name = 'png'):
    folder_name = file_name.split('.')[0]
    output_path = 'image-%s'%folder_name
    zipname = '%s.zip'%folder_name
    with ZipFile(zipname, 'w') as zipf:
        for file in [f for f in  os.listdir(output_path) if f".{sub_file_name}" in f]:
            zipf.write(os.path.join(output_path, file))
    return zipname
    

class VideoProcessesor:
    def __init__(self) -> None:
        self.uploaded = None
        self.sub_file_name = None
        
    def uploadFile(self):
        self.uploaded  = files.upload()
        for file_name in self.uploaded .keys():
            print('已上傳 "{name}" '.format(name=file_name))
    
    def convertImage(self, freq, sub_file_name):
        self.sub_file_name = sub_file_name
        for file_name in self.uploaded.keys():
            video2Image(file_name, freq, sub_file_name = sub_file_name)
            print('已處理 "{name}" '.format(name=file_name))
            
    def downloadZip(self):
        for file_name in self.uploaded.keys():
            print(f'準備下載{file_name}')
            zipname = zipImage(file_name, self.sub_file_name)
            files.download(zipname)