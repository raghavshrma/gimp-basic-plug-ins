#!/usr/bin/env python

from gimpfu import *

def copy_selection_from_layer(image, drawable):
    # Start an undo group, so the action can be undone
    pdb.gimp_image_undo_group_start(image)

    # Get the current layer (drawable) dimensions
    if (pdb.gimp_selection_is_empty(image)):
        pdb.gimp_message("Nothing selected!")
        return

    pdb.gimp_edit_copy(drawable)
    floating_layer = pdb.gimp_edit_paste(drawable, False)
    pdb.gimp_image_raise_item_to_top(image, floating_layer)
    pdb.gimp_floating_sel_to_layer(floating_layer)

    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_displays_flush()

register(
    "python_fu_copy_selection_from_layer",
    "Copy Layer from Selection",
    "Copy Layer from Selection",
    "Raghav Sharma", "Raghav Sharma", "2024",
    "<Image>/Filters/Custom/Copy Layer from Selection",
    "*",
    [],
    [],
    copy_selection_from_layer,
)

main()