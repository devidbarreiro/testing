from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from io import BytesIO
from PIL import Image

app = FastAPI(title="Remove Background API Local")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    # Leer la imagen subida
    input_bytes = await file.read()
    
    # Remover el fondo
    output_bytes = remove(input_bytes)
    
    # Convertir a imagen PNG para enviar como respuesta
    output_image = Image.open(BytesIO(output_bytes))
    buf = BytesIO()
    output_image.save(buf, format="PNG")
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/png")
