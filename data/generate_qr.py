import qrcode
import os

os.makedirs("data/qr_codes", exist_ok=True)

college_id = "1"

qr = qrcode.make(college_id)

qr.save("data/qr_codes/student_1.png")

print("QR Code generated successfully!")
print("College ID:", college_id)
print("Saved: data/qr_codes/student_1.png")