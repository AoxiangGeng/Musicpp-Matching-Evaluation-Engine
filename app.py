import numpy as np
from pitchogram import pitchogram_from_signal
from wave_signal import Signal
import cv2 as cv
import wave
ALLPITCH = 96
class Draw_pic():
    def __init__(self,url,tempname):
        self.url = url
        self.tempname = tempname

    def __get_activenotes(self):
        """从wav文件读取能量信息"""
        f = wave.open(self.url, "rb")
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        str_data = f.readframes(nframes)
        f.close()
        wave_data = np.fromstring(str_data, dtype=np.int32)
        sig = Signal()
        sig.set_signal(wave_data, framerate)
        return pitchogram_from_signal(sig, filtered=True)

    def energypic(self,threshhold,shadenum):
        """获取wav能量信息，绘制图片"""
        active_notes, note_names, note_numbers, time_values = self.__get_activenotes()
        notesnum = len(active_notes)
        totallengh = len(time_values) * 20
        img = np.zeros((96 * 4, totallengh, 3), np.uint8)
        img[:,:,0] = 230
        img[:,:,1] = 245
        img[:,:,2] = 253
        active_notes.sort(key=lambda x: x['v'], reverse=True)
        threshholdnum = int(notesnum * threshhold)
        maxactive = active_notes[0]["v"]
        minactive = 0
        # colorradio_b = (230 - 0) / (maxactive-minactive)
        colorradio_g = (245 - 0) / (maxactive-minactive)
        colorradio_r = (253 - 0) / (maxactive-minactive)
        print(colorradio_r)
        adjustnum = [0.9e-16,1.9e-16,2.9e-16,0.9e-16,1.9e-15,2.9e-15,0.9e-14,1.9e-14,2.9e-14,0.9e-13]
        for i in range(threshholdnum):
            corlor_r = int(253 - (active_notes[i]["v"]-minactive)*(colorradio_r+adjustnum[shadenum]))
            corlor_g = int(245 - (active_notes[i]["v"]-minactive)*(colorradio_g+adjustnum[shadenum]))
            # corlor_b = int(230 - (active_notes[i]["v"]-minactive)*colorradio_b)
            cv.rectangle(img, (20 * (active_notes[i]["t"]), 4 * (96 - (active_notes[i]["n"]) - 1)),
                                 (20 * (active_notes[i]["t"] + 1)-2, 4 * ((96 - (active_notes[i]["n"])))),
                                 (230, corlor_g, corlor_r), -1)
#        cv.imshow("image",img)
#        cv.imwrite("./{}".format(self.tempname),img)
        return totallengh

if __name__ == '__main__':
    url = "/Users/jiating/Documents/pythoncode/wavepitch/tp_cut.wav"
    showpic = Draw_pic(url,"1.png")
    showpic.energypic(0.6,6)
    cv.waitKey(0)
    cv.destroyAllWindows()

