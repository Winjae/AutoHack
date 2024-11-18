import can
import time

def send_can_messages(log_data):
    try:
        bus = can.interface.Bus(
            channel=0,
            bustype='kvaser',
            bitrate=500000
        )
        print("CAN 버스에 성공적으로 연결되었습니다.")
    except Exception as e:
        print(f"CAN 버스 연결 실패: {e}")
        return

    low = 0
    high = len(log_data)
    try:
        while low < high - 1:
            print("==============================================")
            print("                     Menu                     ")
            print("==============================================")
            print(f"Log Data Index {low}:{high}")
            print("[1] Send Low Case")
            print("[2] Send High Case")
            print("[3] Select Low Case")
            print("[4] Select High Case")
            print("==============================================")
            case_NUM = input("Select case : ")
            
            if case_NUM == '1' or case_NUM == '2':
                if case_NUM == '1':
                    print(f"Send Low Case {low} ~ {((low + high) // 2)}")
                    a = low
                    b = (low + high) // 2
                else:
                    print(f"Send High Case {(low + high) // 2} ~ {high}")
                    a = (low + high) // 2
                    b = high
                for i in range(a, b):
                    can_id = log_data[i][0]
                    d = []
                    for j in range(log_data[i][1]):
                        d.append(log_data[i][2 + j])
            
                    msg = can.Message(
                        arbitration_id=can_id,
                        data=d, 
                        is_extended_id=False
                    )
                    try:
                        bus.send(msg)
                        #print(f"메시지를 전송했습니다: {msg}")
                    except can.CanError as e:
                        print(f"메시지 전송 실패: {e}")

                    time.sleep(0.001)
            elif case_NUM == '3' or case_NUM == '4':
                if case_NUM == '3':
                    low = low
                    high = (low + high) // 2
                else:
                    low = (low + high) // 2
                    high = high
        print(f"Your last Can data : {log_data[low][0]:03X}   [{log_data[low][1]:X}] ", end='')
        for i in range(log_data[low][1]):
            print(f'{log_data[low][2 + i]:02X}', end=' ')
        print()
            
                

    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    except Exception as e:
        print(f"수신 중 오류 발생: {e}")
    finally:
        bus.shutdown()
        

def parse_log():
    file_name = input("Input Log File Name >>> ")
    with open(file_name, 'r') as f:
        buf = f.read().split('\n')
    log_data = []
    for line in buf:
        tmp = line.split(' ')
        datas = []
        for num in tmp:
            datas.append(int(num, 16))
        log_data.append(datas)
        
    return log_data
        

if __name__ == "__main__":
    log_data = parse_log()
    send_can_messages(log_data)
