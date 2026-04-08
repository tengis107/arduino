import serial
import numpy as np
import cv2

# 1. Setup Serial
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
except:
    print("Error: check /dev/ttyUSB0 connection.")
    exit()

# 2. Window Setup (10x scaling for 61x13 matrix)
WIDTH, HEIGHT = 610, 130
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

def get_color(dist):
    """Maps 0-200cm to White -> Red -> Blue -> Black"""
    if dist <= 0 or dist > 200:
        return (0, 0, 0) # Black (Void)
    
    # 0 to 50cm: White to Red
    if dist <= 50:
        ratio = dist / 50
        # Decrease Blue and Green, keep Red high
        val = int(255 * (1 - ratio))
        return (val, val, 255) # BGR: White transitions to Red
    
    # 50 to 100cm: Red to Blue
    elif dist <= 100:
        ratio = (dist - 50) / 50
        # Red goes down, Blue goes up
        r = int(255 * (1 - ratio))
        b = int(255 * ratio)
        return (b, 0, r) 
    
    # 100 to 200cm: Blue to Black
    else:
        ratio = (dist - 100) / 100
        # Blue fades to nothing
        b = int(255 * (1 - ratio))
        return (b, 0, 0)

print("Starting Precision Radar... 0cm=White | 100cm=Blue | 200cm=Black")

try:
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        
        if "," in line:
            try:
                p, t, d = map(float, line.split(','))
                
                # Matrix Indices (0-180 step 3, 70-130 step 5)
                c_idx = int(p // 3)
                r_idx = int((t - 70) // 5)
                
                color = get_color(d)
                
                # Draw 10x10 colored rectangle
                x1, y1 = c_idx * 10, r_idx * 10
                cv2.rectangle(canvas, (x1, y1), (x1+10, y1+10), color, -1)
                
                cv2.imshow("Precision Depth Map", canvas)
                
            except (ValueError, IndexError):
                continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

ser.close()
cv2.destroyAllWindows()
