import os
from stegano import lsb
from video import Video


class DigitalWaterMark:
    def encode_image(self, input_image_path: str, message: str, output_image_path: str) -> str:
        image_secrete = lsb.hide(input_image_path, message)
        image_secrete.save(output_image_path)
        return output_image_path

    def decode_image(self, input_path) -> str:
        return lsb.reveal(input_path)

    def encode_video(self, input_video_path: str, message: str,
                     segments_of_a_video: int, output_video_path: str) -> str:
        video = Video(input_video_path)
        if not os.path.isfile(input_video_path):
            raise Exception("Invalid video file")
        video.divide_into_segments()
        if segments_of_a_video >= video.size_of_segments:
            raise Exception("Invalid segment")

        self.encode_image(video.get_segment(segments_of_a_video), message, video.get_segment(segments_of_a_video))
        video.unify_segments(output_video_path)
        video.clean_temp()
        return output_video_path

    def decode_video(self, input_video_path: str, segments_of_a_video: int) -> str:
        video = Video(input_video_path)
        if not os.path.isfile(input_video_path):
            raise Exception("Invalid video file")
        video.divide_into_segments()
        if segments_of_a_video >= video.size_of_segments:
            raise Exception("Invalid segment")

        try:
            message: str = self.decode_image(video.get_segment(segments_of_a_video))
            return message
        except IndexError:
            raise Exception("Impossible to detect message.")
        finally:
            video.clean_temp()


digital_water_mark = DigitalWaterMark()
# digital_water_mark.encode_image(
#     "./media/input/avatar.png",
#     "hello world",
#     "./media/output/avatar.png")
# print(digital_water_mark.decode_image("./media/output/avatar.png"))
# digital_water_mark.encode_video(os.path.join("media", "input", "Danceoff.mp4"),
#                                 "Hello World", 10, os.path.join("media", "output"))
dwm = digital_water_mark.decode_video(input_video_path=os.path.join("media", "input", "Danceoff.mp4"),
                                      segments_of_a_video=10)
print(dwm)
