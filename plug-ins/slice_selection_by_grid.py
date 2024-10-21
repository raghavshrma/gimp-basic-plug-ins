#!/usr/bin/env python

from gimpfu import *
import math

def slice_selection_by_grid(image, drawable):
    # Start an undo group, so the action can be undone
    pdb.gimp_image_undo_group_start(image)

    # Get the current layer (drawable) dimensions
    is_selection_empty = pdb.gimp_selection_is_empty(image)

    if (is_selection_empty):
        layer = drawable
    else:
        has_copied = pdb.gimp_edit_copy(drawable)
        if (not has_copied):
            pdb.gimp_message("No selection found!")
            return

        layer = pdb.gimp_edit_paste(drawable, True)

    width = layer.width
    height = layer.height

    # Get the grid settings from the image
    grid_width, grid_height = pdb.gimp_image_grid_get_spacing(image)

    group_layer = pdb.gimp_layer_group_new(image)
    pdb.gimp_item_set_name(group_layer, "Slices") # This name can be a variable
    pdb.gimp_image_insert_layer(image, group_layer, None, -1)
    pdb.gimp_image_raise_item_to_top(image, group_layer)

    rows = int(math.ceil(height / grid_height))
    cols = int(math.ceil(width / grid_width))

    for row in range(rows):
        for col in range(cols):
            x = col * grid_width
            y = row * grid_height

            new_layer = pdb.gimp_layer_new_from_drawable(layer, image)
            pdb.gimp_item_set_name(new_layer, "S_{}_{}".format(row, col))
            pdb.gimp_image_insert_layer(image, new_layer, group_layer, row * cols + col)

            # Crop the layer
            pdb.gimp_layer_resize(new_layer, grid_width, grid_height, -x, -y)

    if (not is_selection_empty):
        pdb.gimp_floating_sel_remove(layer)

    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_displays_flush()

register(
    "python_fu_slice_selection_by_grid",
    "Slice selection by grid",
    "Slice selection by grid. The grid is picked by the configured image grid.",
    "Raghav Sharma", "Raghav Sharma", "2024",
    "<Image>/Filters/Custom/Slice selection by grid",
    "*",
    [],
    [],
    slice_selection_by_grid,
)

main()