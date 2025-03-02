import serial
import requests
import time

# 配置串口
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# 云端服务器的URL
server_url = "http://your-cloud-server.com/api/upload-location"

def parse_gps_data(data):
    """解析GPS数据"""
    if data.startswith('$GPGGA'):
        parts = data.split(',')
        if parts[2]:  # 纬度
            latitude = float(parts[2][:2]) + float(parts[2][2:]) / 60
            if parts[3] == 'S':
                latitude = -latitude
        else:
            latitude = None

        if parts[4]:  # 经度
            longitude = float(parts[4][:3]) + float(parts[4][3:]) / 60
            if parts[5] == 'W':
                longitude = -longitude
        else:
            longitude = None

        return latitude, longitude
    return None, None

def upload_location(latitude, longitude):
    """上传位置数据到云端服务器"""
    payload = {
        'latitude': latitude,
        'longitude': longitude
    }
    try:
        response = requests.post(server_url, json=payload)
        print(f"上传成功: {response.status_code}")
    except Exception as e:
        print(f"上传失败: {e}")

def main():
    while True:
        line = ser.readline().decode('utf-8').strip()
        latitude, longitude = parse_gps_data(line)
        if latitude and longitude:
            print(f"纬度: {latitude}, 经度: {longitude}")
            upload_location(latitude, longitude)
        time.sleep(1)

if __name__ == "__main__":
    main()
