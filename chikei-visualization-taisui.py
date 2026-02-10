## the graph is in div which using flex property, so in children we use vh for height and % for width.
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import base64
import io
from dash.exceptions import PreventUpdate
import plotly.express as px
import struct
import json

# Get a list of all available color scales
colorscales = px.colors.named_colorscales()
layers = ["1", "2", "3", "4", "5", "7"]
advices = ["Top View", "Hide Coordinates", "Change Colorbar Variation"]
# xmin, xmax, ymin, ymax
layermapping = {
    "1": (-98618, 45832, 75290, 219740, 270, 270),
    "2": (-87008, 35842, 86090, 209750, 90, 90),
    "3": (-45698, -33998, 104720, 129920, 30, 30),
    "4": (-41918, -36638, 115250, 119330, 10, 10),
    "5": (-39808, -38548, 116810, 117870, 5, 5),
    "7": (-74719, -74619, -205709, -205539, 1, 1),
}
Zmax = 5  # min is 0.1 , step is 0.1
Zmax2 = 50  # min is 0.1 , step is 0.1
# Initialize the Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
)

server = app.server


styleForValueMaxMinUp = {
    "marginBottom": "4px",
    "width": "50px",
    "margin-right": "8px",
    "display": "inline-block",
}
styleForLabelMaxMinUp = {
    "marginBottom": "4px",
    "display": "inline-block",
    "margin-right": "2px",
}
styleForValueMaxMinDown = {
    "marginTop": "0px",
    "width": "50px",
    "margin-right": "8px",
    "display": "inline-block",
}
styleForLabelMaxMinDown = {
    "marginTop": "0px",
    "display": "inline-block",
    "margin-right": "2px",
}
styleForoutputMessageUp = {
    "marginLeft": "150px",
    "marginBottom": "4px",
    "width": "700px",
    "display": "inline-block",
}
styleForoutputMessageDown = {
    "marginLeft": "150px",
    "marginTop": "0",
    "width": "700px",
    "display": "inline-block",
}
# Define layout
app.layout = html.Div(
    [
        dcc.Store(id="trace-data"),
        dcc.Store(id="trace-data2"),
        html.H1(
            "Visualization From Chikei Data - 2DH & 3D  - Version3",
            style={"margin": "0%"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Shape change for all height:"),
                        dcc.Slider(
                            id="height-slider",
                            min=0.1,
                            max=Zmax,
                            step=0.1,
                            value=1,
                            tooltip={"always_visible": False, "placement": "bottom"},
                            marks=None,
                        ),
                    ],
                    style={"width": "30%", "margin": "0%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.H3("Shape change for water height:"),
                        dcc.Slider(
                            id="water-slider",
                            min=0.1,
                            max=Zmax2,
                            step=0.1,
                            value=1,
                            tooltip={"always_visible": False, "placement": "bottom"},
                            marks=None,
                        ),
                    ],
                    style={"width": "30%", "margin": "0%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.H3("Colormap:"),
                        dcc.Dropdown(
                            id="colormap-dropdown",
                            options=colorscales,
                            value="viridis",
                            style={"margin": "0%"},
                        ),  # value = 'plasma',
                    ],
                    style={"width": "40%", "margin": "0%", "display": "inline-block"},
                ),
            ]
        ),
        html.Div(
            [
                html.H3(
                    "Please choose the upload file format: ",
                    style={"margin-top": "0px"},
                ),
                dcc.RadioItems(
                    id="file-format-chooser",
                    options=[
                        {"label": "Using .csv file", "value": ".csv"},
                        {"label": "Using .xyznf files", "value": ".xyznf"},
                    ],
                    value=".csv",
                    labelStyle={
                        "display": "block",
                        "background-color": "#CCCCFF",
                        "border": "1px solid #636EFA",
                        "margin-bottom": "2px",
                    },
                    style={"margin-top": "0px", "margin-left": "5px"},
                ),
                html.P(
                    "Trim Height= ", style={"margin-top": "0px", "margin-left": "10px"}
                ),
                dcc.Input(
                    id="Trim Height",
                    type="text",
                    value=None,
                    style={
                        "margin-top": "0px",
                        "margin-left": "10px",
                        "font-size": "20px",
                        "width": "60px",
                        "text-align": "center",
                    },
                ),
                html.P(
                    "Colorbar Max:", style={"margin-top": "0px", "margin-left": "10px"}
                ),
                dcc.Input(
                    id="Colorbar Max",
                    type="text",
                    value=None,
                    style={
                        "margin-top": "0px",
                        "margin-left": "10px",
                        "font-size": "20px",
                        "width": "60px",
                        "text-align": "center",
                    },
                ),
                html.P(
                    "Colorbar Min:", style={"margin-top": "0px", "margin-left": "10px"}
                ),
                dcc.Input(
                    id="Colorbar Min",
                    type="text",
                    value=None,
                    style={
                        "margin-top": "0px",
                        "margin-left": "10px",
                        "font-size": "20px",
                        "width": "60px",
                        "text-align": "center",
                    },
                ),
            ],
            style={"display": "flex", "flexDirection": "row"},
        ),
        html.Div(
            [
                dcc.RadioItems(
                    id="file-chooser",
                    options=[
                        {"label": "One File", "value": "one"},
                        {"label": "Two Files", "value": "two"},
                    ],
                    value="one",
                    labelStyle={"display": "block"},
                    style={
                        "margin-bottom": "5px",
                        "margin-top": "10px",
                        "paddingTop": "5px",
                        "display": "block",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    dcc.Upload(
                                        id="upload-data-one",
                                        children=html.Button("Upload File One"),
                                        multiple=False,
                                    ),
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "10px",
                                    },
                                ),
                                html.P("Xmax1= ", style=styleForLabelMaxMinUp),
                                dcc.Input(
                                    id="input-Xmax1",
                                    type="text",
                                    style=styleForValueMaxMinUp,
                                ),
                                html.P("Xmin1= ", style=styleForLabelMaxMinUp),
                                dcc.Input(
                                    id="input-Xmin1",
                                    type="text",
                                    style=styleForValueMaxMinUp,
                                ),
                                html.P("Ymax1= ", style=styleForLabelMaxMinUp),
                                dcc.Input(
                                    id="input-Ymax1",
                                    type="text",
                                    style=styleForValueMaxMinUp,
                                ),
                                html.P("Ymin1= ", style=styleForLabelMaxMinUp),
                                dcc.Input(
                                    id="input-Ymin1",
                                    type="text",
                                    style=styleForValueMaxMinUp,
                                ),
                                html.P("dx= ", style=styleForLabelMaxMinUp),
                                dcc.Input(
                                    id="input-dx",
                                    type="text",
                                    style=styleForValueMaxMinUp,
                                ),
                                html.P("dy= ", style=styleForLabelMaxMinUp),
                                dcc.Input(
                                    id="input-dy",
                                    type="text",
                                    style=styleForValueMaxMinUp,
                                ),
                            ],
                            id="Block-up",
                            style={"display": "block"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    dcc.Upload(
                                        id="upload-data-two",
                                        children=html.Button("Upload File Two"),
                                        multiple=False,
                                    ),
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "10px",
                                    },
                                ),
                                html.P("Xmax2= ", style=styleForLabelMaxMinDown),
                                dcc.Input(
                                    id="input-Xmax2",
                                    type="text",
                                    style=styleForValueMaxMinDown,
                                ),
                                html.P("Xmin2= ", style=styleForLabelMaxMinDown),
                                dcc.Input(
                                    id="input-Xmin2",
                                    type="text",
                                    style=styleForValueMaxMinDown,
                                ),
                                html.P("Ymax2= ", style=styleForLabelMaxMinDown),
                                dcc.Input(
                                    id="input-Ymax2",
                                    type="text",
                                    style=styleForValueMaxMinDown,
                                ),
                                html.P("Ymin2= ", style=styleForLabelMaxMinDown),
                                dcc.Input(
                                    id="input-Ymin2",
                                    type="text",
                                    style=styleForValueMaxMinDown,
                                ),
                                html.P("dx= ", style=styleForLabelMaxMinDown),
                                dcc.Input(
                                    id="input-dx2",
                                    type="text",
                                    style=styleForValueMaxMinDown,
                                ),
                                html.P("dy= ", style=styleForLabelMaxMinDown),
                                dcc.Input(
                                    id="input-dy2",
                                    type="text",
                                    style=styleForValueMaxMinDown,
                                ),
                            ],
                            id="Block-down",
                            style={"display": "none"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    dcc.Upload(
                                        id="upload-one-water",
                                        children=html.Button(
                                            "Upload-1-water", id="Button-one-water"
                                        ),
                                        multiple=False,
                                    ),
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "21px",
                                        "margin-top": "15px",
                                    },
                                ),
                                html.Div(
                                    dcc.Upload(
                                        id="upload-one-xyzn",
                                        children=html.Button(
                                            "upload-1-xyzn", id="Button-one-xyzn"
                                        ),
                                        multiple=False,
                                    ),
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "21px",
                                    },
                                ),
                                html.Div(
                                    dcc.Upload(
                                        id="upload-one-f",
                                        children=html.Button(
                                            "upload-1-f", id="Button-one-f"
                                        ),
                                        multiple=False,
                                    ),
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "21px",
                                    },
                                ),
                                html.P(
                                    id="outputXY",
                                    children="Xmin Xmax Ymin Ymax value",
                                    style=styleForoutputMessageUp,
                                ),
                            ],
                            id="Block-up-xyzn",
                            style={"display": "none"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    dcc.Upload(
                                        id="upload-two-water",
                                        children=html.Button(
                                            "Upload-2-water", id="Button-two-water"
                                        ),
                                        multiple=False,
                                    ),
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "21px",
                                    },
                                ),
                                html.Div(
                                    dcc.Upload(
                                        id="upload-two-xyzn",
                                        children=html.Button(
                                            "upload-2-xyzn", id="Button-two-xyzn"
                                        ),
                                        multiple=False,
                                    ),
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "21px",
                                    },
                                ),
                                html.Div(
                                    dcc.Upload(
                                        id="upload-two-f",
                                        children=html.Button(
                                            "upload-2-f", id="Button-two-f"
                                        ),
                                        multiple=False,
                                    ),
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "21px",
                                    },
                                ),
                                html.P(
                                    id="outputXY2",
                                    children="Xmin2 Xmax2 Ymin2 Ymax2 value",
                                    style=styleForoutputMessageDown,
                                ),
                            ],
                            id="Block-down-xyzn",
                            style={"display": "none"},
                        ),
                    ],
                    style={
                        "marginTop": "0",
                        "marginLeft": "30px",
                        "display": "block",
                        "verticalAlign": "top",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    "Layer_One: ",
                                    style={
                                        "marginBottom": "4px",
                                        "display": "inline-block",
                                        "margin-right": "140px",
                                    },
                                ),
                                html.P(
                                    "Layer_Two: ",
                                    style={
                                        "marginBottom": "4px",
                                        "display": "inline-block",
                                        "margin-right": "140px",
                                    },
                                ),
                                html.P(
                                    "Y_Ori: ",
                                    style={
                                        "marginBottom": "4px",
                                        "display": "inline-block",
                                        "margin-right": "140px",
                                    },
                                ),
                                html.P(
                                    "Nagao_Advice: ",
                                    id="nagao_advices_text",
                                    style={
                                        "marginBottom": "4px",
                                        "display": "none",
                                        "margin-right": "140px",
                                    },
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.Div(
                                    style={
                                        "margin": "0 70px 0 0px",
                                        "display": "inline-block",
                                    }
                                ),
                                dcc.Dropdown(
                                    id="layer-first",
                                    options=layers,
                                    optionHeight=20,
                                    style={
                                        "padding": "0 0px 0 0px",
                                        "margin": "0 170px 0 0px",
                                        "width": "50px",
                                        "display": "inline-block",
                                        "font-size": "15px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="layer-second",
                                    options=layers,
                                    optionHeight=20,
                                    style={
                                        "padding": " 0 0 0 0px",
                                        "margin": "0 140px 0 0",
                                        "width": "50px",
                                        "display": "inline-block",
                                        "font-size": "15px",
                                    },
                                ),
                                dcc.RadioItems(
                                    id="Yori-chooser",
                                    options=[
                                        {"label": "upward", "value": "Y-upward"},
                                        {"label": "downward", "value": "Y-downward"},
                                    ],
                                    value="Y-downward",
                                    labelStyle={"display": "block"},
                                    style={
                                        "font-size": "20px",
                                        "margin-top": "0px",
                                        "display": "inline-block",
                                        "margin-right": "140px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="nagao_advices_selection",
                                    options=advices,
                                    optionHeight=30,
                                    disabled=True,
                                    style={
                                        "padding": " 0 0 0 0px",
                                        "margin": "0 0 0 0",
                                        "width": "180px",
                                        "display": "inline-block",
                                        "font-size": "15px",
                                    },
                                ),
                            ]
                        ),
                    ],
                    id="layerOriBlock",
                    style={
                        "marginTop": "0",
                        "marginLeft": "30px",
                        "display": "block",
                        "verticalAlign": "top",
                    },
                ),
            ],
            style={"display": "flex", "flexDirection": "row"},
        ),
        html.Button(
            id="Generate-xf",
            children="Generate-xyznf",
            style={
                "margin": "0",
                "height": "40px",
                "width": "120px",
                "backgroundColor": "#FFFFCC",
                "display": "none",
            },
        ),
        html.Div(
            [
                html.Button(
                    id="Generate-csv",
                    children="Generate-csv",
                    style={
                        "margin": "0",
                        "height": "40px",
                        "width": "120px",
                        "backgroundColor": "#FFFFCC",
                        "display": "inline-block",
                    },
                ),
                html.P(
                    id="outputmessage1",
                    children="Output-Message-File1",
                    style=styleForoutputMessageDown,
                ),
                html.P(
                    id="outputmessage2",
                    children="Output-Message-File2",
                    style=styleForoutputMessageDown,
                ),
            ],
            id="generate-csv-block",
        ),
        dcc.Loading(
            id="loading",
            type="cube",
            children=html.Div(id="loading-output", style={"font-weight": "bold"}),
        ),
        html.Button(
            id="Generate-2D",
            children="Generate-2D",
            style={
                "margin": "0",
                "height": "40px",
                "width": "120px",
                "backgroundColor": "#FFE4E1",
                "display": "block",
            },
        ),
        html.Div(
            id="graph-container", style={"display": "flex", "flexDirection": "row"}
        ),
    ],
    style={"transform": "scale(1)"},
)


