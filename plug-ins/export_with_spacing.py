#!/usr/bin/env python

from gimpfu import *

def export_with_spacing(image, drawable, spacing, export_path):
    if not export_path or export_path == 'None':
        path = pdb.gimp_image_get_filename(image)
        if not path.endswith('.xcf'):
            pdb.gimp_message("This is not an XCF file. Won't be exporting.")
            return

        export_path = path[:-4] + '_sp.png'

    pdb.gimp_message("Exporting spaced image to: {}".format(export_path))

    # Duplicate the image, merge layers, and export (rest of your export logic)
    duplicate_image = pdb.gimp_image_duplicate(image)
    merged_layer = pdb.gimp_image_merge_visible_layers(duplicate_image, CLIP_TO_IMAGE) # type: ignore

    # Slicing and spacing image
    g_hei, g_wid = pdb.gimp_image_grid_get_spacing(image)
    h = float(image.height)
    w = float(image.width)
    s = float(spacing)

    rows = int(math.ceil((h / g_hei) * (1 - s / g_hei)))
    cols = int(math.ceil((w / g_wid) * (1 - s / g_wid)))

    for row in range(rows):
        for col in range(cols):
            x = col * g_hei
            y = row * g_wid

            new_layer = pdb.gimp_layer_new_from_drawable(merged_layer, duplicate_image)
            pdb.gimp_item_set_name(new_layer, "S_{}_{}".format(row, col))
            pdb.gimp_image_insert_layer(duplicate_image, new_layer, None, row * cols + col)

            # Crop the layer
            pdb.gimp_layer_resize(new_layer, g_hei, g_wid, -x, -y)
            pdb.gimp_layer_translate(new_layer, spacing * col, spacing * row)

    pdb.gimp_image_remove_layer(duplicate_image, merged_layer)
    merged_layer = pdb.gimp_image_merge_visible_layers(duplicate_image, CLIP_TO_IMAGE) # type: ignore
    pdb.gimp_layer_resize_to_image_size(merged_layer)

    # Exporting the image
    pdb.gimp_file_save(duplicate_image, merged_layer, export_path, export_path)
    pdb.gimp_message("Exported spaced image to: {}".format(export_path))

    # Scale the image
    interpolation_original = pdb.gimp_context_get_interpolation()
    pdb.gimp_context_set_interpolation(INTERPOLATION_LINEAR) # type: ignore

    scale = float(spacing) # Keeping scale same as spacing for now
                           # else spacing won't work if less than scale of LQ Image
    scale_width = int(duplicate_image.width / scale)
    scale_height = int(duplicate_image.height / scale)
    pdb.gimp_image_scale(duplicate_image, scale_width, scale_height)
    pdb.gimp_context_set_interpolation(interpolation_original)

    # Exporting LQ Image
    export_path = export_path[:-4] + '_lq.png'
    pdb.gimp_file_save(duplicate_image, merged_layer, export_path, export_path)
    pdb.gimp_message("Exported LQ spaced image to: {}".format(export_path))

    # Cleanup
    pdb.gimp_image_delete(duplicate_image)
    pdb.gimp_displays_flush()

register(
    "python_fu_export_with_spacing",
    "Export with Spacing",
    "Export with Spacing",
    "Raghav Sharma", "Raghav Sharma", "2024",
    "<Image>/Filters/Custom/Export with Spacing",
    "*",
    [
        (PF_INT32, "spacing", "Spacing", 4),
        (PF_STRING, "export_path", "Export Path", "")
    ],
    [],
    export_with_spacing
)

main()