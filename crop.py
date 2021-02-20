import os
from PIL import Image
from tqdm import tqdm
from logger import Logger


def read_annotacions(file_name):
    with open(file_name) as file_in:
        for _line in file_in:
            yield _line

def crop_faces(line, vggface_subdir_path, logger):
    if 'NAME_ID' not in line:
        img_path, x, y, w, h = line.strip("\n").replace("\"", "").split(",")
        x, y, w, h = int(x), int(y), int(w), int(h)
        full_img_path = os.path.join(vggface_subdir_path, img_path + ".jpg")
        if os.path.exists(full_img_path):
            try:
                img = Image.open(full_img_path)
                im = img.crop((x, y, x + w, y + h))
                im.save(full_img_path)
            except Exception as e:
                error_m = f"{full_img_path} : {repr(e)}"
                logger.error(msg=error_m)
        else:
            error_m = f"{full_img_path}"
            logger.error(msg=error_m)



if __name__ == "__main__":

    bb_path = "/home/adam/data/VGGFACE2/bb_landmark"
    bb_file = ("loose_bb_test.csv", "loose_bb_train.csv")
    vgg_path = "/home/adam/data/VGGFACE2"
    subdirectory = ("test", "train")

    errors = "vgg_errors.txt"
    logger = Logger()
    logger.log_file_path = os.path.join(os.getcwd(), errors)

    for item in zip(subdirectory, bb_file):
        subdir, loose_bb_file = item
        vggface_subdir_path = os.path.join(vgg_path, subdir)
        loose_bb_path = os.path.join(bb_path, loose_bb_file)
        if os.path.exists(loose_bb_path):
            for line in tqdm(read_annotacions(loose_bb_path)):
                crop_faces(line, vggface_subdir_path, logger)
        else:
            error_msg: str = f"File does not exist: {loose_bb_path} "
            logger.error(msg=error_msg)
