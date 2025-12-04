from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
from io import BytesIO

app = FastAPI()

# Configuración ULTRA CALIDAD (BiRefNet):
# BiRefNet (Bilateral Reference Network) es el estado del arte actual.
# Supera a ISNet e U2Net en precisión de bordes y alta resolución.
# Nota: Requiere una versión reciente de rembg. Descargará el modelo la primera vez.
my_session = new_session("birefnet-general")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    # Leemos la imagen original
    input_image = await file.read()
    
    # Configuración "PIXEL PERFECT":
    output_image = remove(
        input_image,
        session=my_session,
        alpha_matting=True,
        
        # Umbrales ajustados para BiRefNet
        # BiRefNet es muy confiable, así que podemos ser estrictos con lo que es fondo (10)
        # y lo que es primer plano (240).
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        
        # Un valor de 0 es ideal para "Raw", pero a veces deja 1px de halo sucio.
        # Usamos 1 con BiRefNet para una limpieza quirúrgica sin perder pelo.
        alpha_matting_erode_size=1,
        
        # Resolución masiva para el refinado de bordes
        alpha_matting_base_size=4096,
        
        # Desactivamos post-proceso para no perder detalles microscópicos
        post_process_mask=False
    )
    
    # Devolvemos la imagen directa como PNG
    return StreamingResponse(BytesIO(output_image), media_type="image/png")