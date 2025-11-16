import os

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

import telegram_worker
from telegram_worker import WatermarkPosition

app = FastAPI()

# Раздаем статические файлы
app.mount("/src", StaticFiles(directory="src"), name="src")

# Создаем папку для загрузок
os.makedirs("uploads", exist_ok=True)


# Главная страница
@app.get("/")
async def main():
    return FileResponse("src/index.html")


# Загрузка файлов
@app.post("/upload")
async def upload_files(
        file: UploadFile = File(...),
        bot_token: str = Form(""),
        chat_id: str = Form(""),
        header: str = Form(""),
        message: str = Form(""),
        watermark: UploadFile = File(...),
        watermark_position: int = Form("")
):
    image_path = ""
    watermark_path = ""
    err_msg = None
    try:
        print(watermark_position)

        image_path = await __save_file(file)
        watermark_path = await __save_file(watermark)

        print(image_path)
        print(watermark_path)

        caption = f"`" + header + "`\n\n" + message

        await telegram_worker.work(
            bot_token, chat_id, image_path, watermark_path, caption, WatermarkPosition(watermark_position)
        )

    except Exception as e:
        err_msg = str(e)
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(watermark_path):
            os.remove(watermark_path)
    if err_msg is None:
        return HTMLResponse(f"""
        <html>
            <body>
                <h1>Upload Complete</h1>
                <a href="/">Back to upload</a>
            </body>
        </html>
        """, status_code=200)
    else:
        return HTMLResponse(f"""
        <html>
            <body>
                <h1>Upload FAIL</h1>
                <p>{err_msg}</p>
                <a href="/">Back to upload</a>
            </body>
        </html>
        """, status_code=200)


async def __save_file(file: UploadFile):
    file_path = f"uploads/{file.filename}"
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    return os.path.abspath(file_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
