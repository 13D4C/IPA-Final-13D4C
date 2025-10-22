# test_ansible.py

print("--- [START] กำลังเริ่มทดสอบไฟล์ test_ansible.py ---")

try:
    # เราจะลอง import ฟังก์ชันเจ้าปัญหาโดยตรง
    from ansible_final import run_show_command

    print("--- [SUCCESS] Import 'run_show_command' สำเร็จ ---")

    # เรียกใช้ฟังก์ชันทันที
    print("--- [ACTION] กำลังเรียกใช้ run_show_command()... ---")
    result = run_show_command()
    print(f"--- [RESULT] ฟังก์ชันคืนค่ากลับมาเป็น: {result} ---")

except ImportError as e:
    print(f"--- [FATAL ERROR] ไม่สามารถ Import ได้: {e} ---")
    print("--- ตรวจสอบว่าไฟล์ ansible_final.py อยู่ในโฟลเดอร์เดียวกันหรือไม่ ---")
except Exception as e:
    print(f"--- [UNEXPECTED ERROR] เกิดข้อผิดพลาดระหว่างรัน: {e} ---")

print("--- [END] การทดสอบเสร็จสิ้น ---")