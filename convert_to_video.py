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
    video = cv2.VideoWriter(os.path.join(args.output_folder, 'Generated_video.avi'), fourcc, args.frame, args.frame_size)
    paused = False
    delay = {True: 0, False: 1}
    while 1:
        try:
            frame = next(imgs)
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
    def coord(s):
        try:
            h, w = map(int, s.split('x'))
            return (h, w)
        except:
            raise argparse.ArgumentTypeError("Coordinates must be x,y,z")
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-folder', dest='input_folder', type=str, help='Input image folder')
    parser.add_argument('--output-folder', dest='output_folder', type=str, help='Output image folder')
    parser.add_argument('--frame', dest='frame', type=float, help='Frame per sec')
    parser.add_argument('--frame-size', dest='frame_size', type=coord, help='Size of frame : HxW')
    args = parser.parse_args()

    print(args.frame, args.frame_size)

    images = load_images(args.input_folder)
    convert_imgs_to_video(images)