def process_uploaded_file(contents, value):
    # Process the uploaded file and return the data
    content_string = contents.split(",")[1]
    decoded = base64.b64decode(content_string)
    data = pd.read_csv(io.StringIO(decoded.decode("utf-8")), header=None)
    deleted_columns = 0
    deleted_rows = 0
    while True:
        last_column = data.iloc[:, -1][0:5]
        last_row = data.iloc[-1, :][0:5]
        has_null_values_col = last_column.isnull().any()
        has_null_values_row = last_row.isnull().any()
        if has_null_values_col:
            data = data.iloc[:, :-1]
            deleted_columns += 1
        else:
            data = data.iloc[:, :]
            if not has_null_values_col and not has_null_values_row:
                break
        if has_null_values_row:
            data = data.iloc[:-1]
            deleted_rows += 1
        else:
            data = data.iloc[:, :]
            if not has_null_values_col and not has_null_values_row:
                break
    outputMessage = (
        f"Deleted {deleted_columns} columns and {deleted_rows} rows;Shapes:{data.shape}"
    )
    if value == "Y-upward":
        data = data.iloc[::-1]
    return data.values, outputMessage


def extract_filename(filename):
    filename_netname, filename_type = filename.split(".")
    return filename_netname


def create_3d_surface(height_grid, x, y, selected_colormap, title):
    fig = go.Figure(
        data=[
            go.Surface(
                z=height_grid,
                x=x,
                y=y,
                colorscale=selected_colormap,
                colorbar=dict(orientation="h"),
                contours=dict(
                    z=dict(
                        show=True,
                        usecolormap=True,
                        highlightcolor="limegreen",
                        project_z=True,
                    )
                ),
            )
        ],
        layout=go.Layout(title=title),
    )

    return fig


