from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import main

app = FastAPI()


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are supported.")

    try:
        # Чтение изображения
        image = Image.open(io.BytesIO(await file.read()))

        # main.py ожидает путь к файлу, сохраняем изображение временно
        image.save("temp_image.png")

        # Вызов функции распознавания текста из main.py
        recognized_text = main.teseract_recognition("temp_image.png")

        # Удаление временного файла, если необходимо
        # os.remove("temp_image.png")

        return JSONResponse(content={"recognized_text": recognized_text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)