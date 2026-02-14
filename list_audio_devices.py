
import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    print("\n--- Audio Devices Found ---\n")
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print(f"Input Device id {i} - {p.get_device_info_by_host_api_device_index(0, i).get('name')}")
            
    print("\n--- Output Devices Found ---\n")
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
            print(f"Output Device id {i} - {p.get_device_info_by_host_api_device_index(0, i).get('name')}")

    p.terminate()

if __name__ == "__main__":
    try:
        list_audio_devices()
    except Exception as e:
        print(f"Error listing devices: {e}")
