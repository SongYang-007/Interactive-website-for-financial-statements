import base64
import io

import numpy as np
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------
# 1. 默认示例数据（就是你发给我的 Raw Data）
# -----------------------------------------------------------

def get_default_data():
    years = ["Year -4", "Year -3", "Year -2", "Year -1", "Year 0"]

    revenue_df = pd.DataFrame(
        {
            "Year": years,
            "Business 1": [102_007, 118_086, 131_345, 142_341, 150_772],
            "Business 2": [156_387, 158_882, 160_034, 174_988, 191_520],
            "Business 3": [134_622, 138_520, 143_362, 145_897, 148_631],
            "Consolidated": [393_016, 415_488, 434_741, 463_226, 490_923],
            "COGS": [207_069, 206_012, 218_369, 227_962, 243_130],
            "Profit Margin ($)": [26_063, 34_177, 43_380, 64_068, 70_081],
            "Profit Margin (%)": [0.07, 0.08, 0.10, 0.14, 0.14],
        }
    )

    expenses_df = pd.DataFrame(
        {
            "Year": years,
            "Salaries and Benefits": [70_854, 77_974, 81_616, 79_006, 85_735],
            "Rent and Overhead": [32_789, 35_375, 35_261, 38_060, 39_236],
            "Depreciation & Amortization": [48_741, 54_450, 51_615, 49_631, 48_241],
            "Interest": [7_500, 7_500, 4_500, 4_500, 4_500],
            "Total": [159_884, 175_299, 172_992, 171_197, 177_712],
        }
    )

    budget_year0 = {
        "Revenue": 475_000,
        "COGS": 238_000,
        "Expenses": 186_000,
        "Profit Margin": 73_500,
        "Profit Margin (%)": 0.155,
    }

    balance_sheet = {
        "Current Assets": 395_685,
        "Non-current Assets": 589_610,
        "Total Assets": 985_295,
        "Current Liabilities": 135_374,
        "Long-term Liabilities": 384_962,
        "Shareholders' Equity": 464_959,
        "Liabilities & Shareholders' Equity": 985_295,
    }

    return revenue_df, expenses_df, budget_year0, balance_sheet


# -----------------------------------------------------------
# 2. 解析上传文件（可选）
# -----------------------------------------------------------

def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    if filename.lower().endswith(".csv"):
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    else:
        df = pd.read_excel(io.BytesIO(decoded))

    required_cols = [
        "Year",
        "Business 1",
        "Business 2",
        "Business 3",
        "Consolidated",
        "COGS",
        "Profit Margin ($)",
        "Profit Margin (%)",
        "Salaries and Benefits",
        "Rent and Overhead",
        "Depreciation & Amortization",
        "Interest",
        "Total Expenses",
    ]
    if "Total" in df.columns and "Total Expenses" not in df.columns:
        df = df.rename(columns={"Total": "Total Expenses"})

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in uploaded file: {missing}")

    rev_cols = [
        "Year",
        "Business 1",
        "Business 2",
        "Business 3",
        "Consolidated",
        "COGS",
        "Profit Margin ($)",
        "Profit Margin (%)",
    ]
    revenue_df = df[rev_cols].copy()

    exp_cols = [
        "Year",
        "Salaries and Benefits",
        "Rent and Overhead",
        "Depreciation & Amortization",
        "Interest",
        "Total Expenses",
    ]
    expenses_df = df[exp_cols].copy()
    expenses_df = expenses_df.rename(columns={"Total Expenses": "Total"})

    _, _, budget, bs = get_default_data()
    return revenue_df, expenses_df, budget, bs


# -----------------------------------------------------------
# 3. 图表函数（颜色区分好 + 字体放松一点）
# -----------------------------------------------------------

def base_layout(title):
    # 不在这里设置 margin，避免重复传参
    return dict(
        title=title,
        template="plotly_white",
        font=dict(family="Arial", size=12),
    )


def build_business_unit_revenue_figure(revenue_df):
    years = revenue_df["Year"]

    fig = go.Figure()
    fig.add_bar(
        x=years,
        y=revenue_df["Business 1"],
        name="Business 1",
        marker_color="#4F81BD",
    )
    fig.add_bar(
        x=years,
        y=revenue_df["Business 2"],
        name="Business 2",
        marker_color="#A5A5A5",
    )
    fig.add_bar(
        x=years,
        y=revenue_df["Business 3"],
        name="Business 3",
        marker_color="#5B9BD5",
    )

    fig.update_layout(
        **base_layout("Business Unit Revenue"),
        barmode="stack",
        xaxis_title="Year",
        yaxis_title="Revenue (USD thousands)",
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.15,
            font=dict(size=11),
        ),
        margin=dict(l=50, r=40, t=60, b=50),
    )
    return fig