def create_2d_surface(height_grid, x, y, selected_colormap, title):
    fig = go.Figure(
        data=[
            go.Contour(
                z=height_grid,
                x=x,
                y=y,
                colorscale=selected_colormap,
                colorbar=dict(orientation="h"),
            )
        ],
        layout=go.Layout(title=title),
    )

    return fig


def create_3d_surface_frombin(
    file_water,
    file_xyzn,
    file_f,
    filename_water,
    selected_colormap,
    scaling_factor,
    scaling_factor_water,
    trim_value,
):
    # read xyzn data
    content_type, content_string_xyzn1 = file_xyzn.split(",")
    decoded_xyzn1 = base64.b64decode(content_string_xyzn1)
    with io.BytesIO(decoded_xyzn1) as file:
        file.read(4)
        is_, js, ks, IE, je, KE = struct.unpack(">6i", file.read(24))
        # print("is,js,ks,ie,je,ke \n",is_, js, ks, IE, je, KE)
        size_x0 = IE - (is_ - 2) + 2
        size_x1 = je - (js - 2) + 2
        size_x2 = KE - (ks - 2) + 2
        file.read(8)
        X0 = np.array(struct.unpack(f">{size_x0}d", file.read(size_x0 * 8)))
        file.read(8)
        X1 = np.array(struct.unpack(f">{size_x1}d", file.read(size_x1 * 8)))
        file.read(8)
        X2 = np.array(struct.unpack(f">{size_x2}d", file.read(size_x2 * 8)))
        file.read(8)
        (icc,) = struct.unpack(">i", file.read(4))
        # print("icc : ",icc)
        # Read conditional data
        conditional_data = {}
        for _ in range(icc):
            file.read(8)
            i, k, j, nf3, nfb3 = struct.unpack(">5i", file.read(20))
            conditional_data[(i, k, j)] = (nf3, nfb3)
    # read f data
    content_typef, content_string_f1 = file_f.split(",")
    decoded_f1 = base64.b64decode(content_string_f1)
    with io.BytesIO(decoded_f1) as file:
        file.read(4)
        ica, icb = struct.unpack(">2i", file.read(8))
        # print('ica:',ica,'icb:',icb)
        fb_data = {}
        for _ in range(ica):
            file.read(8)
            # Read X(0,:), X(1,:) and X(2,:) arrays
            (nn1,) = struct.unpack(">i", file.read(4))
            file.read(24)
            (af,) = struct.unpack(">d", file.read(8))
            fb_data[nn1] = af
    # read water data
    content_typew, content_string_water1 = file_water.split(",")
    decoded_water1 = base64.b64decode(content_string_water1)
    with io.BytesIO(decoded_water1) as file:
        file.read(4)
        c1a, c1b, c1c = struct.unpack(">3d", file.read(24))
        file.read(8)
        c2a, c2b = struct.unpack(">2i", file.read(8))
        F_data = {}
        for _ in range(ica):
            file.read(8)
            (nn2,) = struct.unpack(">i", file.read(4))
            if nn2 == ica + 1:
                break
            file.read(24)
            (uF,) = struct.unpack(">d", file.read(8))
            file.read(8)
            F_data[nn2] = uF
            file.read(8)
    # calculate for inne
    inne = 0
    mn = {}
    for j in range(js - 1, je + 1):
        for i in range(is_ - 1, IE + 1):
            k = ks
            mn[(i, j)] = [0, 0, 0]
            nf, nfb = conditional_data.get((i, k, j), (0, 0))
            if nf >= 0 or (nf == -1 and 1 <= nfb < 200):
                inne += 1
                mn[(i, j)] = [inne, 0, 0]
    # print("inne",inne)

    # append fb and F
    for j in range(js - 1, je):
        for i in range(is_ - 1, IE):
            inne_temp, fb_0, F_0 = mn.get((i, j))
            fb_temp = fb_data.get(inne_temp, 0)
            mn.get((i, j), [0, 0, 0])[1] = fb_temp
            F_temp = F_data.get(inne_temp, 0)
            mn.get((i, j), [0, 0, 0])[2] = F_temp

    # get the coordinate mapping data
    coord_mapping = {
        "istart": X0[is_ - 1],
        "iend": X0[-2],
        "jstart": X1[js - 1],
        "jend": X1[-2],
        "kstart": X2[ks - 1],
        "kend": X2[-2],
    }
    dx = round(X0[is_] - X0[is_ - 1], 3)
    dy = round(X1[js] - X1[js - 1], 3)
    dz = round(X2[ks] - X2[ks - 1], 3)
    # print("Xs,Xe,Ys,Ye,Zs,Ze \n",X0[is_-1],X0[-2],X1[js-1],X1[-2],X2[ks-1],X2[-2],"\n dx :",dx, "dy :",dy,"dz :",dz)
    ceiling_height = coord_mapping.get("kend")
    depth_grid = coord_mapping.get("kend") - coord_mapping.get("kstart")

    # Initialize 2D arrays for terr_ele and water_lev
    terr_ele_array = np.full((je - js, IE - is_), 0, dtype=float)
    water_lev_array = np.full((je - js, IE - is_), 0, dtype=float)
    for j in range(js, je):
        for i in range(is_, IE):
            inne_temp, fb_0, F_0 = mn.get((i, j))
            fb_0 = round(fb_0, 15)
            F_0 = round(F_0, 15)
            terr_ele = ceiling_height - depth_grid * fb_0
            water_lev = ceiling_height - depth_grid * fb_0 * (1 - F_0)
            # if water_lev == terr_ele:  #for boundary, needed modify
            #     water_lev = terr_ele-30.5
            terr_ele_array[j - js, i - is_] = round(terr_ele, 6)
            water_lev_array[j - js, i - is_] = round(water_lev, 6)
    mask = terr_ele_array == water_lev_array
    water_lev_array[mask] = np.nan
    x = np.linspace(
        int(coord_mapping.get("istart")) + dx / 2,
        int(coord_mapping.get("iend")) - dx / 2,
        IE - is_,
    )
    y = np.linspace(
        int(coord_mapping.get("jstart")) + dy / 2,
        int(coord_mapping.get("jend")) - dy / 2,
        je - js,
    )
    x, y = np.meshgrid(x, y)
    # get file name
    t_index = filename_water.find(".t")
    file_one_name = "T =" + filename_water[t_index + 2 :]
    z_terr = terr_ele_array
    if trim_value is not None:
        z_terr = np.where(terr_ele_array > float(trim_value), terr_ele_array, np.nan)
    fig_one = create_3d_surface(z_terr, x, y, selected_colormap, file_one_name)
    outputXY = f"Xmin={X0[is_-1]}, Xmax={X0[-2]}, Ymin={X1[js-1]}, Ymax={X1[-2]}, dx={dx},dy={dy}"
    water_lev_array_new = water_lev_array * scaling_factor_water
    fig_one.add_trace(
        go.Surface(
            x=x,
            y=y,
            z=water_lev_array_new,
            colorscale="Blues",
            opacity=0.5,
            showscale=False,
        )
    )
    fig_one.update_layout(
        scene=dict(
            xaxis_title="X-axis",
            yaxis_title="Y-axis",
            zaxis_title="Height",
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=-1.25, y=-2.0, z=1.25),
            ),
            aspectratio={"x": 1, "y": 1, "z": scaling_factor},
        )
    )
    trace_data = {
        "trace0": {"x": x.tolist(), "y": y.tolist(), "z": terr_ele_array.tolist()},
        "trace1": {"z": water_lev_array.tolist()},
    }
    trace_data_json = json.dumps(trace_data)
    return fig_one, outputXY, trace_data_json


