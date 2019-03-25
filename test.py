import matplotlib.pyplot as plt
import numpy as np
import wave

f = wave.open('sp_cut.wav','rb')
params = f.getparams()  
nchannels, sampwidth, framerate, nframes = params[:4]
#读取波形数据  
#读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）  
str_data  = f.readframes(nframes)  
f.close()
#将波形数据转换成数组
#需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组  
wave_data = np.fromstring(str_data,dtype = np.short)
#将wave_data数组改为2列，行数自动匹配。在修改shape的属性时，需使得数组的总长度不变。
#wave_data.shape = -1,2
##转置数据
#wave_data = wave_data.T
#通过取样点数和取样频率计算出每个取样的时间。
time=np.arange(0,nframes)/framerate



fig,ax2=plt.subplots(1,1)

#
#ax1.plot(time,f.readframes,'b',marker='o')
#ax1.set_title('Time information')
#ax1.set_xlabel('time')
#ax1.set_ylabel('amplitude')


ax2.specgram(wave_data,window=np.hamming(50),NFFT=50,noverlap=40,Fs=0.02,mode='psd')
ax2.set_title('Frequency information')
ax2.set_xlabel('frequency')
ax2.set_ylabel('energy')
ax2.set_xscale('log')
#ax2.set_ylim(20,1500)







plt.show()