# Blender Drag and Drop NIF
A small addon for Blender that enables drag and drop import for NIF files when using the [PyNifly](https://github.com/BadDogSkyrim/PyNifly) addon. For Blender version 4.1.0 and above.

> [!IMPORTANT] 
> **To function, this addon requires that PyNifly is installed and enabled.**

## Installation
Download the `BlenderDragAndDropNIF.zip` file from the latest version on the [Releases](https://github.com/Sync-67/Blender-Drag-and-Drop-NIF/releases/latest) page.

In Blender, select `Edit > Preferences > Addons > Install`, navigate to and select the download .zip file, and press the Install Add-on button. Enable "**Drag & Drop NIF**" in the Import-Export category of the addons list.

## Usage
To quickly import a NIF file, drag and drop the file into the 3D Viewport.

PyNifly's default import settings will be used automatically if the option in Preferences is checked (enabled by default).
Disabling automatic import will result in the file import window appearing each time a NIF file is dropped into the 3D Viewport, allowing the import settings to be changed. The path for the file that was dropped will automatically be filled in the file import window.

## License
Files in this repository are licensed under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html).