# input Xmaxmin,Ymaxmin from layer_one option
@app.callback(
    Output("input-Xmax1", "value"),
    Output("input-Xmin1", "value"),
    Output("input-Ymax1", "value"),
    Output("input-Ymin1", "value"),
    Output("input-dx", "value"),
    Output("input-dy", "value"),
    Input("layer-first", "value"),
)
def undate_input(value):
    result = layermapping.get(value)
    if result is not None:
        Xmin1, Xmax1, Ymin1, Ymax1, dx, dy = result
        return Xmax1, Xmin1, Ymax1, Ymin1, dx, dy
    else:
        return 0, 0, 0, 0, 1, 1


# input Xmaxmin,Ymaxmin from layer_two option
@app.callback(
    Output("input-Xmax2", "value"),
    Output("input-Xmin2", "value"),
    Output("input-Ymax2", "value"),
    Output("input-Ymin2", "value"),
    Output("input-dx2", "value"),
    Output("input-dy2", "value"),
    Input("layer-second", "value"),
)
def undate_input(value):
    result = layermapping.get(value)
    if result is not None:
        Xmin2, Xmax2, Ymin2, Ymax2, dx, dy = result
        return Xmax2, Xmin2, Ymax2, Ymin2, dx, dy
    else:
        return 0, 0, 0, 0, 1, 1


# callback first for create the container
@app.callback(
    Output("graph-container", "children", allow_duplicate=True),
    Input("Generate-csv", "n_clicks"),
    Input("Generate-xf", "n_clicks"),
    prevent_initial_call=True,
)
def update_container(click, click2):
    children = [dcc.Graph(figure=go.Figure())]
    return children


