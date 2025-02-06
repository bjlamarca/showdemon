import wave
import matplotlib.pyplot as plt
import numpy as np



obj = wave.open('HauntedHouse.wav', 'rb')


print('Number of channels:', obj.getnchannels())
print('Sample width:', obj.getsampwidth())
sample_freq = obj.getframerate()
print('Frame rate:', obj.getframerate())
print('Number of frames:', obj.getnframes())
n_samples = obj.getnframes()
print('Parameters:', obj.getparams())

t_audio = obj.getnframes() / obj.getframerate()
print('Time:', t_audio, 's')

frames = obj.readframes(obj.getnframes())
print('Number of bytes:', len(frames))
print(type(frames), type(frames[0]))


signal_array = np.frombuffer(frames, dtype=np.int16)

times = np.linspace(0, t_audio, num=n_samples)

plt.figure(figsize=(15, 5))
plt.plot(times, signal_array)
plt.title('Audio signal')
plt.ylabel('Amplitude')
plt.xlabel('Time [s]')
plt.xlim = (0, t_audio)
plt.show()

obj.close()


# obj_new = wave.open('CantinaBand60_new.wav', 'wb')
# obj_new.setnchannels(2)
# obj_new.setsampwidth(2)
# obj_new.setframerate(16000)
# obj_new.writeframes(frames)
# obj_new.close()