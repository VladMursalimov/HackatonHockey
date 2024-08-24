import argparse
import annotation
import frames_to_video

def main():
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description='Process video and annotations.')
    parser.add_argument('--modelPath', type=str, required=True, help='Path to the YOLO model .pt')
    parser.add_argument('--videoPath', type=str, required=True, help='Path to the video file .mp4')

    # Чтение аргументов
    args = parser.parse_args()

    modelPath = args.modelPath
    videoPath = args.videoPath

    # Выполнение основной логики
    output_dir = annotation.annotaion(modelPath, videoPath)
    frames_to_video.frames_to_video(output_dir, videoPath)

if __name__ == "__main__":
    main()
