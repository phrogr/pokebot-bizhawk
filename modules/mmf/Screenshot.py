import io
import logging
import mmap

import cv2
import numpy
from PIL import Image
from datetime import date

from modules.Config import GetConfig

log = logging.getLogger(__name__)
config = GetConfig()


def GetScreenshot():
    retry = 0
    while True:
        screenshot = None
        try:
            screenshot = Image.open(io.BytesIO(mmap.mmap(0, 24576, "bizhawk_screenshot-" + config["bot_instance_id"])))
            screenshot = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_BGR2RGB)
            return screenshot
        except Exception as e:
            log.debug("Failed to GetScreenshot(), trying again...")
            log.exception(str(e))
            if screenshot is not None:
                screenshot.close()
            if retry >= 5:
                return None
            retry += 1

def SaveShinyScreenshot(pokemon):
    screenshot = GetScreenshot()
    retry = 0
    while True:
        try:
            cv2.imwrite(f"logs/screenshots/{date.today()} {pokemon['name']}.png", screenshot)
            log.info(f"Saving screenshot...")
            return None
        except:
            log.info("Saving screenshot failed, trying again...")
            retry += 1
            if retry == 3:
                log.info("Failed to save screenshot")