# Chikei Visualization Tool (Taisui)

A Python web application built with Plotly and Dash for visualizing and comparing geometry (chikei) data from CSV files. The application provides interactive 3D visualizations with various viewing options.

## Features

- **Single File Visualization**: Display 3D geometry data from a single CSV file
- **Two File Comparison**: Compare two different geometry datasets side-by-side
- **Interactive Controls**: 
  - Top view toggle
  - Coordinate display toggle
  - Layer selection
- **CSV Export**: Generate visualization data as CSV files

## Requirements

- Python 3.x
- Required packages listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chikei-visualization-taisui
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

Run the application:
```bash
python chikei-visualization-taisui.py
```

The web app will start and be accessible in your browser (typically at `http://127.0.0.1:8050`).

### Single File Visualization

1. In the web app, set **Layer_One** to `5` (for 5th layer data)
2. Click **Upload File One** and select your CSV file (e.g., `ori_dom_xy_tky7_5-cnv.csv`)
3. Click **Generate-csv** to create the visualization

**Note**: The Top View and Hide Coordinates features (Nagao_advice) are only available for single file visualization.

### Two File Comparison

1. Select the **Two Files** option
2. Upload two CSV files using the respective upload buttons
3. Select the layer number for each file
4. Click **Generate-csv** to generate the comparison visualization

## Configuration

To visualize different chikei data layers, modify the `layermapping` dictionary in the code at line 22.

## Known Issues

- **CSV files only**: Currently, only `.csv` file format is fully supported
- **XYZNF file support**: Using `.xyznf` files may generate unexpected square shapes and needs refinement

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

by baihaodong(haku) 2023

