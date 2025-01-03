# Render my Blend
A Blender Python script to automate the 360° rendering of a 3d STL Model

## Overview

**Render my Blend** is a simple project designed to streamline the rendering process for 3D STL models. It utilizes a Windows batch file to execute Blender in background mode, passing a Python script that performs the following tasks:

1. Searches for STL files in a specified directory.
2. Loads each STL file into Blender.
3. Renders screenshots of the model from multiple angles.
4. Generates a 360° rotating video of the model.

This project is ideal for users who need automated rendering of 3D models without manually setting up Blender scenes.

## Features

- **Batch Processing**: Automatically processes all STL files in a given directory.
- **Screenshots**: Captures multiple rendered views of each model.
- **360° Video Rendering**: Creates a rotating video of the 3D model.
- **Background Execution**: Runs Blender in background mode to save system resources.

## Prerequisites

1. **Blender**: Ensure Blender is installed and added to the system's PATH.
   - [Download Blender](https://www.blender.org/download/)
2. **Python**: Included with Blender.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/render-my-blend.git
   ```

## Usage

1. Navigate to the project directory:
   ```bash
   cd render-my-blend
   ```
2. Place your STL files in the `source` input directory
3. Run the batch file:
  ```bat
  ./render.bat
  ```
4. The rendered screenshots and video will be saved in the `rendered` directory.

## Project Structure

```graphql
render-my-blend/
├── blender_script.py       # Blender Python script for automation
├── render.bat              # Windows batch file to execute Blender
├── source/                 # Directory to place STL files
├── rendered/               # Directory where rendered files will be saved
├── LICENSE                 # Project License file
└── README.md               # Project documentation
```

## TODO

1. create a configuration file to parameterize source and output directory, background image, rendered resolution, number of rendered frames and video length and fps
2. improve autopositioning of camera and background
3. parameterize lights power and color
4. translate all comments into English
5. clean and refactor code (sorry about that, it started as a test and immediately went into production without proper standardization, I will do it very soon)


## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

The project is licensed under GPL3 License. See the LICENSE for details.

## Acknowledgments

Special thanks to the Blender community for their robust API and resources.


Happy Rendering! 🎥✨