# callback for files format choosen and file choosen
@app.callback(
    Output("layerOriBlock", "style"),
    Output("Block-up-xyzn", "style"),
    Output("Block-down-xyzn", "style"),
    Output("Block-up", "style"),
    Output("Block-down", "style"),
    Output("generate-csv-block", "style"),
    Output("Generate-xf", "style"),
    Input("file-chooser", "value"),
    Input("file-format-chooser", "value"),
)
def update_configuration(numvalue, value):
    if value == ".xyznf" and numvalue == "one":
        styleLayer = {"display": "none"}
        styleupxyzn = {"display": "block"}
        styledownxyzn = {"display": "none"}
        styleup = {"display": "none"}
        styledown = {"display": "none"}
        stylegeneratecsv = {"display": "none"}
        stylegeneratexf = {
            "margin-top": "20px",
            "height": "40px",
            "width": "120px",
            "backgroundColor": "#FFFFCC",
            "display": "block",
        }
    elif value == ".xyznf" and numvalue == "two":
        styleLayer = {"display": "none"}
        styleupxyzn = {"display": "block"}
        styledownxyzn = {"display": "block"}
        styleup = {"display": "none"}
        styledown = {"display": "none"}
        stylegeneratecsv = {"display": "none"}
        stylegeneratexf = {
            "margin-top": "20px",
            "height": "40px",
            "width": "120px",
            "backgroundColor": "#FFFFCC",
            "display": "block",
        }
    elif value == ".csv" and numvalue == "one":
        styleLayer = {"display": "block"}
        styleupxyzn = {"display": "none"}
        styledownxyzn = {"display": "none"}
        styleup = {"display": "block"}
        styledown = {"display": "none"}
        stylegeneratecsv = {"display": "block"}
        stylegeneratexf = {"display": "none"}

    elif value == ".csv" and numvalue == "two":
        styleLayer = {"display": "block"}
        styleupxyzn = {"display": "none"}
        styledownxyzn = {"display": "none"}
        styleup = {"display": "block"}
        styledown = {"display": "block"}
        stylegeneratecsv = {"display": "block"}
        stylegeneratexf = {"display": "none"}
    return (
        styleLayer,
        styleupxyzn,
        styledownxyzn,
        styleup,
        styledown,
        stylegeneratecsv,
        stylegeneratexf,
    )