def build_profit_margin_figure(revenue_df):
    years = revenue_df["Year"]

    fig = go.Figure()

    fig.add_bar(
        x=years,
        y=revenue_df["Profit Margin ($)"],
        name="Profit Margin ($)",
        marker_color="#4472C4",
        yaxis="y1",
    )

    fig.add_trace(
        go.Scatter(
            x=years,
            y=revenue_df["Profit Margin (%)"] * 100,
            name="Profit Margin (%)",
            mode="lines+markers",
            marker=dict(size=7, color="#ED7D31"),
            line=dict(width=2, color="#ED7D31", dash="dash"),
            yaxis="y2",
        )
    )

    fig.update_layout(
        **base_layout("Profit Margin"),
        xaxis=dict(title="Year"),
        yaxis=dict(
            title="Profit Margin ($)",
            side="left",
            showgrid=True,
        ),
        yaxis2=dict(
            title="Profit Margin (%)",
            overlaying="y",
            side="right",
            tickformat=".0f",
        ),
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.15,
            font=dict(size=11),
        ),
        margin=dict(l=50, r=40, t=60, b=50),
    )
    return fig


def build_cumulative_revenue_figure(revenue_df):
    year0 = revenue_df.iloc[-1]
    x = ["Business 1", "Business 2", "Business 3", "Consolidated"]
    y = [year0["Business 1"], year0["Business 2"], year0["Business 3"], year0["Consolidated"]]

    fig = go.Figure(
        go.Waterfall(
            x=x,
            y=y,
            measure=["relative", "relative", "relative", "total"],
            text=[f"{v:,.0f}" for v in y],
            textposition="outside",
            connector={"line": {"color": "rgb(150,150,150)"}},
        )
    )
    fig.update_layout(
        **base_layout("Cumulative Revenue (Year 0)"),
        yaxis_title="Revenue (USD thousands)",
        margin=dict(l=50, r=40, t=60, b=50),
    )
    return fig


def build_expenses_figure(expenses_df):
    years = expenses_df["Year"]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=years,
            y=expenses_df["Salaries and Benefits"],
            stackgroup="one",
            name="Salaries and Benefits",
            mode="none",
            fillcolor="#4472C4",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=expenses_df["Rent and Overhead"],
            stackgroup="one",
            name="Rent and Overhead",
            mode="none",
            fillcolor="#A5A5A5",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=expenses_df["Depreciation & Amortization"],
            stackgroup="one",
            name="Depreciation & Amortization",
            mode="none",
            fillcolor="#5B9BD5",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=expenses_df["Interest"],
            stackgroup="one",
            name="Interest",
            mode="none",
            fillcolor="#FFC000",
        )
    )

    fig.update_layout(
        **base_layout("Expenses"),
        xaxis_title="Year",
        yaxis_title="Amount (USD thousands)",
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.18,
            font=dict(size=11),
        ),
        margin=dict(l=50, r=40, t=70, b=50),
    )
    return fig


# -------- Performance Summary：表格 + 右侧微缩柱状+折线图 ----------

