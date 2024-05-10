import os
import urllib
from datetime import datetime
import glob
import tomllib
import dotenv
from flask import Flask, request, render_template, redirect
from markupsafe import Markup
from openai import OpenAI
from PIL import Image
from handlers import logger

dotenv.load_dotenv()

client = OpenAI()
app = Flask(__name__)

@app.context_processor
def inject_stage_and_region() -> dict:
    """Generates the config for the application to run correctly.

    Returns:
        dict: The application configuration that has been parsed into a dictionary.
    """
    return {
        "APP_VERSION": os.environ.get("APP_VERSION", "undefined"),
    }

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

PROMPT_USER = config["prompt"]["user"]
PROMPT_CONSTRAINTS = config["prompt"]["constraints"]

def generate_image(prompt: str) -> str:
    """Access the OpenAI API and generate an image based on the parameters provided.

    Args:
        prompt (str): The description of the image to generate

    Returns:
        str: Image Response
    """
    logger.debug(f"Prompt User => '{PROMPT_USER}'")
    logger.debug(f"Prompt Constraints => '{PROMPT_CONSTRAINTS}'")
    response = client.images.generate(
        model="dall-e-3",
        user=PROMPT_USER,
        prompt=f"{prompt}, {PROMPT_CONSTRAINTS}",
        size=config["prompt"]["size"],
        quality=config["prompt"]["quality"],
        n=1,
    )
    logger.debug(f"Response => {response}")
    image_url = response.data[0].url
    return image_url


def download_image(image_url: str, filename: str) -> str:
    """Download the generated image and write to disk.

    Args:
        image_url (str): _description_
        filename (str): _description_

    Returns:
        str: The path to the newly written file
    """
    path = f"static/{filename}"

    logger.debug(f"Path => '{path}'")

    with urllib.request.urlopen(image_url) as img:
        with open(path, "wb") as f:
            f.write(img.read())
    return path


@app.route("/img/<image_id>/delete", methods=["POST"])
def delete_image(image_id) -> redirect:
    """Delete an existing image from disk

    Args:
        image_id (_type_): _description_

    Returns:
        redirect: _description_
    """
    images = glob.glob(f"static/*{image_id}.png")

    logger.debug(f"Images => {images}")

    for each in images:
        if os.path.isfile(each):
            os.remove(each)

    return redirect("/", code=302)


@app.route("/img/<image_id>", methods=["GET"])
def show_image(image_id) -> render_template:
    """Display a single image that's previously been generated

    Args:
        image_id (_type_): _description_

    Returns:
        render_template: _description_
    """
    return render_template("image.html", image_id=image_id)


def generate_thumbnail(filename: str, size=(96, 96)) -> None:
    """Generate thumbnails for the requested image file

    Args:
        filename (str): _description_
        size (tuple, optional): _description_. Defaults to (96, 96).
    """
    path = f"static/{filename}"
    img = Image.open(path)
    img.thumbnail(size)
    img.save(path.replace("image-", "thumb-"))


@app.route("/", methods=["GET", "POST"])
def index() -> render_template:
    """The root of the website

    Returns:
        render_template: _description_
    """

    previous_images = glob.glob("static/thumb-*.png")
    previous_images.sort()
    previous_images.reverse()
    logger.debug(f"Previous Images => {previous_images}")
    previous_images = [f.replace("static/", "") for f in previous_images]
    previous_images = previous_images[0:20]
    logger.debug(f"Previous Images, Stripped => {previous_images}")

    if request.method == "GET":
        return render_template("index.html", previous_images=previous_images)

    prompt = Markup.escape(request.form["prompt"])
    logger.debug(f"Prompt => {prompt}")
    filename_suffix = datetime.now().strftime("%s")
    filename = f"image-{filename_suffix}.png"
    logger.debug(f"Filename => {filename}")

    image_url = generate_image(prompt)
    logger.debug(f"Image URL => {image_url}")

    download_image(image_url=image_url, filename=filename)
    generate_thumbnail(filename=filename)

    return render_template(
        "index.html",
        filename=filename,
        prompt=prompt,
        previous_images=previous_images,
    )


if __name__ == "__main__":
    app.run()
