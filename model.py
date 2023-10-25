import easyocr
import argparse


def processOcr(opt):
    reader = easyocr.Reader(['ch_sim','en'])
    result = reader.readtext(opt.pathImge)
    return result



if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--pathImge', type=str)

    opt = parser.parse_args()
    print(opt)

    print(processOcr(opt))