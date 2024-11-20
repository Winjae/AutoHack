import can

def receive_can_messages(channel=0, bitrate=500000, filter_id=None):
    
    file_name = input("Input Log File Name >>> ")
    
    try:
        # 버스 설정
        bus = can.interface.Bus(bustype='kvaser', channel=channel, bitrate=bitrate)
        print(f"Kvaser CAN 버스 채널 {channel}에 연결되었습니다. 비트레이트: {bitrate}bps")
        
        # 필터 설정 (선택 사항)
        if filter_id is not None:
            bus.set_filters([{"can_id": filter_id, "can_mask": 0xFFFFFFFF}])
            print(f"필터링된 메시지 ID: 0x{filter_id:X}")
        
    except OSError as e:
        print(f"Kvaser CAN 버스에 연결할 수 없습니다: {e}")
        return
    
    try:
        write_data = ''
        
        print("메시지 수신 대기 중...")
        for msg in bus:
            if msg.is_error_frame:
                print(f"에러 프레임 수신: {msg}")
            else:
                can_data = ''
                print(f"수신된 메시지: ID=0x{msg.arbitration_id:X}, 데이터={msg.data}, 시간={msg.timestamp}")
                can_data += f'{msg.arbitration_id:03X} {len(msg.data)}'
                for i in range(len(msg.data)):
                    can_data += f' {msg.data[i]:02X}'
                can_data += '\n'
                #if can_data not in write_data:
                write_data += can_data
    except KeyboardInterrupt:
        with open(file_name, 'w') as f:
            f.write(write_data[:-1])
        print("\n수신 종료")
    finally:
        bus.shutdown()

if __name__ == "__main__":
    receive_can_messages()
