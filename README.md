# Colouring Book

An AI-powered colouring book page generator, built using OpenAI DALL-E 3 and Python Flask and allows users to view, download, and delete images.

## Features

- Generate images using OpenAI's DALL-E model based on user-provided prompts.
- Download generated images.
- Display previously generated images.
- Delete images from the server.

## Requirements

- Python 3.x
- Flask
- OpenAI Python Client
- Pillow
- Python-dotenv

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/djw4/colouring-book.git
    cd colouring-book
    ```

1. Create a `.env` file in the root directory of the project and add your OpenAI API key, `TZ`:
    ```env
    OPENAI_API_KEY=<your_openai_api_key>
    TZ=Australia/Brisbane
    ```

    Optionally include a new value for `APP_PORT`:
    ```env
    APP_PORT=5050
    ```

2. Run the application using docker compose:
   ```bash
   docker compose up -d
   ```

3. Open your web browser and go to `http://127.0.0.1:5050` (update the port if required).


## Development Server

1. Install `pipenv`:
    ```bash
    pip install pipenv --user
    ```

1. Use pipenv to create a virtual env and install the required packages:
   ```bash
   pipenv install --dev
   ```

1. Run the development server, within pipenv
   ```bash
   pipenv run make dev
   ```

You can also use the `run-dev` Makefile target to build the container image first then run the development server from the new container directly:


## Build Image

1. Follow the steps for installing the development server.

1. Run `make build`.

### Endpoints

- **GET /**: Display the homepage with previously generated images.
- **POST /**: Generate a new image based on the user prompt.
- **GET /img/<image_id>**: Display a specific image.
- **POST /img/<image_id>/delete**: Delete a specific image.

## Functionality

### `generate_image(prompt: str) -> str`

Generates an image using the OpenAI API based on the provided prompt.

- **Parameters**:
  - `prompt` (str): The description of the image to generate.
- **Returns**:
  - `str`: The URL of the generated image.

### `download_image(image_url: str, filename: str) -> str`

Downloads the generated image and saves it to disk.

- **Parameters**:
  - `image_url` (str): The URL of the image to download.
  - `filename` (str): The name of the file to save the image as.
- **Returns**:
  - `str`: The path to the saved image file.

### `delete_image(image_id) -> redirect`

Deletes an image from the server.

- **Parameters**:
  - `image_id`: The ID of the image to delete.
- **Returns**:
  - `redirect`: Redirects to the homepage.

### `show_image(image_id) -> render_template`

Displays a specific image.

- **Parameters**:
  - `image_id`: The ID of the image to display.
- **Returns**:
  - `render_template`: Renders the image.html template.

### `generate_thumbnail(filename: str, size=(96, 96)) -> None`

Generates a thumbnail for a given image file.

- **Parameters**:
  - `filename` (str): The name of the image file.
  - `size` (tuple, optional): The size of the thumbnail. Defaults to (96, 96).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit a Pull Request for any enhancements or bug fixes.

## Contact

For questions or suggestions, please open an issue or contact the repository owner.

