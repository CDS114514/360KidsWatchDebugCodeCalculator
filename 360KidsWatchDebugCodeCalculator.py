from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import hashlib

def encrypt_aes_base64(key, iv, data):
    return base64.b64encode(AES.new(key.encode(), AES.MODE_CBC, iv.encode()).encrypt(pad(data.encode(), AES.block_size))).decode()

def md5_encode(param_string):
    return hashlib.md5(param_string.encode()).hexdigest()

def generate_key(str1, str2, hard_code):
    return md5_encode(''.join(sorted([str1, str2, md5_encode(hard_code)])))

def get_code(base_string, str1, str2, hard_code):
    encrypted_base64 = encrypt_aes_base64(generate_key(str1, str2, hard_code), "eip97324acpamzbv", base_string)
    length = max(len(encrypted_base64) // 6, 1)
    return ''.join(str(ord(encrypted_base64[i * length]) % 10) for i in range(6))

def main():
    print("欢迎使用360儿童手表调试模式密码计算器！")
    while True:
        try:
            choice = int(input("请选择手表是否被绑定（1: 是, 2: 否）: "))
            if choice not in [1, 2]:
                print("选项不存在")
                continue
            if choice == 1:
                device_key = input("请输入DeviceKey: ")
                device_id = input("请输入DeviceId: ")
                hard_code = input("请输入HardCode: ")
                str1, str2 = device_key, device_id
            else:
                imei = input("请输入IMEI: ")
                qr_code = input("请输入QRCode: ")
                hard_code = input("请输入HardCode: ")
                str1, str2 = imei, qr_code
            print("调试模式密码:", get_code("develop_mode_code", str1, str2, hard_code), "\n工厂模式密码:", get_code("factory_mode_code", str1, str2, hard_code))
            print("按下回车键退出程序...")
            input()
            break 
        except ValueError:
            print("输入错误，请输入数字。")

if __name__ == "__main__":
    main()