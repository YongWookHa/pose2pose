import argparse
import cv2
import glob
import os

def load_images(dir):
    def file_number(x):
        num = x.split('\\')[-1][:-4] # *-outputs.png
        return int(num)

    if not os.path.exists(dir):
        raise FileNotFoundError(dir)
    input_paths = sorted(glob.glob(os.path.join(dir, "*.png")), key=file_number)
    
    for path in input_paths:
        try:
            img = cv2.imread(path)
            yield img
        except TypeError:
            print("TypeError Occured during reading image from : ", path)
            raise

def convert_imgs_to_video(imgs):
    if iter(imgs) != iter(imgs):
        print("Parameter \'imgs\' should be a type of iterator")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    get_shape = True
    paused = False
    delay = {True: 0, False: 1}
    while 1:
        try:
            frame = next(imgs)
            if get_shape:
                height, width, channels = frame.shape
                video = cv2.VideoWriter(os.path.join(args.output_folder, 'Generated_video.avi'), fourcc, args.frame,(height, width))
                get_shape = False
            else:
                if (height, width, channels) != frame.shape:
                    print("The size of frame does not match to the first one")
                    raise
            video.write(frame)
            cv2.imshow('video', frame)
            key = cv2.waitKey(delay[paused])
            if key & 255 == ord('p'):
                paused = not paused
            if key & 255 == ord('q'):
                break
        except StopIteration:
            break
    video.release()
    cv2.destroyAllWindows()
    print("Video released!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-folder', dest='input_folder', type=str, help='Input image folder')
    parser.add_argument('--output-folder', dest='output_folder', type=str, help='Output image folder')
    parser.add_argument('--frame', dest='frame', type=float, help='Frame per sec')
    args = parser.parse_args()

    images = load_images(args.input_folder)
    convert_imgs_to_video(images)
