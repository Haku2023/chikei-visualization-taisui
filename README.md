# Chikei Visualization Tool (Taisui)

A Python web application built with Plotly and Dash for visualizing and comparing geometry (chikei) data from CSV files. The application provides interactive 3D visualizations with various viewing options.

## Features

- **Single File Visualization**: Display 3D geometry data from a single CSV file
- **Two File Comparison**: Compare two different geometry datasets side-by-side
- **Interactive Controls**: 
  - Top view toggle
  - Coordinate display toggle
  - Layer selection
  - Change height ratio
  - Color scheme selection
  - 2D/3D mode selection

## Requirements

- Python 3.13 works fine
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

### Single File Visualization(test for layer 5)

#### using csv file
1. In the web app, set **Layer_One** to `5` (for 5th layer data) 
> this will get the Layer 5 info and fill it in the xmax,xmin,ymax,ymin,dx,dy blank
> if not choosing layer, the default max,min,d value will be chosen
2. Click **Upload File One** and select your CSV file (e.g., `ori_dom_xy_tky7_5-cnv.csv`)
> this files contains only height of the geometry,if shape is (212,252),which means 
> 212 rows -> Y values; 252 columns -> X values;
3. Click **Generate-csv** to create the visualization
#### using xyznf file
1. Choose **using .xyznf files**, notice it should be 2D files in H-Fresh
2. Upload **xyzn-file**,**f-file**,**water-file**
3. Click **Generate-csv** to create the visualization


**Note**: The Top View and Hide Coordinates features (Nagao_advice) are only available for single file visualization.

### Two File Comparison

1. Select the **Two Files** option
2. Upload two CSV files or using xyzn file using the respective upload buttons
3. Select the layer number for each file
4. Click **Generate-csv** to generate the comparison visualization

## Configuration

To visualize different chikei data layers, there are several ways:
- use default value of xmax,xmin,etc which means only upload csv file 
- fill the xmin,xmax,etc blank manually
- modify the `layermapping` dictionary in the code at line 22. so that you can set xmax,xmin,ymax,ymin,dx,dy by choosing layer you have set


## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

by baihaodong(haku) 2023-2026

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
  - 高さ比率の変更
  - カラースキームの選択
  - ２D、3D表示の切り替え

## 必要な環境

- Python 3.13で正常に動作
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

### 単一ファイルの可視化（レイヤー5のテスト）

#### CSVファイルを使用する場合
1. Webアプリで**Layer_One**を`5`に設定（第5層データの場合）
> これによりレイヤー5の情報を取得し、xmax、xmin、ymax、ymin、dx、dyの空欄に値が入力されます
> レイヤーを選択しない場合は、デフォルトのmax、min、d値が選択されます
2. **Upload File One**をクリックし、CSVファイルを選択（例：`ori_dom_xy_tky7_5-cnv.csv`）
> このファイルには地形の高さ情報のみが含まれています。形状が(212,252)の場合、
> 212行 -> Y値、252列 -> X値を意味します
3. **Generate-csv**をクリックして可視化を生成

#### .xyznfファイルを使用する場合
1. **using .xyznf files**を選択してください。H-Freshの2Dファイルである必要があります
2. **xyzn-file**、**f-file**、**water-file**をアップロード
3. **Generate-csv**をクリックして可視化を生成

**注意**: トップビューと座標非表示機能（Nagao_advice）は、単一ファイル可視化でのみ利用可能です。

### 2ファイル比較

1. **Two Files**オプションを選択
2. それぞれのアップロードボタンを使用して2つのCSVファイルまたはxyznファイルをアップロード
3. 各ファイルのレイヤー番号を選択
4. **Generate-csv**をクリックして比較可視化を生成

## 設定

異なる地形データレイヤーを可視化するには、いくつかの方法があります：
- xmax、xminなどのデフォルト値を使用する（CSVファイルのみアップロード）
- xmin、xmaxなどの空欄に手動で値を入力する
- コードの22行目にある`layermapping`辞書を変更する。これにより、設定したレイヤーを選択することで、xmax、xmin、ymax、ymin、dx、dyを設定できます

## 貢献

貢献を歓迎します。issueやプルリクエストをお気軽に送信してください。

## ライセンス

by 白皓東(haku) 2023-2026