# callback for generate 3D main
@app.callback(
    [
        Output("graph-container", "children"),
        Output("outputmessage1", "children"),
        Output("outputmessage2", "children"),
        Output("outputXY", "children"),
        Output("outputXY2", "children"),
        Output("trace-data", "data"),
        Output("trace-data2", "data"),
        Output("Button-one-water", "style"),
        Output("Button-one-xyzn", "style"),
        Output("Button-one-f", "style"),
        Output("Button-two-water", "style"),
        Output("Button-two-xyzn", "style"),
        Output("Button-two-f", "style"),
        Output("loading-output", "children"),
        Output("nagao_advices_text", "style"),
        Output("nagao_advices_selection", "disabled"),
    ],
    [
        Input("Generate-csv", "n_clicks"),
        Input("Generate-xf", "n_clicks"),
        Input("height-slider", "value"),
        Input("water-slider", "value"),
        Input("colormap-dropdown", "value"),
    ],
    [
        State("upload-data-one", "contents"),
        State("upload-data-two", "contents"),
        State("upload-data-one", "filename"),
        State("upload-data-two", "filename"),
        State("upload-one-xyzn", "filename"),
        State("upload-two-xyzn", "filename"),
        State("upload-one-water", "filename"),
        State("upload-two-water", "filename"),
        State("upload-one-water", "contents"),
        State("upload-one-xyzn", "contents"),
        State("upload-one-f", "contents"),
        State("upload-two-water", "contents"),
        State("upload-two-xyzn", "contents"),
        State("upload-two-f", "contents"),
        State("Trim Height", "value"),
        State("input-Xmax1", "value"),
        State("input-Xmin1", "value"),
        State("input-Ymax1", "value"),
        State("input-Ymin1", "value"),
        State("input-Xmax2", "value"),
        State("input-Xmin2", "value"),
        State("input-Ymax2", "value"),
        State("input-Ymin2", "value"),
        State("input-dx", "value"),
        State("input-dy", "value"),
        State("input-dx2", "value"),
        State("input-dy2", "value"),
        State("outputXY", "children"),
        State("outputXY2", "children"),
        State("Yori-chooser", "value"),
        State("file-chooser", "value"),
        State("file-format-chooser", "value"),
        State("trace-data", "data"),
        State("trace-data2", "data"),
        State("graph-container", "children"),
    ],
    prevent_initial_call=True,
)
def update_graph(
    click,
    click2,
    scaling_factor,
    scaling_factor_water,
    selected_colormap,
    file_one_contents,
    file_two_contents,
    file_one_filename,
    file_two_filename,
    filename_xyzn1,
    filename_xyzn2,
    filename_water1,
    filename_water2,
    file1_water,
    file1_xyzn,
    file1_f,
    file2_water,
    file2_xyzn,
    file2_f,
    trim_value,
    xmax1,
    xmin1,
    ymax1,
    ymin1,
    xmax2,
    xmin2,
    ymax2,
    ymin2,
    dx,
    dy,
    dx2,
    dy2,
    outputXY,
    outputXY2,
    Yori_chooser_value,
    file_chooser_value,
    file_formate_value,
    trace_data_json,
    trace_data2_json,
    figure_content,
):
    return_dic = {
        "children": None,
        "outputMessage1": None,
        "outputMessage2": None,
        "outputXY": outputXY,
        "outputXY2": outputXY2,
        "trace_data_json": None,
        "trace_data2_json": None,
        "style-water1": None,
        "style-xyzn1": None,
        "style-f1": None,
        "style-water2": None,
        "style-xyzn2": None,
        "style-f2": None,
        "loading": None,
        "advices_text": None,
        "advices_selection": None,
    }
    SuccessText = "Success!Generation complete"
    # change_id for get the content of the callback trigger
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    # slider change for terr in .csv
    if (
        file_formate_value == ".csv"
        and "height-slider" in changed_id
        and file_one_contents is not None
        and "Generate-csv" not in changed_id
    ):
        trace_data = json.loads(trace_data_json)
        x = trace_data["trace0"]["x"]
        y = trace_data["trace0"]["y"]
        z = trace_data["trace0"]["z"]
        file_one_name = extract_filename(file_one_filename)
        fig = go.Figure(
            data=[
                go.Surface(
                    z=z,
                    x=x,
                    y=y,
                    colorscale=selected_colormap,
                    colorbar=dict(orientation="h"),
                    contours=dict(
                        z=dict(
                            show=True,
                            usecolormap=True,
                            highlightcolor="limegreen",
                            project_z=True,
                        )
                    ),
                )
            ],
            layout=go.Layout(
                scene=dict(
                    xaxis_title="X-axis",
                    yaxis_title="Y-axis",
                    zaxis_title="Height",
                ),
                title=file_one_name,
            ),
        )
        fig.update_layout(
            scene=dict(
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=-1.25, y=-2.0, z=1.25),
                ),
                aspectratio={"x": 1, "y": 1, "z": scaling_factor},
            )
        )
        trace_data = {"trace0": {"x": x, "y": y, "z": z}}
        trace_data_json = json.dumps(trace_data)
        if file_chooser_value == "two":
            children = [dcc.Graph(figure=fig, style={"width": "50%", "height": "90vh"})]
            trace_data2 = json.loads(trace_data2_json)
            x2 = trace_data2["trace0"]["x"]
            y2 = trace_data2["trace0"]["y"]
            z2 = trace_data2["trace0"]["z"]
            file_two_name = extract_filename(file_two_filename)
            fig_two = go.Figure(
                data=[
                    go.Surface(
                        z=z2,
                        x=x2,
                        y=y2,
                        colorscale=selected_colormap,
                        colorbar=dict(orientation="h"),
                        contours=dict(
                            z=dict(
                                show=True,
                                usecolormap=True,
                                highlightcolor="limegreen",
                                project_z=True,
                            )
                        ),
                    )
                ],
                layout=go.Layout(
                    scene=dict(
                        xaxis_title="X-axis",
                        yaxis_title="Y-axis",
                        zaxis_title="Height",
                    ),
                    title=file_two_name,
                ),
            )
            fig_two.update_layout(
                scene=dict(
                    camera=dict(
                        up=dict(x=0, y=0, z=1),
                        center=dict(x=0, y=0, z=0),
                        eye=dict(x=-1.25, y=-2.0, z=1.25),
                    ),
                    aspectratio={"x": 1, "y": 1, "z": scaling_factor},
                )
            )
            children.append(
                dcc.Graph(figure=fig_two, style={"width": "50%", "height": "90vh"})
            )
            trace_data2 = {"trace0": {"x": x2, "y": y2, "z": z2}}
            trace_data2_json = json.dumps(trace_data2)
            return_dic["trace_data2_json"] = trace_data2_json
        else:
            children = [
                dcc.Graph(figure=fig, style={"width": "100%", "height": "90vh"})
            ]
        return_dic["children"] = children
        return_dic["trace_data_json"] = trace_data_json
        return_dic["loading"] = SuccessText
        return tuple(return_dic.values())

    # slider change for terr in .xyznf
    if (
        file_formate_value == ".xyznf"
        and ("height-slider" in changed_id or "water-slider" in changed_id)
        and "Generate-xf" not in changed_id
        and file1_xyzn is not None
        and file1_f is not None
        and file1_water is not None
    ):
        trace_data = json.loads(trace_data_json)
        x = trace_data["trace0"]["x"]
        y = trace_data["trace0"]["y"]
        z = trace_data["trace0"]["z"]
        zz = np.array(z)
        z_terr = zz
        if trim_value is not None:
            z_terr = np.where(zz > float(trim_value), zz, np.nan)
        z_water = trace_data["trace1"]["z"]
        z_r_water = np.array(z_water) * scaling_factor_water
        t_index = filename_water1.find(".t")
        file_one_name = "T =" + filename_water1[t_index + 2 :]
        fig = go.Figure(
            data=[
                go.Surface(
                    z=z_terr,
                    x=x,
                    y=y,
                    colorscale=selected_colormap,
                    colorbar=dict(orientation="h"),
                    contours=dict(
                        z=dict(
                            show=True,
                            usecolormap=True,
                            highlightcolor="limegreen",
                            project_z=True,
                        )
                    ),
                )
            ],
            layout=go.Layout(
                scene=dict(
                    xaxis_title="X-axis",
                    yaxis_title="Y-axis",
                    zaxis_title="Height",
                ),
                title=file_one_name,
            ),
        )
        fig.add_trace(
            go.Surface(
                x=x, y=y, z=z_r_water, colorscale="Blues", opacity=0.5, showscale=False
            )
        )
        fig.update_layout(
            scene=dict(
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=-1.25, y=-2.0, z=1.25),
                ),
                aspectratio={"x": 1, "y": 1, "z": scaling_factor},
            )
        )
        trace_data = {"trace0": {"x": x, "y": y, "z": z}, "trace1": {"z": z_water}}
        trace_data_json = json.dumps(trace_data)
        if file_chooser_value == "two":
            children = [dcc.Graph(figure=fig, style={"width": "50%", "height": "90vh"})]
            trace_data2 = json.loads(trace_data2_json)
            x2 = trace_data2["trace0"]["x"]
            y2 = trace_data2["trace0"]["y"]
            z2 = trace_data2["trace0"]["z"]
            zz2 = np.array(z2)
            z2_terr = zz2
            if trim_value is not None:
                z2_terr = np.where(zz2 > float(trim_value), zz2, np.nan)
            z2_water = trace_data2["trace1"]["z"]
            z2_r_water = np.array(z2_water) * scaling_factor_water
            t2_index = filename_water2.find(".t")
            file_two_name = "T =" + filename_water2[t2_index + 2 :]
            fig_two = go.Figure(
                data=[
                    go.Surface(
                        z=z2_terr,
                        x=x2,
                        y=y2,
                        colorscale=selected_colormap,
                        colorbar=dict(orientation="h"),
                        contours=dict(
                            z=dict(
                                show=True,
                                usecolormap=True,
                                highlightcolor="limegreen",
                                project_z=True,
                            )
                        ),
                    )
                ],
                layout=go.Layout(
                    scene=dict(
                        xaxis_title="X-axis",
                        yaxis_title="Y-axis",
                        zaxis_title="Height",
                    ),
                    title=file_two_name,
                ),
            )
            fig_two.add_trace(
                go.Surface(
                    x=x2,
                    y=y2,
                    z=z2_r_water,
                    colorscale="Blues",
                    opacity=0.5,
                    showscale=False,
                )
            )
            fig_two.update_layout(
                scene=dict(
                    camera=dict(
                        up=dict(x=0, y=0, z=1),
                        center=dict(x=0, y=0, z=0),
                        eye=dict(x=-1.25, y=-2.0, z=1.25),
                    ),
                    aspectratio={"x": 1, "y": 1, "z": scaling_factor},
                )
            )
            children.append(
                dcc.Graph(figure=fig_two, style={"width": "50%", "height": "90vh"})
            )
            trace_data2 = {
                "trace0": {"x": x2, "y": y2, "z": z2},
                "trace1": {"z": z2_water},
            }
            trace_data2_json = json.dumps(trace_data2)
            return_dic["trace_data2_json"] = trace_data2_json
        else:
            children = [
                dcc.Graph(figure=fig, style={"width": "100%", "height": "90vh"})
            ]
        return_dic["children"] = children
        return_dic["trace_data_json"] = trace_data_json
        return_dic["loading"] = SuccessText
        return tuple(return_dic.values())

    if file_formate_value == ".csv":
        if file_chooser_value == "one" and file_one_contents is None:
            return_dic["children"] = [dcc.Graph(figure=go.Figure())]
            return_dic["outputMessage1"] = "Output-Message-File1"
            return_dic["outputMessage2"] = "Output-Message-File2"
            return_dic["loading"] = "Please upload the file one"
            return tuple(return_dic.values())

        elif file_chooser_value == "two" and (
            file_one_contents is None or file_two_contents is None
        ):
            return_dic["children"] = [dcc.Graph(figure=go.Figure())]
            return_dic["outputMessage1"] = "Output-Message-File1"
            return_dic["outputMessage2"] = "Output-Message-File2"
            return_dic["loading"] = "Please upload the file one and file two"
            return tuple(return_dic.values())

        else:
            height_grid_one, outputMessage1 = process_uploaded_file(
                file_one_contents, Yori_chooser_value
            )
            height_grid_two = np.zeros_like(
                height_grid_one
            )  # Create an empty array for the second file
            file_one_name = extract_filename(file_one_filename)
            sh_y1, sh_x1 = height_grid_one.shape
            if xmax1 == 0 and ymax1 == 0:
                xmax1 = xmin1 + sh_x1
                ymax1 = ymin1 + sh_y1
            # Create the X, Y coordinates for the grid
            x, y = np.linspace(
                int(xmin1) + dx / 2, int(xmax1) - dx / 2, sh_x1
            ), np.linspace(int(ymin1) + dy / 2, int(ymax1) - dy / 2, sh_y1)
            # Create 3D surface plots for each file
            fig_one = create_3d_surface(
                height_grid_one, x, y, selected_colormap, file_one_name
            )
            fig_one.update_layout(
                scene=dict(
                    xaxis=dict(title="X-axis", visible=True),
                    yaxis=dict(title="Y-axis", visible=True),
                    zaxis=dict(title="Height", visible=True),
                    camera=dict(
                        up=dict(x=0, y=0, z=1),
                        center=dict(x=0, y=0, z=0),
                        eye=dict(x=-1.25, y=-2.0, z=1.25),
                        # eye=dict(x=0, y=0, z=2),
                    ),
                    aspectratio={"x": 1, "y": 1, "z": scaling_factor},
                )
            )
            trace_data = {
                "trace0": {
                    "x": x.tolist(),
                    "y": y.tolist(),
                    "z": height_grid_one.tolist(),
                }
            }
            trace_data_json = json.dumps(trace_data)
            return_dic["advices_text"] = {"display": "inline-block"}
            return_dic["advices_selection"] = False

        if file_chooser_value == "two":
            children = [
                dcc.Graph(figure=fig_one, style={"width": "50%", "height": "90vh"})
            ]
            height_grid_two, outputMessage2 = process_uploaded_file(
                file_two_contents, Yori_chooser_value
            )
            sh_y2, sh_x2 = height_grid_two.shape
            if xmax2 == 0 and ymax2 == 0:
                xmax2 = xmin2 + sh_x2
                ymax2 = ymin2 + sh_y2
            x2, y2 = np.linspace(
                int(xmin2) + dx2 / 2, int(xmax2) - dx2 / 2, sh_x2
            ), np.linspace(int(ymin2) + dy2 / 2, int(ymax2) - dy / 2, sh_y2)
            file_two_name = extract_filename(file_two_filename)
            return_dic["outputMessage2"] = outputMessage2
            fig_two = create_3d_surface(
                height_grid_two, x2, y2, selected_colormap, file_two_name
            )
            fig_two.update_layout(
                scene=dict(
                    xaxis_title="X-axis",
                    yaxis_title="Y-axis",
                    zaxis_title="Height",
                    camera=dict(
                        up=dict(x=0, y=0, z=1),
                        center=dict(x=0, y=0, z=0),
                        eye=dict(x=-1.25, y=-2.0, z=1.25),
                    ),
                    aspectratio={"x": 1, "y": 1, "z": scaling_factor},
                )
            )
            children.append(
                dcc.Graph(figure=fig_two, style={"width": "50%", "height": "90vh"})
            )
            trace_data2 = {
                "trace0": {
                    "x": x2.tolist(),
                    "y": y2.tolist(),
                    "z": height_grid_two.tolist(),
                }
            }
            trace_data2_json = json.dumps(trace_data2)
            return_dic["trace_data2_json"] = trace_data2_json
        else:
            children = [
                dcc.Graph(
                    id="3d-graph",
                    figure=fig_one,
                    style={"width": "100%", "height": "90vh"},
                )
            ]
        ### change the width of graph according to the number of the figures

        return_dic["children"] = children
        return_dic["outputMessage1"] = outputMessage1
        return_dic["loading"] = SuccessText
        return_dic["trace_data_json"] = trace_data_json
        return tuple(return_dic.values())

    else:
        if file_chooser_value == "one" and (
            file1_xyzn is None or file1_f is None or file1_water is None
        ):
            return_dic["children"] = [dcc.Graph(figure=go.Figure())]
            return_dic["outputMessage1"] = "Output-Message-File1"
            return_dic["outputMessage2"] = "Output-Message-File2"
            return_dic["outputXY"] = "Xmin Xmax Ymin Ymax value"
            return_dic["outputXY2"] = "Xmin2 Xmax2 Ymin2 Ymax2 value"
            if file1_water is not None:
                return_dic["style-water1"] = {
                    "backgroundColor": "green",
                    "color": "white",
                }
            if file1_xyzn is not None:
                return_dic["style-xyzn1"] = {
                    "backgroundColor": "green",
                    "color": "white",
                }
            if file1_f is not None:
                return_dic["style-f1"] = {"backgroundColor": "green", "color": "white"}
            return_dic["loading"] = "Please upload file which is gray"
            return tuple(return_dic.values())

        elif file_chooser_value == "two" and (
            file1_xyzn is None
            or file1_f is None
            or file1_water is None
            or file2_xyzn is None
            or file2_f is None
            or file2_water is None
        ):
            return_dic["children"] = [dcc.Graph(figure=go.Figure())]
            return_dic["outputMessage1"] = "Output-Message-File1"
            return_dic["outputMessage2"] = "Output-Message-File2"
            return_dic["outputXY"] = "Xmin Xmax Ymin Ymax value"
            return_dic["outputXY2"] = "Xmin2 Xmax2 Ymin2 Ymax2 value"
            return_dic["trace_data_json"] = None
            if file1_water is not None:
                return_dic["style-water1"] = {
                    "backgroundColor": "green",
                    "color": "white",
                }
            if file1_xyzn is not None:
                return_dic["style-xyzn1"] = {
                    "backgroundColor": "green",
                    "color": "white",
                }
            if file1_f is not None:
                return_dic["style-f1"] = {"backgroundColor": "green", "color": "white"}
            if file2_water is not None:
                return_dic["style-water2"] = {
                    "backgroundColor": "green",
                    "color": "white",
                }
            if file2_xyzn is not None:
                return_dic["style-xyzn2"] = {
                    "backgroundColor": "green",
                    "color": "white",
                }
            if file2_f is not None:
                return_dic["style-f2"] = {"backgroundColor": "green", "color": "white"}
            return_dic["loading"] = "Please upload file which is gray"
            return tuple(return_dic.values())

        else:
            fig_one, outputXY, trace_data_json = create_3d_surface_frombin(
                file1_water,
                file1_xyzn,
                file1_f,
                filename_water1,
                selected_colormap,
                scaling_factor,
                scaling_factor_water,
                trim_value,
            )
            return_dic["outputXY"] = outputXY
            return_dic["trace_data_json"] = trace_data_json

        if file_chooser_value == "two":
            children = [
                dcc.Graph(figure=fig_one, style={"width": "50%", "height": "90vh"})
            ]
            fig_two, outputXY2, trace_data2_json = create_3d_surface_frombin(
                file2_water,
                file2_xyzn,
                file2_f,
                filename_water2,
                selected_colormap,
                scaling_factor,
                scaling_factor_water,
                trim_value,
            )
            children.append(
                dcc.Graph(figure=fig_two, style={"width": "50%", "height": "90vh"})
            )
            return_dic["outputXY2"] = outputXY2
            return_dic["trace_data2_json"] = trace_data2_json
        ### change the width of graph according to the number of the figures
        else:
            children = [
                dcc.Graph(figure=fig_one, style={"width": "100%", "height": "90vh"})
            ]

        return_dic["children"] = children
        return_dic["loading"] = "Generate Success"
        return tuple(return_dic.values())


