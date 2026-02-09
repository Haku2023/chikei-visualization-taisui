# Chikei Visualization Tool (Taisui)

A Python web application built with Plotly and Dash for visualizing and comparing geometry (chikei) data from CSV files. The application provides interactive 3D visualizations with various viewing options.

## Features

- **Single File Visualization**: Display 3D geometry data from a single CSV file
- **Two File Comparison**: Compare two different geometry datasets side-by-side
- **Interactive Controls**: 
  - Top view toggle
  - Coordinate display toggle
  - Layer selection
  - Color scheme selection
  - 2D/3D mode selection

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

---

# 地形可視化ツール（Taisui）

PlotlyとDashで構築されたPython Webアプリケーションで、CSVファイルから地形（chikei）データを可視化・比較します。さまざまな表示オプションを備えたインタラクティブな3D可視化を提供します。

## 機能

- **単一ファイル可視化**: 単一のCSVファイルから3D地形データを表示
- **2ファイル比較**: 2つの異なる地形データセットを並べて比較
- **インタラクティブコントロール**: 
  - 上面図の切り替え
  - 座標表示の切り替え
  - レイヤー選択
  - カラースキームの選択
  - ２D、3D表示の切り替え

## 必要な環境

- Python 3.x
- `requirements.txt`に記載されている必要なパッケージ

## インストール

1. リポジトリをクローンする:
```bash
git clone <repository-url>
cd chikei-visualization-taisui
```

2. 依存関係をインストールする:
```bash
pip install -r requirements.txt
```

## 使用方法

### アプリケーションの起動

アプリケーションを実行する:
```bash
python chikei-visualization-taisui.py
```

Webアプリが起動し、ブラウザでアクセス可能になります（通常は`http://127.0.0.1:8050`）。

### 単一ファイルの可視化

1. Webアプリで**Layer_One**を`5`に設定（第5層データの場合）
2. **Upload File One**をクリックし、CSVファイルを選択（例：`ori_dom_xy_tky7_5-cnv.csv`）
3. **Generate-csv**をクリックして可視化を生成

**注意**: トップビューと座標非表示機能（Nagao_advice）は、単一ファイル可視化でのみ利用可能です。

### 2ファイル比較

1. **Two Files**オプションを選択
2. それぞれのアップロードボタンを使用して2つのCSVファイルをアップロード
3. 各ファイルのレイヤー番号を選択
4. **Generate-csv**をクリックして比較可視化を生成

## 設定

異なる地形データレイヤーを可視化するには、コードの22行目にある`layermapping`辞書を変更してください。

## 既知の問題

- **CSVファイルのみ**: 現在、`.csv`ファイル形式のみが完全にサポートされています
- **XYZNFファイルのサポート**: `.xyznf`ファイルを使用すると予期しない四角形が生成される可能性があり、改善が必要です

## 貢献

貢献を歓迎します。issueやプルリクエストをお気軽に送信してください。

## ライセンス

by 白皓東(haku) 2023


