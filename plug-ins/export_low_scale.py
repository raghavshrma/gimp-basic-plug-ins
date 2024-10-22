#!/usr/bin/env python

from gimpfu import *

def export_low_scale(image, drawable, scale, export_path):
    scale_mult = 1.0 / scale

    if not export_path or export_path == 'None':
        path = pdb.gimp_image_get_filename(image)
        if not path.endswith('.xcf'):
            pdb.gimp_message("This is not an XCF file. Won't be exporting.")
            return

        export_path = path[:-4] + '_lq.png'

    pdb.gimp_message("Exporting low-scale image to: {}".format(export_path))

    # Duplicate the image, merge layers, and export (rest of your export logic)
    duplicate_image = pdb.gimp_image_duplicate(image)
    merged_layer = pdb.gimp_image_merge_visible_layers(duplicate_image, CLIP_TO_IMAGE) # type: ignore

    # Scale the image
    interpolation_original = pdb.gimp_context_get_interpolation()
    pdb.gimp_context_set_interpolation(INTERPOLATION_LINEAR) # type: ignore

    scale_width = int(duplicate_image.width * scale_mult)
    scale_height = int(duplicate_image.height * scale_mult)
    pdb.gimp_image_scale(duplicate_image, scale_width, scale_height)
    pdb.gimp_context_set_interpolation(interpolation_original)

    # Exporting the image
    pdb.gimp_file_save(duplicate_image, merged_layer, export_path, export_path)
    pdb.gimp_image_delete(duplicate_image)
    pdb.gimp_message("Exported low-scale image to: {}".format(export_path))

    pdb.gimp_displays_flush()

register(
    "python_fu_export_low_scale",
    "Export Low Scaled Image",
    "Export Low Scaled Image",
    "Raghav Sharma", "Raghav Sharma", "2024",
    "<Image>/Filters/Custom/Export Low Scaled Image",
    "*",
    [
        (PF_INT32, "scale", "Scale Down", 4),
        (PF_STRING, "export_path", "Export Path", "")
    ],
    [],
    export_low_scale
)

main()