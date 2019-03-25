import numpy as np
from pitchogram import pitchogram_from_signal
from wave_signal import Signal
import cv2 as cv
import wave
ALLPITCH = ["C#/Db(1)","D(1)","D#/Eb(1)","E(1)","F(1)","F#/Gb(1)","G(1)","G#/Ab(1)","A(1)","A#/Bb(1)"
             ,"B(1)","C(2)","C#/Db(2)","D(2)","D#/Eb(2)","E(2)","F(2)","F#/Gb(2)","G(2)","G#/Ab(2)",
              "A(2)","A#/Bb(2)","B(2)","C(3)","C#/Db(3)","D(3)","D#/Eb(3)","E(3)","F(3)","F#/Gb(3)",
             "G(3)","G#/Ab(3)","A(3)","A#/Bb(3)","B(3)","C(4)","C#/Db(4)","D(4)","D#/Eb(4)","E(4)",
             "F(4)","F#/Gb(4)","G(4)","G#/Ab(4)","A(4)","A#/Bb(4)","B(4)","C(5)","C#/Db(5)","D(5)",
             "D#/Eb(5)","E(5)","F(5)","F#/Gb(5)","G(5)","G#/Ab(5)","A(5)","A#/Bb(5)","B(5)","C(6)",
             "C#/Db(6)","D(6)","D#/Eb(6)","E(6)","F(6)","F#/Gb(6)","G(6)","G#/Ab(6)","A(6)","A#/Bb(6)",
             "B(6)","C(7)","C#/Db(7)","D(7)","D#/Eb(7)","E(7)","F(7)"]
class Draw_pic():
    def __init__(self,url):
        self.url = url

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

    def energypic(self,):
        """获取wav能量信息，绘制图片"""
        active_notes, note_names, note_numbers, time_values = self.__get_activenotes()
        totallengh = len(time_values) * 8
        img = np.zeros((len(ALLPITCH) * 4, totallengh, 3), np.uint8)
        img[:,:,0] = 230
        img[:,:,1] = 245
        img[:,:,2] = 253
        maxenergy = 0
        minenergy = 99999999999999999
        for info in active_notes:
            if int(info["v"])>maxenergy:
                maxenergy = int(info["v"])
            if int(info["v"])<minenergy:
                minenergy = int(info["v"])
        for pitchpos in active_notes:
            colorradio = (int(pitchpos["v"])-minenergy)/(maxenergy-minenergy)
            # increasgreen = int((245-143)*(colorradio))
            if (colorradio+0.1)<1:
                cv.rectangle(img, (8 * (pitchpos["t"]), 4 * (len(ALLPITCH) - (pitchpos["n"]))),
                             (8 * (pitchpos["t"]+1), 4 * ((len(ALLPITCH) - (pitchpos["n"]))+1)),
                             (230,245*(1-(colorradio+0.1)),253), -1)
            else:
                cv.rectangle(img, (8 * (pitchpos["t"]), 4 * (len(ALLPITCH) - (pitchpos["n"]))),
                             (8 * (pitchpos["t"] + 1), 4 * ((len(ALLPITCH) - (pitchpos["n"])) + 1)),
                             (230, 245 * (1 - colorradio), 253), -1)
            cv.rectangle(img, (8 * (pitchpos["t"]), 4 * (len(ALLPITCH) - (pitchpos["n"]))),
                         (8 * (pitchpos["t"] + 1), 4 * ((len(ALLPITCH) - (pitchpos["n"])) + 1)),
                         (230, 245, 253), 1)
        # cv.imshow("image",img)


        return img,totallengh

if __name__ == '__main__':
    url = "/Users/jiating/Documents/pythoncode/wavepitch/1.wav"
    showpic = Draw_pic(url)
    showpic.energypic()
    cv.waitKey(0)
    cv.destroyAllWindows()

