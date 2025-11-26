import os
import uuid
from enum import Enum

import numpy
from PIL import Image
from telegram.ext import ApplicationBuilder


class WatermarkPosition(Enum):
    NOPE = 0
    LEFT_UP = 1
    LEFT_DOWN = 2
    RIGHT_UP = 3
    RIGHT_DOWN = 4


async def work(
        bot_token: str,
        chat_id: str,
        image_path: str,
        watermark_path: str,
        caption: str,
        w_pos: WatermarkPosition
):
    try:
        if len(image_path) > 0:
            if w_pos is not WatermarkPosition.NOPE and len(watermark_path) > 0:
                img_with_wm = __add_watermark(image_path, watermark_path, w_pos)
                print(f"Send image with wm: '%s'" % img_with_wm)
                return await __send_photo(bot_token, chat_id, img_with_wm, caption)
            else:
                print(f"Send image: '%s'" % image_path)
                return await __send_photo(bot_token, chat_id, image_path, caption)
        else:
            print(f"Send msg: '%s'" % caption)
            return await __send_msg(bot_token, chat_id, caption)
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(watermark_path):
            os.remove(watermark_path)
    return ""


async def __send_photo(bot_token: str, chat_id: str, image_path: str, caption: str):
    try:
        async with ApplicationBuilder().token(bot_token).build().bot as bot:
            await bot.send_photo(
                chat_id=chat_id,
                photo=image_path,
                caption=caption,
                parse_mode="MarkdownV2"
            )
        os.remove(image_path)
    except Exception as e:
        err = "Error, but need work. Img: %s Error: %s" % (image_path, e)
        print(err)
        if os.path.exists(image_path):
            os.remove(image_path)
        return err
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
    return None


async def __send_msg(bot_token: str, chat_id: str, caption: str):
    try:
        async with ApplicationBuilder().token(bot_token).build().bot as bot:
            await bot.send_message(chat_id=chat_id,
                                   text=caption,
                                   parse_mode="MarkdownV2")
    except Exception as e:
        err = "Cannot send msg: %s" % e
        print(err)
        return err
    return None


def __add_watermark(image_path: str, watermark_path: str, w_pos: WatermarkPosition):
    new_name = os.path.dirname(image_path) + "/" + str(uuid.uuid4()) + ".png"
    wm = Image.open(watermark_path)
    wm_x, wm_y = wm.size
    img = Image.open(image_path)
    img_x, img_y = img.size
    new_img = img.copy()

    if w_pos is WatermarkPosition.LEFT_UP:
        new_img.paste(wm, (0, 0), wm)
    if w_pos is WatermarkPosition.LEFT_DOWN:
        new_img.paste(wm, (0, img_y - wm_y), wm)
    if w_pos is WatermarkPosition.RIGHT_UP:
        new_img.paste(wm, (img_x - wm_x, 0), wm)
    if w_pos is WatermarkPosition.RIGHT_DOWN:
        new_img.paste(wm, (img_x - wm_x, img_y - wm_y), wm)

    save_array = numpy.asarray(new_img)
    Image.fromarray(save_array).save(new_name)
    return new_name
