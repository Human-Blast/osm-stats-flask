import io
import base64
from PIL import Image
from io import BytesIO

class ImageProcess:
    def __init__(self,fig):
        self.fig = fig

    def fig2img(self):
        """Convert a Matplotlib figure to a PIL Image and return it"""
        buf = io.BytesIO()
        self.fig.savefig(buf)
        buf.seek(0)
        return Image.open(buf)  

    def ImageToBase64(self):
        img = self.fig2img()
                
        output_buffer = BytesIO()
        img.save(output_buffer, format='png')
        binary_data = output_buffer.getvalue()
        base64_data = base64.b64encode(binary_data)

        return base64_data.decode('utf-8')

    