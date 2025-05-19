---
title: Scientific Plotting
description: ""
date: 2024-07-12T16:07:07+08:00
tags: 
  - "academic"
  - "code"
sidebar: false
---


## Some Principles

- Divided into schematic diagrams representing concepts and data charts representing results.
- Data Charts
	- Prioritize using position to represent quantity, followed by length and area.
	- Try to avoid pie charts (unless it's essential to show proportions).
	- Color is not the first choice (gray is very misleading; viridis is recommended).
	- Use three-line tables.
- Schematic Diagrams
	- Illustrations are better than engineering drawings or photographs.
- Image Formats
	- Bitmaps are safer.
		- jpg has good color support, suitable for photographs.
		- png has good shape support, suitable for schematic diagrams.
		- Journals generally require a resolution greater than 300 dpi.
	- Vector graphics have poor cross-platform support but are still the first choice for academic journals.
		- pdf is preferred.
		- svg fonts may have issues; eps is outdated.

## Aesthetic Issues

- Coordination of layout and color between frames, text, and lines.
- Text
	- Use Song Ti or Hei Ti for Chinese.
	- Use Arial or Times New Roman for English.
	- Try to keep the font and font size consistent for all images in an article.
		- Image font size should not be larger than the main text font size.
		- Text before images.
	- All fonts in a single image must be consistent.
		- Use color and bolding for emphasis.


## Technical Issues

### Displaying Chinese in Matplotlib

Generally, Matplotlib cannot display Chinese directly and requires font settings.
This can be easily solved using [Clarmy/mplfonts: Fonts manager for matplotlib (github.com)](https://github.com/Clarmy/mplfonts).

First, install and set it up in the command line:
```shell
# 1. Install
pip install mplfonts
# 2. Set up
mplfonts init
```

Then, you can use the specified Chinese font in your Python code:
```python
from mplfonts import use_font

use_font('Noto Serif CJK SC')

# Other plotting code	
```

- Noto Sans Mono CJK SC: Noto Monospace Sans-serif
- Noto Serif CJK SC: Noto Serif
- Noto Sans CJK SC: Noto Sans-serif
- Source Han Serif SC: Source Han Serif
- Source Han Mono SC: Source Han Monospace

### Matching Colors of Data Points and Fit Lines in Matplotlib

When plotting data with Matplotlib, it is often desirable for data points and their corresponding fit lines to use the same color for clarity and aesthetics.
Here's a concise and efficient method using Matplotlib's built-in features to achieve automatic color matching without hardcoding.

#### Example Code

```python
import random
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use('science')

# Generate data
x1 = range(10)
y1 = [x + random.randint(1, 2) for x in x1]
y1_fit = np.polyfit(x1, y1, 1)

x2 = range(-2, 8)
y2 = [x + random.randint(1, 5) for x in x2]
y2_fit = np.polyfit(x2, y2, 1)

# Plot data points
plt.plot(x1, y1, 'o', label='data 1')
plt.plot(x2, y2, 'o', label='data 2')

# Get colors of all lines in the current plot
colors = [line.get_color() for line in plt.gca().lines]

# Plot fit lines using the same colors
plt.plot(x1, np.polyval(y1_fit, x1), '--', color=colors[0], label='fit 1')
plt.plot(x2, np.polyval(y2_fit, x2), '--', color=colors[1], label='fit 2')

plt.legend()
plt.show()
```

#### Core Code Explanation

The key part of this code is how colors are obtained and used:

```python
# Get colors of all lines in the current plot 
colors = [line.get_color() for line in plt.gca().lines]
```

This line uses a list comprehension to extract the color of each line from the `lines` attribute of the current axes (`gca()` object).
Since `plt.plot` uses colors from the color cycle in order by default, this method ensures that the fit lines use the same colors as their corresponding data points.

### Using ProPlot to Control Multiple Subplots

ProPlot wraps Matplotlib.

Shared axis labels, spanning.

### Using SciencePlots to Control Plotting Style

Use templates from different journals.

### Using adjusttext to Control Text Overlap

Reference: [Examples — adjustText documentation](https://adjusttext.readthedocs.io/en/latest/Examples.html)