# callback for generate 2D main
@app.callback(
    [
        Output("graph-container", "children", allow_duplicate=True),
        Output("loading-output", "children", allow_duplicate=True),
    ],
    [Input("Generate-2D", "n_clicks")],
    [
        State("upload-data-one", "contents"),
        State("upload-data-two", "contents"),
        State("upload-data-one", "filename"),
        State("upload-data-two", "filename"),
        State("input-Xmax1", "value"),
        State("input-Xmin1", "value"),
        State("input-Ymax1", "value"),
        State("input-Ymin1", "value"),
        State("input-Xmax2", "value"),
        State("input-Xmin2", "value"),
        State("input-Ymax2", "value"),
        State("input-Ymin2", "value"),
        State("input-dx", "value"),
        State("input-dy", "value"),
        State("input-dx2", "value"),
        State("input-dy2", "value"),
        State("Yori-chooser", "value"),
        State("file-chooser", "value"),
        State("file-format-chooser", "value"),
        State("colormap-dropdown", "value"),
    ],
    prevent_initial_call=True,
)
def update_graph_2D(
    click,
    file_one_contents,
    file_two_contents,
    file_one_filename,
    file_two_filename,
    xmax1,
    xmin1,
    ymax1,
    ymin1,
    xmax2,
    xmin2,
    ymax2,
    ymin2,
    dx,
    dy,
    dx2,
    dy2,
    Yori_chooser_value,
    file_chooser_value,
    file_formate_value,
    selected_colormap,
):
    return_dic = {"children": None, "loading": None}
    SuccessText = "Success!Generation complete"
    if file_formate_value == ".csv":
        if file_chooser_value == "one" and file_one_contents is None:
            return_dic["children"] = [dcc.Graph(figure=go.Figure())]
            return_dic["loading"] = "Please upload the file one"
            return tuple(return_dic.values())

        elif file_chooser_value == "two" and (
            file_one_contents is None or file_two_contents is None
        ):
            return_dic["children"] = [dcc.Graph(figure=go.Figure())]
            return_dic["loading"] = "Please upload the file one and file two"
            return tuple(return_dic.values())

        else:
            height_grid_one, outputMessage1 = process_uploaded_file(
                file_one_contents, Yori_chooser_value
            )
            height_grid_two = np.zeros_like(
                height_grid_one
            )  # Create an empty array for the second file
            file_one_name = extract_filename(file_one_filename)
            # Create the X, Y coordinates for the grid
            sh_y1, sh_x1 = height_grid_one.shape
            x, y = np.linspace(
                int(xmin1) + dx / 2, int(xmax1) - dx / 2, sh_x1
            ), np.linspace(int(ymin1) + dy / 2, int(ymax1) - dy / 2, sh_y1)
            fig_one = create_2d_surface(
                height_grid_one, x, y, selected_colormap, file_one_name
            )
            fig_one.update_layout(
                scene=dict(xaxis_title="X-axis", yaxis_title="Y-axis")
            )
        if file_chooser_value == "two":
            children = [
                dcc.Graph(figure=fig_one, style={"width": "50%", "height": "90vh"})
            ]
            height_grid_two, outputMessage2 = process_uploaded_file(
                file_two_contents, Yori_chooser_value
            )
            sh_y2, sh_x2 = height_grid_two.shape
            x2, y2 = np.linspace(
                int(xmin2) + dx2 / 2, int(xmax2) - dx2 / 2, sh_x2
            ), np.linspace(int(ymin2) + dy2 / 2, int(ymax2) - dy / 2, sh_y2)
            file_two_name = extract_filename(file_two_filename)
            fig_two = create_2d_surface(
                height_grid_two, x2, y2, selected_colormap, file_two_name
            )
            fig_two.update_layout(
                scene=dict(xaxis_title="X-axis", yaxis_title="Y-axis")
            )
            children.append(
                dcc.Graph(figure=fig_two, style={"width": "50%", "height": "90vh"})
            )
        else:
            children = [
                dcc.Graph(figure=fig_one, style={"width": "100%", "height": "90vh"})
            ]
        return_dic["children"] = children
        return_dic["loading"] = SuccessText
        return tuple(return_dic.values())


