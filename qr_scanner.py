import cv2
from pyzbar.pyzbar import decode
import numpy as np
from tkinter import Tk, filedialog, Button, Canvas
from PIL import Image, ImageTk

def select_image():
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    root.destroy()  # Close the Tkinter window after file selection
    return file_path

def scan_qr_codes(image_path, canvas):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Decode QR codes
    qr_codes = decode(gray)

    # Print information about each QR code
    for qr_code in qr_codes:
        data = qr_code.data.decode('utf-8')
        print(f"QR Code Data: {data}")

        # Draw a rectangle around the QR code
        points = qr_code.polygon
        if len(points) == 4:
            pts = np.array([(pt.x, pt.y) for pt in points], dtype=np.int32)
            cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            # Calculate the center of the QR code
            center = (int((pts[0][0] + pts[2][0]) / 2), int((pts[0][1] + pts[2][1]) / 2))

            # Display information at the center of the QR code with red color and bold
            text_position = (center[0] - 50, center[1])  # Adjust the position as needed
            cv2.putText(image, data, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # Adjust thickness to 2 for bold

    # Convert the OpenCV image to PIL format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)

    # Convert PIL image to PhotoImage
    img = ImageTk.PhotoImage(pil_image)

    # Configure the canvas size based on the image size
    canvas.config(width=pil_image.width, height=pil_image.height)

    # Display the image on the canvas
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.image = img

if __name__ == "__main__":
    root = Tk()
    root.title("QR Code Scanner")

    canvas = Canvas(root)
    canvas.pack()

    def upload_action(event=None):
        image_path = select_image()
        if image_path:
            scan_qr_codes(image_path, canvas)

    upload_button = Button(root, text="Upload Image", command=upload_action)
    upload_button.pack(pady=10)

    root.mainloop()
