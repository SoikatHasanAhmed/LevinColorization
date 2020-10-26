import  os
import cv2
from utils.colorization import *

if __name__ == '__main__':
    file_count = 3
    for i in range(1,file_count+1):
        print('woring example {}'.format(i))
        in_path = './data/input{}.bmp'.format(i)
        hint_path = './data/hint{}.bmp'.format(i)
        input = cv2.cvtColor(cv2.imread(in_path),cv2.COLOR_BGR2RGB)
        hint= cv2.cvtColor(cv2.imread(hint_path),cv2.COLOR_BGR2RGB)
        output = colorize(input, hint)
        show_save(input,hint,output,'output{}'.format(i))



