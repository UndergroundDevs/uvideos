from subprocess import call, STDOUT
from os import path as os_path, devnull, remove as remove_file
from uuid import uuid4
import cv2
from os import listdir


class Video:
    size_of_segments: int = 0
    path: str
    __temp_audio_file_path: str
    __temp_video_file_path: str
    __temp_image_segments_of_a_video_path: str = os_path.join("media", "temp", "segments_of_a_video")

    def __init__(self, path):
        self.path = path

    def get_segment(self, index: int) -> str:
        return os_path.join(self.__temp_image_segments_of_a_video_path, f"segment-{index}.png")

    def divide_into_segments(self) -> None:
        self.__temp_audio_file_path = os_path.join("media", "temp", "audio", f"{uuid4()}-audio.mp3")
        call(["ffmpeg", "-i", self.path, "-q:a", "0", "-map",
              "a", self.__temp_audio_file_path, "-y"],
             stdout=open(devnull, "w"), stderr=STDOUT)

        video = cv2.VideoCapture(self.path)
        count = 0
        while True:
            success, image = video.read()
            if not success:
                break
            cv2.imwrite(os_path.join(self.__temp_image_segments_of_a_video_path,
                                     "segment-{:d}.png".format(count)), image)
            count += 1

        self.size_of_segments = count
        video.release()

    def unify_segments(self, output_path: str) -> None:
        self.__temp_video_file_path = os_path.join("media", "temp", "video", f"{uuid4()}.mov")
        call(["ffmpeg", "-i", os_path.join(self.__temp_image_segments_of_a_video_path, "segment-%d.png"),
              "-vcodec", "png", self.__temp_video_file_path, "-y"], stdout=open(devnull, "w"),
             stderr=STDOUT)
        call(["ffmpeg", "-i", self.__temp_video_file_path, "-i", self.__temp_audio_file_path, "-codec", "copy",
              "data/enc-" + os_path.join(output_path, f"teste.mov"), "-y"], stdout=open(devnull, "w"),
             stderr=STDOUT)
        call(["ffmpeg", "-i", self.__temp_video_file_path, "-i", self.__temp_audio_file_path, "-codec", "copy", os_path.join(output_path, "video.mov"), "-y"],
             stdout=open(devnull, "w"), stderr=STDOUT)

    def clean_temp(self) -> None:
        if os_path.isfile(self.__temp_audio_file_path):
            remove_file(self.__temp_audio_file_path)

        if hasattr(self, '__temp_video_file_path') and os_path.isfile(self.__temp_video_file_path):
            remove_file(self.__temp_video_file_path)

        image_files = listdir(self.__temp_image_segments_of_a_video_path)
        for file in image_files:
            file_path = os_path.join(self.__temp_image_segments_of_a_video_path, file)
            if os_path.isfile(file_path):
                remove_file(file_path)