# callback for advices
@app.callback(
    Output("3d-graph", "figure"),
    [
        Input("nagao_advices_selection", "value"),
        Input("3d-graph", "figure"),
        Input("Colorbar Max", "value"),
        Input("Colorbar Min", "value"),
    ],
    prevent_initial_call=True,
)
def update_figure_from_advies(value, figure, max_value, min_value):
    if value == "Hide Coordinates":
        figure["layout"]["scene"]["xaxis"]["visible"] = False
        figure["layout"]["scene"]["yaxis"]["visible"] = False
        figure["layout"]["scene"]["zaxis"]["visible"] = False
        return figure
    elif value == "Top View":
        figure["layout"]["scene"]["camera"]["eye"]["z"] = 2
        figure["layout"]["scene"]["camera"]["eye"]["y"] = 0
        figure["layout"]["scene"]["camera"]["eye"]["x"] = 0
        figure["layout"]["scene"]["camera"]["up"]["z"] = 0
        figure["layout"]["scene"]["camera"]["up"]["y"] = 1
        figure["layout"]["scene"]["camera"]["up"]["x"] = 0
        return figure
    elif value == "Change Colorbar Variation":
        figure["data"][0]["cmax"] = max_value
        figure["data"][0]["cmin"] = min_value
        return figure
    else:
        return figure


if __name__ == "__main__":
    app.run(debug=True)
