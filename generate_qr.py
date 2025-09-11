#!/usr/bin/env python3
"""
Generate QR code for the Course Topic Selection System
"""

try:
    import qrcode
    from PIL import Image
    
    # Your application URL
    url = "https://course-topic-selection-hsba5qkmq3nvpqbkpgaubc.streamlit.app/"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image
    img.save("course_selection_qr.png")
    print("✅ QR code generated successfully!")
    print(f"📱 QR code saved as: course_selection_qr.png")
    print(f"🔗 URL: {url}")
    print("\n📋 Instructions:")
    print("1. Open the QR code image")
    print("2. Scan with your phone camera or QR code app")
    print("3. Access the course selection system!")
    
except ImportError:
    print("❌ Missing required packages. Please install:")
    print("pip install qrcode[pil] Pillow")
except Exception as e:
    print(f"❌ Error generating QR code: {e}")