def build_performance_summary_section(revenue_df, expenses_df):
    avg_revenue = revenue_df["Consolidated"].mean()
    avg_cogs = revenue_df["COGS"].mean()
    avg_exp = expenses_df["Total"].mean()
    avg_prof = revenue_df["Profit Margin ($)"].mean()
    avg_prof_pct = revenue_df["Profit Margin (%)"].mean() * 100

    metrics = [
        "Revenue",
        "COGS",
        "Expenses",
        "Profit Margin",
        "Profit Margin (%)",
    ]
    averages = [
        avg_revenue,
        avg_cogs,
        avg_exp,
        avg_prof,
        avg_prof_pct,
    ]

    table_df = pd.DataFrame(
        {"Metric": metrics, "5-Yr Average": averages}
    )

    perf_table = dash_table.DataTable(
        columns=[
            {"name": "Metric", "id": "Metric"},
            {"name": "5-Yr Average", "id": "5-Yr Average", "type": "numeric"},
        ],
        data=table_df.to_dict("records"),
        style_cell={
            "textAlign": "left",
            "padding": "8px",
            "fontFamily": "Arial",
            "fontSize": 13,
        },
        style_header={
            "fontWeight": "bold",
            "backgroundColor": "#f2f2f2",
        },
        style_data_conditional=[
            {"if": {"column_id": "5-Yr Average"}, "textAlign": "right"},
        ],
        style_table={"width": "100%"},
    )

    years = revenue_df["Year"]
    series_dict = {
        "Revenue": revenue_df["Consolidated"],
        "COGS": revenue_df["COGS"],
        "Expenses": expenses_df["Total"],
        "Profit Margin": revenue_df["Profit Margin ($)"],
        "Profit Margin (%)": revenue_df["Profit Margin (%)"] * 100,
    }

    colors_bar = {
        "Revenue": "#4F81BD",
        "COGS": "#A5A5A5",
        "Expenses": "#5B9BD5",
        "Profit Margin": "#70AD47",
        "Profit Margin (%)": "#ED7D31",
    }

    colors_line = {
        "Revenue": "#2F5597",
        "COGS": "#7F7F7F",
        "Expenses": "#2E75B6",
        "Profit Margin": "#548235",
        "Profit Margin (%)": "#C55A11",
    }

    fig = make_subplots(
        rows=5,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=metrics,
    )

    for i, metric in enumerate(metrics, start=1):
        s = series_dict[metric]
        fig.add_trace(
            go.Bar(
                x=years,
                y=s,
                marker_color=colors_bar[metric],
                showlegend=False,
            ),
            row=i,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=years,
                y=s,
                mode="lines+markers",
                line=dict(color=colors_line[metric], width=2),
                marker=dict(size=4),
                showlegend=False,
            ),
            row=i,
            col=1,
        )
        fig.update_yaxes(showticklabels=False, row=i, col=1)
        fig.update_xaxes(showgrid=False, row=i, col=1)

    fig.update_layout(
        **base_layout("Trend (Five-Year – Micro Charts)"),
        height=420,
        margin=dict(l=40, r=20, t=60, b=40),
    )

    perf_graph = dcc.Graph(
        figure=fig,
        config={"displayModeBar": False},
        style={"height": "420px"},
    )

    return html.Div(
        className="row",
        children=[
            html.Div(perf_table, className="six columns"),
            html.Div(perf_graph, className="six columns"),
        ],
        style={"padding": "0 10px"},
    )


# ----------------- Income Statement ------------------------

def build_income_statement_table(revenue_df, expenses_df, budget_year0):
    year0_rev = revenue_df.iloc[-1]
    year0_exp = expenses_df.iloc[-1]

    actual_revenue = year0_rev["Consolidated"]
    actual_cogs = year0_rev["COGS"]
    actual_expenses = year0_exp["Total"]
    actual_profit = year0_rev["Profit Margin ($)"]
    actual_profit_pct = year0_rev["Profit Margin (%)"]

    lines = [
        ("Revenue", actual_revenue, budget_year0["Revenue"]),
        ("COGS", actual_cogs, budget_year0["COGS"]),
        ("Expenses", actual_expenses, budget_year0["Expenses"]),
        ("Profit Margin", actual_profit, budget_year0["Profit Margin"]),
        ("Profit Margin (%)", actual_profit_pct * 100, budget_year0["Profit Margin (%)"] * 100),
    ]

    records = []
    for name, actual, budget in lines:
        variance = actual - budget
        var_pct = variance / budget * 100 if budget != 0 else np.nan
        records.append(
            {
                "Item": name,
                "Actual": actual,
                "Budget": budget,
                "Variance": variance,
                "Var%": var_pct,
            }
        )

    df = pd.DataFrame(records)

    table = dash_table.DataTable(
        columns=[
            {"name": "Item", "id": "Item"},
            {"name": "Actual", "id": "Actual", "type": "numeric"},
            {"name": "Budget", "id": "Budget", "type": "numeric"},
            {"name": "Variance", "id": "Variance", "type": "numeric"},
            {"name": "Var%", "id": "Var%", "type": "numeric"},
        ],
        data=df.to_dict("records"),
        style_cell={
            "textAlign": "right",
            "padding": "8px",
            "fontFamily": "Arial",
            "fontSize": 13,
        },
        style_header={
            "fontWeight": "bold",
            "backgroundColor": "#f2f2f2",
        },
        style_data_conditional=[
            {"if": {"column_id": "Item"}, "textAlign": "left"},
            {"if": {"filter_query": "{Variance} < 0", "column_id": "Variance"}, "color": "red"},
            {"if": {"filter_query": "{Variance} > 0", "column_id": "Variance"}, "color": "green"},
            {"if": {"filter_query": "{Var%} < 0", "column_id": "Var%"}, "color": "red"},
            {"if": {"filter_query": "{Var%} > 0", "column_id": "Var%"}, "color": "green"},
        ],
        style_table={"width": "100%"},
    )
    return table


