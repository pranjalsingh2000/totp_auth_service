import qrcode
import io
import base64

def generate_qr_code_base64(uri: str):
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()
