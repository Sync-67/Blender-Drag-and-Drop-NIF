bl_info = {
    "name" : "Drag & Drop NIF",
    "description": "Support for drag & drop import of NIF files.",
    "author" : "Sync-67",
    "version": (1, 0, 0),
    "blender" : (4, 1, 0),
    "doc_url": "https://github.com/Sync-67/Blender-Drag-and-Drop-NIF",
    "support": "COMMUNITY",
    "category": "Import-Export"
}


import bpy
import addon_utils
import textwrap


# Addon Preferences Menu:
class DDNIF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    auto_import: bpy.props.BoolProperty(
        name="Automatic Import",
        default=True,
        description="Whether or not the import options will be shown when a NIF file is dropped into the 3D view"
    )

    def draw(self, context):
        pynifly_check = addon_utils.check("io_scene_nifly")
        layout = self.layout

        # Auto import option
        if (pynifly_check == (False, True)) or (pynifly_check == (True, True)):
            row = layout.row()
            row.separator(factor=0.5)
            row.prop(self, "auto_import", text="Automatically Import with Default Settings When a File is Dropped")
            layout.separator(factor=0.1)


        # Error message if PyNifly can't be found:
        else:
            # Text wrapping for message:
            long_text = "PyNifly is either not installed or not enabled in the Blender Preferences Add–ons list. This addon is dependent on PyNifly to function. The latest version of PyNifly can be found here:"

            # Get the Preferences area
            for area in bpy.context.screen.areas:
                if area.type == 'PREFERENCES':
                    break
            # Calculate the width of the panel
            for region in area.regions:
                if region.type == 'WINDOW':
                    panel_width = (region.width - 30)
                    break

            # Calculate the maximum width of the label
            uifontscale = 6 * context.preferences.system.ui_scale
            max_width = int(panel_width // uifontscale)

            # Wrap text and put lines in a list
            wrapping = textwrap.TextWrapper(width=max_width)
            wrap_list = wrapping.wrap(text=long_text)

            # Static heading label
            layout.label(text="ERROR: Missing Dependency", icon= 'ERROR')

            # Dynamically wrapped text
            for text in wrap_list:
                row = layout.row(align=True)
                row.scale_y = 0.4
                row.label(text=text, icon='BLANK1')

            layout.separator(factor=0.2)

            grid = layout.grid_flow(columns=3)
            grid.separator(factor=5)

            # Button
            grid.operator(
                "wm.url_open",
                text=" Latest PyNifly Release ",
                icon='URL'
            ).url = "https://github.com/BadDogSkyrim/PyNifly/releases/latest"

            grid.separator(factor=5)

            layout.separator(factor=0.2)


# Drag and Drop:
class DDNIF_drag_and_drop_nif(bpy.types.FileHandler):
    bl_idname = "WM_FH_drag_and_drop_nif"
    bl_label = "Import NIF"
    bl_import_operator = "wm.ddnif_import_nif"
    bl_file_extensions = ".nif"

    @classmethod
    def poll_drop(cls, context):
        if context.space_data.type == "VIEW_3D":
            return True


# Import file with PyNifly
class DDNIF_import_nif(bpy.types.Operator):
    bl_idname = "wm.ddnif_import_nif"
    bl_label = "Import NIF"
    bl_options = {'INTERNAL'}

    # Filepath for the dropped file
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Check if PyNifly is installed and enabled
        # 'check' function returns a tuple of booleans --> (loaded_default, loaded_state)
        # loaded_default = True when the addon is enabled by default in startup file
        # loaded_state = True when the addon is currently enabled
        pynifly_check = addon_utils.check("io_scene_nifly")

        if (pynifly_check == (False, True)) or (pynifly_check == (True, True)):
            # Check if default settings are automatically used for import
            if bpy.context.preferences.addons[__package__].preferences.auto_import:
                print(
                    "\nINFO: Drag and Drop NIF:\
                    \n    pyNifly Detected!\
                    \n    Auto import is enabled.\
                    \n    Now importing with default settings...\
                    \n\
                    \n====================================\
                    \n"
                )
                # Call PyNifly operator with defaults
                bpy.ops.import_scene.pynifly("EXEC_DEFAULT", filepath=self.filepath)
            else:
                print(
                    "\nINFO: Drag and Drop NIF:\
                    \n    pyNifly Detected!\
                    \n    Auto import is disabled.\
                    \n    Showing import menu...\
                    \n\
                    \n====================================\
                    \n"
                )
                # Call PyNifly operator and show its screen
                bpy.ops.import_scene.pynifly("INVOKE_DEFAULT", filepath=self.filepath)

        # Can't find PyNifly, so alert user and abort
        else:
            print(
                "\nERROR: Drag and Drop NIF:\
                \n    PyNifly is either not installed or not enabled in the Blender Preferences Add-ons list.\
                \n    The latest version of PyNifly can be found here:\
                \n    https://github.com/BadDogSkyrim/PyNifly/releases/latest\
                \n"
            )
            self.report({'ERROR'}, "Drag & Drop NIF: \nPyNifly is either not installed or not enabled!")
            return {'CANCELLED'}

        return {'FINISHED'}


# ######################################
#             REGISTRATION             #
# ######################################


def register():
    bpy.utils.register_class(DDNIF_addon_prefs)
    bpy.utils.register_class(DDNIF_drag_and_drop_nif)
    bpy.utils.register_class(DDNIF_import_nif)

def unregister():
    bpy.utils.unregister_class(DDNIF_addon_prefs)
    bpy.utils.unregister_class(DDNIF_drag_and_drop_nif)
    bpy.utils.unregister_class(DDNIF_import_nif)


# ######################################
#             GPL-3.0 License          #
# ######################################
#    
#    Copyright (C) <2024>  <Sync-67>
#    <https://github.com/Sync-67>
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#    
# ######################################