# ----------------- P&L Summary -----------------------------

def build_pl_summary_table(revenue_df, expenses_df):
    year0_rev = revenue_df.iloc[-1]
    year0_exp = expenses_df.iloc[-1]

    records = [
        {"Item": "Revenue", "Amount": year0_rev["Consolidated"]},
        {"Item": "COGS", "Amount": year0_rev["COGS"]},
        {"Item": "", "Amount": ""},
        {"Item": "Salaries and Benefits", "Amount": year0_exp["Salaries and Benefits"]},
        {"Item": "Rent and Overhead", "Amount": year0_exp["Rent and Overhead"]},
        {"Item": "Depreciation & Amortization", "Amount": year0_exp["Depreciation & Amortization"]},
        {"Item": "Interest", "Amount": year0_exp["Interest"]},
        {"Item": "Total Expenses", "Amount": year0_exp["Total"]},
        {"Item": "", "Amount": ""},
        {"Item": "Net Operating Profit", "Amount": year0_rev["Profit Margin ($)"]},
    ]
    df = pd.DataFrame(records)

    table = dash_table.DataTable(
        columns=[
            {"name": "Item", "id": "Item"},
            {"name": "Amount", "id": "Amount"},
        ],
        data=df.to_dict("records"),
        style_cell={
            "textAlign": "right",
            "padding": "8px",
            "fontFamily": "Arial",
            "fontSize": 13,
        },
        style_header={
            "fontWeight": "bold",
            "backgroundColor": "#f2f2f2",
        },
        style_data_conditional=[
            {"if": {"column_id": "Item"}, "textAlign": "left"},
            {"if": {"filter_query": "{Item} = 'Net Operating Profit'"}, "fontWeight": "bold"},
        ],
        style_table={"width": "100%"},
    )
    return table


# ----------------- Balance Sheet Summary （HTML排版版）-------

def build_balance_sheet_section(balance_sheet):

    def fmt(x):
        return f"{x:,.0f}"

    row_style = {
        "display": "flex",
        "justifyContent": "space-between",
        "padding": "2px 0",
    }

    left_style = {
        "width": "60%",
    }

    right_style = {
        "width": "40%",
        "textAlign": "right",
    }

    def row(label, value, bold=False, underline=False):
        style_right = right_style.copy()
        style_left = left_style.copy()
        if bold:
            style_left["fontWeight"] = "bold"
            style_right["fontWeight"] = "bold"
        if underline:
            style_right["borderBottom"] = "2px solid #999"
            style_right["paddingBottom"] = "2px"
        return html.Div(
            [
                html.Div(label, style=style_left),
                html.Div("" if value == "" else fmt(value), style=style_right),
            ],
            style=row_style,
        )

    return html.Div(
        [
            html.Div(
                "Balance Sheet Summary (Year 0)",
                style={
                    "fontWeight": "bold",
                    "marginBottom": "10px",
                    "fontSize": "16px",
                    "textAlign": "left",
                },
            ),

            html.Div("Assets", style={"fontWeight": "bold", "marginTop": "10px", "marginBottom": "5px"}),
            row("Current Assets", balance_sheet["Current Assets"]),
            row("Non-current Assets", balance_sheet["Non-current Assets"]),
            row("Total Assets", balance_sheet["Total Assets"], bold=True, underline=True),

            html.Div("Liabilities", style={"fontWeight": "bold", "marginTop": "20px", "marginBottom": "5px"}),
            row("Current Liabilities", balance_sheet["Current Liabilities"]),
            row("Long-term Liabilities", balance_sheet["Long-term Liabilities"]),
            row("Shareholders' Equity", balance_sheet["Shareholders' Equity"]),
            row(
                "Liabilities & Shareholders' Equity",
                balance_sheet["Liabilities & Shareholders' Equity"],
                bold=True,
                underline=True,
            ),
        ],
        style={
            "fontFamily": "Arial",
            "fontSize": "14px",
            "width": "100%",
            "padding": "10px 20px",
            "backgroundColor": "white",
        },
    )


