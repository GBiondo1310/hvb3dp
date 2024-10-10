# HVB3DP - High Volume Batch for 3D Printing

HVB3DP is here to help makers automate their 3D printing workflow, making batch printing simpler and more efficient.

## The Maker's Struggle

Printing large batches of small objects on a typical desktop 3D printer can be a hassle:

- **Limited space**: You can only fit a few pieces on the bed at once, meaning you'll need to keep checking in, removing finished prints, and starting new jobs.
- **Print failure**: If one piece in the batch fails, it often messes up the rest of the pieces too.
- **Slow speeds**: Filling up the print bed means longer travel moves between pieces, which not only takes more time but can cause stringing issues. And because you're afraid of ruining the entire batch, you might even slow down your print speeds.

## The HVB3DP Solution

Why not print one piece at a time? With HVB3DP, your printer can:

- **Focus on one object**: Print faster and avoid extra travel time between objects.
- **Auto-eject and restart**: Once a piece is done, the print head knocks it off the bed, and the next print starts automatically—no need to constantly check on it.

## A Few Things to Know

- **Work in progress**: HVB3DP is still under development, so it might have some bugs. Always double-check the generated G-code before starting a print.
- **Tested printers**: It has been tested on Creality Ender 3 (E3, E3V2, E3PRO), Longer LK4, and QIDI X-MAX printers. Even though it's worked fine for me, I recommend testing with a small print before going all-in on a big batch.
- **Use at your own risk**: While I haven’t had any issues, I can't guarantee that this tool won’t cause problems with your printer. Please be cautious, and I'm not responsible for any damage.

## Tips for Using HVB3DP

- **Compatible slicers**: Right now, HVB3DP works with Ultimaker Cura. Other slicer support is coming soon.
- **Turn off bed adhesion**: Make sure to remove any bed adhesion features, like skirts or brims, before generating your G-code.
- **Add a purge line**: Design a purge line at the base of your print to ensure the nozzle is ready to go for the next piece.
- **Optimize your object placement**: If possible, design or position your object to have minimal surface area on the build plate, making it easier for the printer to knock it off after printing.
- **Remove start & end gcodes**: Default start and end gcodes will cause issues when printing,
please remove them in your slicer's settings. HVB3DP will provide start and end gcodes.




# Install in editable mode:
```
pip install -e .
```

# Install from github:
```
pip install project_name@git+"https://github.com/GBiondo1310/hvb3dp.git"
```
