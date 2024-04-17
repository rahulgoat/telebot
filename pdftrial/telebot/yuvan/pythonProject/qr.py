import qrcode

# Prompt the user to input the data
data = input("Enter the data to encode in the QR code: ")

# Create the QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=20,
    border=1
)

qr.add_data(data)
qr.make(fit=True)

# Generate the QR code image
img = qr.make_image(fill_color='black', back_color='white')

# Save the image
file_name = input("Enter the file name (including extension) to save the QR code image: ")
img.save(file_name)

print("QR code image saved successfully.")