# -----------------------------------------------------------
# 4. 先用默认数据生成「初始图 & 表」，避免空画布
# -----------------------------------------------------------

_default_rev, _default_exp, _default_budget, _default_bs = get_default_data()

default_rev_fig = build_business_unit_revenue_figure(_default_rev)
default_pm_fig = build_profit_margin_figure(_default_rev)
default_cum_fig = build_cumulative_revenue_figure(_default_rev)
default_exp_fig = build_expenses_figure(_default_exp)
default_perf_section = build_performance_summary_section(_default_rev, _default_exp)
default_is_table = build_income_statement_table(_default_rev, _default_exp, _default_budget)
default_pl_table = build_pl_summary_table(_default_rev, _default_exp)
default_bs_section = build_balance_sheet_section(_default_bs)


# -----------------------------------------------------------
# 5. Dash Layout
# -----------------------------------------------------------

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Financial Dashboard"

app.layout = html.Div(
    [
        html.H2("Financial Dashboard", style={"textAlign": "center", "marginBottom": "10px"}),

        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select File")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px 0 20px 0",
            },
            multiple=False,
        ),
        html.Div(id="upload-status", style={"marginBottom": "20px", "fontStyle": "italic"}),

        html.Div(
            className="row",
            children=[
                html.Div(dcc.Graph(id="rev_graph", figure=default_rev_fig), className="six columns"),
                html.Div(dcc.Graph(id="pm_graph", figure=default_pm_fig), className="six columns"),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(dcc.Graph(id="cumrev_graph", figure=default_cum_fig), className="six columns"),
                html.Div(dcc.Graph(id="exp_graph", figure=default_exp_fig), className="six columns"),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    [
                        html.H4("Performance Summary (Five-Year)", style={"marginTop": "30px"}),
                        html.Div(id="perf_table", children=default_perf_section),
                    ],
                    className="six columns",
                ),
                html.Div(
                    [
                        html.H4("Income Statement (Year 0)", style={"marginTop": "30px"}),
                        html.Div(id="is_table", children=default_is_table),
                    ],
                    className="six columns",
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    [
                        html.H4("P&L Summary (Year 0)", style={"marginTop": "30px"}),
                        html.Div(id="pl_table", children=default_pl_table),
                    ],
                    className="six columns",
                ),
                html.Div(
                    [
                        html.H4("Balance Sheet Summary (Year 0)", style={"marginTop": "30px"}),
                        html.Div(id="bs_table", children=default_bs_section),
                    ],
                    className="six columns",
                ),
            ],
        ),
    ],
    style={"margin": "20px"},
)


# -----------------------------------------------------------
# 6. Callback：上传文件时才更新（不上传就用默认图）
# -----------------------------------------------------------

@app.callback(
    [
        Output("rev_graph", "figure"),
        Output("pm_graph", "figure"),
        Output("cumrev_graph", "figure"),
        Output("exp_graph", "figure"),
        Output("perf_table", "children"),
        Output("is_table", "children"),
        Output("pl_table", "children"),
        Output("bs_table", "children"),
        Output("upload-status", "children"),
    ],
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")],
)
def update_dashboard(contents, filename):
    if contents is None:
        revenue_df, expenses_df, budget, bs = get_default_data()
        status = "Using built-in sample data (no file uploaded)."
    else:
        try:
            revenue_df, expenses_df, budget, bs = parse_contents(contents, filename)
            status = f"File '{filename}' uploaded and parsed successfully."
        except Exception as e:
            revenue_df, expenses_df, budget, bs = get_default_data()
            status = (
                f"Failed to parse uploaded file '{filename}': {e}. "
                "Falling back to built-in sample data."
            )

    fig_rev = build_business_unit_revenue_figure(revenue_df)
    fig_pm = build_profit_margin_figure(revenue_df)
    fig_cum = build_cumulative_revenue_figure(revenue_df)
    fig_exp = build_expenses_figure(expenses_df)
    perf_section = build_performance_summary_section(revenue_df, expenses_df)
    is_table = build_income_statement_table(revenue_df, expenses_df, budget)
    pl_table = build_pl_summary_table(revenue_df, expenses_df)
    bs_section = build_balance_sheet_section(bs)

    return (
        fig_rev,
        fig_pm,
        fig_cum,
        fig_exp,
        perf_section,
        is_table,
        pl_table,
        bs_section,
        status,
    )


# -----------------------------------------------------------
# 7. 入口（Dash 3 用 app.run）
# -----------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
