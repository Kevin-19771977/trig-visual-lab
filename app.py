import math
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# =========================================================
# 三角函數視覺化教學系統
# Trigonometric Functions Visual Learning System
# =========================================================

st.set_page_config(
    page_title="三角函數視覺化教學系統",
    page_icon="📐",
    layout="wide"
)

EPS = 1e-10


def deg_to_rad(theta_deg: float) -> float:
    return math.radians(theta_deg)


def normalize_degrees(theta_deg: float) -> float:
    return theta_deg % 360


def clean_num(x: float, digits: int = 6) -> str:
    if abs(x) < EPS:
        x = 0.0
    return f"{x:.{digits}f}"


def safe_div(num: float, den: float):
    if abs(den) < EPS:
        return None
    return num / den


def value_text(x):
    if x is None:
        return "無定義"
    return clean_num(x)


def trig_values(theta_deg: float):
    r = deg_to_rad(theta_deg)
    s = math.sin(r)
    c = math.cos(r)
    t = safe_div(s, c)
    cot = safe_div(c, s)
    sec = safe_div(1, c)
    csc = safe_div(1, s)
    return {
        "sin θ": s,
        "cos θ": c,
        "tan θ": t,
        "cot θ": cot,
        "sec θ": sec,
        "csc θ": csc,
    }


def quadrant(theta_norm: float) -> str:
    if abs(theta_norm - 0) < EPS:
        return "正 x 軸"
    if abs(theta_norm - 90) < EPS:
        return "正 y 軸"
    if abs(theta_norm - 180) < EPS:
        return "負 x 軸"
    if abs(theta_norm - 270) < EPS:
        return "負 y 軸"
    if 0 < theta_norm < 90:
        return "第一象限"
    if 90 < theta_norm < 180:
        return "第二象限"
    if 180 < theta_norm < 270:
        return "第三象限"
    return "第四象限"


def reference_angle(theta_norm: float) -> float:
    if theta_norm <= 90:
        return theta_norm
    if theta_norm <= 180:
        return 180 - theta_norm
    if theta_norm <= 270:
        return theta_norm - 180
    return 360 - theta_norm


def exact_special_values(angle: int):
    values = {
        0:   ("0", "1", "0"),
        30:  ("1/2", "√3/2", "√3/3"),
        45:  ("√2/2", "√2/2", "1"),
        60:  ("√3/2", "1/2", "√3"),
        90:  ("1", "0", "無定義"),
        120: ("√3/2", "-1/2", "-√3"),
        135: ("√2/2", "-√2/2", "-1"),
        150: ("1/2", "-√3/2", "-√3/3"),
        180: ("0", "-1", "0"),
        210: ("-1/2", "-√3/2", "√3/3"),
        225: ("-√2/2", "-√2/2", "1"),
        240: ("-√3/2", "-1/2", "√3"),
        270: ("-1", "0", "無定義"),
        300: ("-√3/2", "1/2", "-√3"),
        315: ("-√2/2", "√2/2", "-1"),
        330: ("-1/2", "√3/2", "-√3/3"),
        360: ("0", "1", "0"),
    }
    return values.get(angle, ("", "", ""))


def draw_right_triangle(theta_deg: float, hyp: float, focus: str = "sin"):
    theta_rad = deg_to_rad(theta_deg)
    adjacent = hyp * math.cos(theta_rad)
    opposite = hyp * math.sin(theta_rad)

    if abs(adjacent) < EPS:
        adjacent = 0.0
    if abs(opposite) < EPS:
        opposite = 0.0

    colors = {
        "hypotenuse": "#f4a7b9",  # 粉紅色
        "opposite": "#a7d8f0",    # 粉藍色
        "adjacent": "#b8e6c1",    # 粉綠色
    }

    focus_sides = {
        "sin": {"opposite", "hypotenuse"},
        "cos": {"adjacent", "hypotenuse"},
        "tan": {"opposite", "adjacent"},
    }.get(focus, set())

    def side_width(side_name: str) -> float:
        return 6 if side_name in focus_sides else 3.2

    fig, ax = plt.subplots(figsize=(5.2, 4.4))

    # 三條邊分別以固定顏色呈現
    ax.plot([0, adjacent], [0, 0],
            color=colors["adjacent"], linewidth=side_width("adjacent"), solid_capstyle="round")
    ax.plot([adjacent, adjacent], [0, opposite],
            color=colors["opposite"], linewidth=side_width("opposite"), solid_capstyle="round")
    ax.plot([0, adjacent], [0, opposite],
            color=colors["hypotenuse"], linewidth=side_width("hypotenuse"), solid_capstyle="round")

    ax.scatter([0, adjacent, adjacent], [0, 0, opposite], s=45)

    # 直角標記
    if adjacent > EPS and opposite > EPS:
        size = min(adjacent, opposite) * 0.13
        ax.plot([adjacent - size, adjacent - size, adjacent],
                [0, size, size], color="gray", linewidth=1.6)

    # 角度弧線
    arc_r = max(min(hyp * 0.22, 1.0), 0.35)
    if theta_deg > EPS:
        arc = np.linspace(0, theta_rad, 120)
        ax.plot(arc_r * np.cos(arc), arc_r * np.sin(arc), color="gray", linewidth=2)
    ax.text(arc_r * 1.12, max(arc_r * 0.18, 0.12), f"{theta_deg:.1f}°", fontsize=10)

    # 邊長標示
    ax.text(max(adjacent / 2, 0.05), -0.42, f"鄰邊 = {adjacent:.2f}",
            ha="center", fontsize=10)
    ax.text(adjacent + 0.18, max(opposite / 2, 0.08), f"對邊 = {opposite:.2f}",
            va="center", fontsize=10)
    ax.text(max(adjacent / 2 - 0.35, 0.05), max(opposite / 2 + 0.25, 0.25),
            f"斜邊 = {hyp:.2f}", fontsize=10)

    focus_title = {
        "sin": "sin θ = 對邊 / 斜邊",
        "cos": "cos θ = 鄰邊 / 斜邊",
        "tan": "tan θ = 對邊 / 鄰邊",
    }.get(focus, "Right Triangle")
    ax.set_title(focus_title)

    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.25)
    ax.set_xlim(-0.6, max(adjacent + 1.5, 3.5))
    ax.set_ylim(-0.75, max(opposite + 1.25, 3.2))
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return fig, adjacent, opposite


def draw_similar_triangles(theta_deg: float):
    theta_rad = deg_to_rad(theta_deg)
    hyp_list = [2.5, 4.0, 5.5]
    fig, ax = plt.subplots(figsize=(6.2, 4.8))

    for hyp in hyp_list:
        adj = hyp * math.cos(theta_rad)
        opp = hyp * math.sin(theta_rad)
        ax.plot([0, adj, adj, 0], [0, 0, opp, 0], linewidth=2.5)
        ax.scatter([adj], [opp], s=35)
        ax.text(adj + 0.08, opp + 0.08, f"h={hyp:.1f}", fontsize=10)

    ax.set_title("Similar Right Triangles")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    max_adj = max(h * math.cos(theta_rad) for h in hyp_list)
    max_opp = max(h * math.sin(theta_rad) for h in hyp_list)
    ax.set_xlim(-0.5, max_adj + 1.2)
    ax.set_ylim(-0.5, max_opp + 1.2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return fig, hyp_list


def draw_unit_circle(theta_deg: float):
    theta_norm = normalize_degrees(theta_deg)
    theta_rad = deg_to_rad(theta_norm)
    x = math.cos(theta_rad)
    y = math.sin(theta_rad)

    fig, ax = plt.subplots(figsize=(6.2, 6.2))
    t = np.linspace(0, 2 * np.pi, 700)
    ax.plot(np.cos(t), np.sin(t), linewidth=2.2)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    ax.plot([0, x], [0, y], linewidth=3)
    ax.scatter([x], [y], s=80)
    ax.plot([x, x], [0, y], linestyle="--", linewidth=1.3)
    ax.plot([0, x], [y, y], linestyle="--", linewidth=1.3)

    arc_r = 0.32
    if theta_norm == 0:
        arc = np.array([0])
    else:
        arc = np.linspace(0, theta_rad, 200)
    ax.plot(arc_r * np.cos(arc), arc_r * np.sin(arc), linewidth=2)

    ax.text(x + 0.04, y + 0.04, f"P({x:.3f}, {y:.3f})", fontsize=11)
    ax.text(0.37, 0.05, f"{theta_norm:.1f}°", fontsize=11)
    ax.set_title("Unit Circle and Terminal Side")
    ax.set_xlabel("x = cos θ")
    ax.set_ylabel("y = sin θ")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.grid(True, alpha=0.35)
    return fig


def draw_basic_trig_graph(theta_deg: float, show_tan: bool = True):
    xs = np.linspace(-720, 720, 2800)
    rad = np.radians(xs)
    theta_display = ((theta_deg + 720) % 1440) - 720
    theta_rad = math.radians(theta_display)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(xs, np.sin(rad), label="sin x", linewidth=2)
    ax.plot(xs, np.cos(rad), label="cos x", linewidth=2)

    if show_tan:
        ty = np.tan(rad)
        ty[np.abs(ty) > 8] = np.nan
        ax.plot(xs, ty, label="tan x", linewidth=1.8)

    ax.axvline(theta_display, linestyle="--", linewidth=2)
    ax.scatter([theta_display], [math.sin(theta_rad)], s=50)
    ax.scatter([theta_display], [math.cos(theta_rad)], s=50)

    if show_tan and abs(math.cos(theta_rad)) > EPS:
        tv = math.tan(theta_rad)
        if abs(tv) <= 8:
            ax.scatter([theta_display], [tv], s=50)

    ax.set_title("Basic Trigonometric Graphs")
    ax.set_xlabel("x degrees")
    ax.set_ylabel("value")
    ax.set_xlim(-720, 720)
    ax.set_ylim(-8.5 if show_tan else -1.3, 8.5 if show_tan else 1.3)
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig


def trig_func_values(kind: str, x_deg_array):
    r = np.radians(x_deg_array)
    if kind == "sin":
        return np.sin(r)
    if kind == "cos":
        return np.cos(r)
    y = np.tan(r)
    y[np.abs(y) > 10] = np.nan
    return y


def draw_transformed_graph(kind: str, A: float, B: float, C: float, D: float):
    xs = np.linspace(-720, 720, 4000)
    base = trig_func_values(kind, xs)
    transformed_input = B * (xs - C)
    trans = A * trig_func_values(kind, transformed_input) + D

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(xs, base, label=f"original y={kind}(x)", linewidth=2)
    ax.plot(xs, trans, label=f"transformed y=A{kind}(B(x-C))+D", linewidth=2.3)
    ax.axhline(D, linestyle="--", linewidth=1.5, label="midline y=D")
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    ax.set_title("Stretch, Compression, Reflection, and Translation")
    ax.set_xlabel("x degrees")
    ax.set_ylabel("y")
    ax.set_xlim(-720, 720)
    y_min, y_max = -max(6, abs(D) + abs(A) + 2), max(6, abs(D) + abs(A) + 2)
    if kind == "tan":
        y_min, y_max = -10, 10
    ax.set_ylim(y_min, y_max)
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig


st.title("📐 三角函數視覺化教學系統")
st.caption("從直角三角形三角比出發，逐步銜接廣義角、單位圓、三角函數圖形、圖形伸縮平移與基本關係式。")

with st.expander("📘 平台教學主軸", expanded=True):
    st.markdown(
        """
        本平台的學習順序是：

        **三角比 → 相似三角形 → 廣義角 → 單位圓 → 特殊角 → 三角函數圖形 → 伸縮平移 → 基本關係式**

        教學上建議不要一開始就要求學生背公式，而是先讓學生看見：
        1. 三角比來自直角三角形的邊長比例；
        2. 當斜邊固定為 1 時，三角比自然連結到單位圓；
        3. 單位圓上的座標 \(P(\\cos\theta,\\sin\theta)\) 可以延伸到廣義角；
        4. 三角函數圖形則是角度連續變化時，函數值形成的週期圖形。
        """
    )


tabs = st.tabs([
    "0 三角比入門",
    "1 相似三角形",
    "2 廣義角與同界角",
    "3 單位圓與六個三角函數",
    "4 特殊角",
    "5 基本圖形",
    "6 伸縮平移",
    "7 基本關係式",
    "8 教學任務與引導"
])

with tabs[0]:
    st.header("三角比的定義")
    col_ctrl, col_info = st.columns([0.9, 1.1])

    with col_ctrl:
        theta0 = st.slider("角度 θ（度）", 0.0, 90.0, 30.0, 1.0, key="theta0")
        hyp0 = st.slider("斜邊長度", 1.0, 10.0, 5.0, 0.5, key="hyp0")
        st.markdown("#### 三角比定義")
        st.latex(r"\sin\theta=\frac{\text{對邊}}{\text{斜邊}}")
        st.latex(r"\cos\theta=\frac{\text{鄰邊}}{\text{斜邊}}")
        st.latex(r"\tan\theta=\frac{\text{對邊}}{\text{鄰邊}}")

    theta0_rad = deg_to_rad(theta0)
    adj = hyp0 * math.cos(theta0_rad)
    opp = hyp0 * math.sin(theta0_rad)

    if abs(adj) < EPS:
        adj = 0.0
    if abs(opp) < EPS:
        opp = 0.0

    sin0 = safe_div(opp, hyp0)
    cos0 = safe_div(adj, hyp0)
    tan0 = safe_div(opp, adj)

    with col_info:
        st.subheader("如何從圖形理解 sin、cos、tan？")
        st.markdown(
            """
            三角比的重點不是先背公式，而是看懂「角 θ」和三條邊的關係。  
            下面三個直角三角形的角度、大小與邊長完全相同，只是分別強調不同的比值。
            """
        )
        st.markdown(
            """
            - 粉紅色：斜邊  
            - 粉藍色：對邊  
            - 粉綠色：鄰邊  
            """
        )

    tri_col1, tri_col2, tri_col3 = st.columns(3)

    with tri_col1:
        fig_sin, _, _ = draw_right_triangle(theta0, hyp0, focus="sin")
        st.pyplot(fig_sin, use_container_width=True)
        st.latex(r"\sin\theta=\frac{\text{對邊}}{\text{斜邊}}")
        st.write(f"sin θ = {opp:.2f} / {hyp0:.2f} = **{value_text(sin0)}**")

    with tri_col2:
        fig_cos, _, _ = draw_right_triangle(theta0, hyp0, focus="cos")
        st.pyplot(fig_cos, use_container_width=True)
        st.latex(r"\cos\theta=\frac{\text{鄰邊}}{\text{斜邊}}")
        st.write(f"cos θ = {adj:.2f} / {hyp0:.2f} = **{value_text(cos0)}**")

    with tri_col3:
        fig_tan, _, _ = draw_right_triangle(theta0, hyp0, focus="tan")
        st.pyplot(fig_tan, use_container_width=True)
        st.latex(r"\tan\theta=\frac{\text{對邊}}{\text{鄰邊}}")
        st.write(f"tan θ = {opp:.2f} / {adj:.2f} = **{value_text(tan0)}**")

    st.subheader("即時計算")
    df = pd.DataFrame({
        "項目": ["對邊", "鄰邊", "斜邊", "sin θ", "cos θ", "tan θ"],
        "數值": [
            clean_num(opp),
            clean_num(adj),
            clean_num(hyp0),
            value_text(sin0),
            value_text(cos0),
            value_text(tan0),
        ],
        "意義": [
            "角 θ 對面的邊",
            "靠近角 θ、但不是斜邊的邊",
            "直角對面的最長邊",
            "對邊 / 斜邊",
            "鄰邊 / 斜邊",
            "對邊 / 鄰邊；當鄰邊為 0 時無定義"
        ]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info("教學重點：同一個直角三角形可以同時看出 sin、cos、tan；差別在於我們拿哪兩條邊來做比值。")


with tabs[1]:
    st.header("模組 1：三角比與相似三角形")
    col_a, col_b = st.columns([1.1, 1])

    with col_a:
        theta1 = st.slider("固定角度 θ（度）", 10.0, 80.0, 36.0, 1.0, key="theta1")
        fig, hyp_list = draw_similar_triangles(theta1)
        st.pyplot(fig, use_container_width=True)

    with col_b:
        rows = []
        for hyp in hyp_list:
            adj = hyp * math.cos(deg_to_rad(theta1))
            opp = hyp * math.sin(deg_to_rad(theta1))
            rows.append({
                "斜邊": clean_num(hyp),
                "對邊": clean_num(opp),
                "鄰邊": clean_num(adj),
                "對邊/斜邊": clean_num(opp / hyp),
                "鄰邊/斜邊": clean_num(adj / hyp),
                "對邊/鄰邊": clean_num(opp / adj)
            })
        st.subheader("相似三角形的比例")
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.success("結論：角度固定時，即使三角形放大或縮小，三角比仍然相同。")
        st.markdown("教師可以引導學生觀察：**邊長變了，但比值沒有變。** 這正是三角比可以成為函數的前置概念。")

with tabs[2]:
    st.header("模組 2：廣義角與同界角")
    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        theta2 = st.number_input("輸入任意廣義角 θ（度）", min_value=-10000.0, max_value=10000.0, value=390.0, step=15.0, key="theta2")
        st.pyplot(draw_unit_circle(theta2), use_container_width=True)

    with col_b:
        norm2 = normalize_degrees(theta2)
        st.metric("原始角度 θ", f"{theta2:.6g}°")
        st.metric("0° 到 360° 的同界角", f"{norm2:.6g}°")
        st.metric("所在位置", quadrant(norm2))
        st.metric("參考角", f"{reference_angle(norm2):.6g}°")
        st.markdown("#### 同界角公式")
        st.latex(r"\theta_{\text{同界}}=\theta+360^\circ k,\quad k\in\mathbb{Z}")
        k_values = list(range(-3, 4))
        rows = []
        for k in k_values:
            rows.append({"k": k, "同界角": f"{norm2 + 360 * k:.6g}°", "終邊是否相同": "是"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.info("只要終邊相同，三角函數值就相同。")

with tabs[3]:
    st.header("模組 3：單位圓與六個三角函數")
    col_a, col_b = st.columns([1.05, 1])
    with col_a:
        theta3 = st.slider("角度 θ（度）", -720.0, 720.0, 150.0, 1.0, key="theta3")
        st.pyplot(draw_unit_circle(theta3), use_container_width=True)

    with col_b:
        norm3 = normalize_degrees(theta3)
        vals = trig_values(norm3)
        x = vals["cos θ"]
        y = vals["sin θ"]
        st.subheader("角度與座標")
        st.write(f"同界角：**{norm3:.3f}°**")
        st.write(f"位置：**{quadrant(norm3)}**")
        st.write(f"參考角：**{reference_angle(norm3):.3f}°**")
        st.latex(r"P(\cos\theta,\sin\theta)")
        st.write(f"單位圓終點：P = ({x:.6f}, {y:.6f})")
        rows = []
        for name, val in vals.items():
            meaning = {
                "sin θ": "單位圓終點的 y 座標",
                "cos θ": "單位圓終點的 x 座標",
                "tan θ": "sin θ / cos θ，也就是 y / x",
                "cot θ": "cos θ / sin θ，也就是 x / y",
                "sec θ": "1 / cos θ",
                "csc θ": "1 / sin θ",
            }[name]
            rows.append({"三角函數": name, "數值": value_text(val), "意義": meaning})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with tabs[4]:
    st.header("模組 4：特殊角三角函數值")
    special_angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
    angle4 = st.selectbox("選擇特殊角", special_angles, index=1, key="angle4")
    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        st.pyplot(draw_unit_circle(angle4), use_container_width=True)
    with col_b:
        s_exact, c_exact, t_exact = exact_special_values(angle4)
        vals = trig_values(angle4)
        df = pd.DataFrame({
            "三角函數": ["sin θ", "cos θ", "tan θ"],
            "精確值": [s_exact, c_exact, t_exact],
            "小數值": [value_text(vals["sin θ"]), value_text(vals["cos θ"]), value_text(vals["tan θ"])]
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("#### 教學提醒")
        st.write("特殊角不建議只用背誦。可以先判斷參考角，再由象限決定正負號。")
        st.write(f"目前角度 {angle4}° 的位置：**{quadrant(normalize_degrees(angle4))}**")

with tabs[5]:
    st.header("模組 5：三角函數基本圖形")
    col_a, col_b = st.columns([0.85, 1.15])
    with col_a:
        theta5 = st.slider("標示目前角度 θ（度）", -720.0, 720.0, 60.0, 1.0, key="theta5")
        show_tan5 = st.checkbox("顯示 tan x", value=True, key="show_tan5")
        st.markdown("#### 基本觀念")
        st.write("sin 和 cos 的圖形都具有週期性，且函數值介於 -1 到 1。")
        st.latex(r"-1\leq \sin x \leq 1,\quad -1\leq \cos x \leq 1")
        st.write("tan 的圖形有無定義位置，因此會出現垂直漸近線。")
    with col_b:
        st.pyplot(draw_basic_trig_graph(theta5, show_tan5), use_container_width=True)

with tabs[6]:
    st.header("模組 6：三角函數圖形的伸縮與平移")
    st.latex(r"f(x)=A\sin(B(x-C))+D")
    st.write("也可以切換成 cos 或 tan。這裡的 x 以「度」為單位。")
    col_ctrl, col_graph, col_info = st.columns([0.9, 1.35, 1.0])
    with col_ctrl:
        kind6 = st.radio("選擇函數", ["sin", "cos", "tan"], horizontal=True, key="kind6")
        A6 = st.slider("A：上下伸縮／反射", -5.0, 5.0, 1.0, 0.1, key="A6")
        B6 = st.slider("B：週期壓縮或拉長", 0.1, 5.0, 1.0, 0.1, key="B6")
        C6 = st.slider("C：水平平移（度）", -360.0, 360.0, 0.0, 5.0, key="C6")
        D6 = st.slider("D：垂直平移", -5.0, 5.0, 0.0, 0.1, key="D6")
    with col_graph:
        st.pyplot(draw_transformed_graph(kind6, A6, B6, C6, D6), use_container_width=True)
    with col_info:
        st.subheader("參數意義")
        if kind6 in ["sin", "cos"]:
            period = 360 / abs(B6)
            st.metric("振幅", f"|A| = {abs(A6):.3f}")
            st.metric("週期", f"{period:.3f}°")
            st.metric("中線", f"y = {D6:.3f}")
            st.metric("最大值", f"{D6 + abs(A6):.3f}")
            st.metric("最小值", f"{D6 - abs(A6):.3f}")
        else:
            period = 180 / abs(B6)
            st.metric("tan 的週期", f"{period:.3f}°")
            st.metric("垂直平移", f"D = {D6:.3f}")
            st.warning("tan 沒有振幅與最大最小值，因為它的函數值沒有上下界。")
        st.markdown("""
        - \(A\)：控制上下伸縮，負值會造成上下反射  
        - \(B\)：控制週期，越大圖形越密  
        - \(C\)：控制水平平移，\(x-C\) 表示向右移 \(C\)  
        - \(D\)：控制垂直平移，也就是中線位置  
        """)

with tabs[7]:
    st.header("模組 7：平方關係、商數關係與餘角關係")
    theta7 = st.slider("選擇角度 θ（度）", 0.0, 90.0, 30.0, 1.0, key="theta7")
    vals7 = trig_values(theta7)
    comp = 90 - theta7
    vals_comp = trig_values(comp)
    sub1, sub2, sub3 = st.tabs(["平方關係", "商數關係", "餘角關係"])

    with sub1:
        st.subheader("平方關係")
        st.latex(r"\sin^2\theta+\cos^2\theta=1")
        s = vals7["sin θ"]
        c = vals7["cos θ"]
        st.write(f"目前 θ = {theta7:.1f}°")
        st.write(f"sin²θ + cos²θ = {s**2:.6f} + {c**2:.6f} = **{s**2 + c**2:.6f}**")
        st.success("這個關係來自單位圓方程式：x² + y² = 1。")
        sec = vals7["sec θ"]
        tan = vals7["tan θ"]
        csc = vals7["csc θ"]
        cot = vals7["cot θ"]
        rows = [{"關係式": "sin²θ + cos²θ = 1", "驗證值": clean_num(s**2 + c**2), "是否成立": "成立"}]
        if tan is not None and sec is not None:
            rows.append({"關係式": "1 + tan²θ = sec²θ", "驗證值": f"{clean_num(1 + tan**2)} ； sec²θ={clean_num(sec**2)}", "是否成立": "成立"})
        else:
            rows.append({"關係式": "1 + tan²θ = sec²θ", "驗證值": "此角度 tan 或 sec 無定義", "是否成立": "不適用"})
        if cot is not None and csc is not None:
            rows.append({"關係式": "1 + cot²θ = csc²θ", "驗證值": f"{clean_num(1 + cot**2)} ； csc²θ={clean_num(csc**2)}", "是否成立": "成立"})
        else:
            rows.append({"關係式": "1 + cot²θ = csc²θ", "驗證值": "此角度 cot 或 csc 無定義", "是否成立": "不適用"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with sub2:
        st.subheader("商數關係")
        st.latex(r"\tan\theta=\frac{\sin\theta}{\cos\theta}")
        st.latex(r"\cot\theta=\frac{\cos\theta}{\sin\theta}")
        tan_from_sc = safe_div(vals7["sin θ"], vals7["cos θ"])
        cot_from_cs = safe_div(vals7["cos θ"], vals7["sin θ"])
        df = pd.DataFrame({
            "項目": ["tan θ", "sin θ / cos θ", "cot θ", "cos θ / sin θ"],
            "數值": [value_text(vals7["tan θ"]), value_text(tan_from_sc), value_text(vals7["cot θ"]), value_text(cot_from_cs)],
            "說明": ["正切函數值", "用 sin 與 cos 計算 tan", "餘切函數值", "用 cos 與 sin 計算 cot"]
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.info("當分母為 0 時，對應的商數關係會無定義。")

    with sub3:
        st.subheader("餘角關係")
        st.latex(r"\sin(90^\circ-\theta)=\cos\theta")
        st.latex(r"\cos(90^\circ-\theta)=\sin\theta")
        st.latex(r"\tan(90^\circ-\theta)=\cot\theta")
        df = pd.DataFrame({
            "比較項目": [
                "sin(90° − θ) 與 cos θ",
                "cos(90° − θ) 與 sin θ",
                "tan(90° − θ) 與 cot θ",
                "cot(90° − θ) 與 tan θ",
                "sec(90° − θ) 與 csc θ",
                "csc(90° − θ) 與 sec θ",
            ],
            "左側數值": [
                value_text(vals_comp["sin θ"]),
                value_text(vals_comp["cos θ"]),
                value_text(vals_comp["tan θ"]),
                value_text(vals_comp["cot θ"]),
                value_text(vals_comp["sec θ"]),
                value_text(vals_comp["csc θ"]),
            ],
            "右側數值": [
                value_text(vals7["cos θ"]),
                value_text(vals7["sin θ"]),
                value_text(vals7["cot θ"]),
                value_text(vals7["tan θ"]),
                value_text(vals7["csc θ"]),
                value_text(vals7["sec θ"]),
            ],
            "是否對應": ["是", "是", "是", "是", "是", "是"]
        })
        st.write(f"目前 θ = {theta7:.1f}°，餘角 = {comp:.1f}°")
        st.dataframe(df, use_container_width=True, hide_index=True)

with tabs[8]:
    st.header("模組 8：學生探索任務與教師引導")
    task = st.selectbox(
        "選擇教學任務",
        [
            "任務 1：認識對邊、鄰邊、斜邊",
            "任務 2：觀察角度固定時比值固定",
            "任務 3：從三角比連到單位圓",
            "任務 4：觀察同界角",
            "任務 5：觀察象限與正負號",
            "任務 6：觀察圖形伸縮平移",
            "任務 7：驗證三角函數基本關係式",
        ]
    )
    st.subheader(task)
    task_text = {
        "任務 1：認識對邊、鄰邊、斜邊": """
**學生任務**  
1. 在直角三角形中找出斜邊、對邊、鄰邊。  
2. 改變角度 θ，觀察對邊和鄰邊如何改變。  
3. 用自己的話說明：為什麼斜邊一定是最長邊？

**教師引導語**  
「三角比的第一步不是背 sin、cos、tan，而是先看懂每一條邊跟角 θ 的關係。」
""",
        "任務 2：觀察角度固定時比值固定": """
**學生任務**  
1. 固定角度 θ，例如 30°。  
2. 改變三角形大小。  
3. 記錄 sin θ、cos θ、tan θ 是否改變。

**教師引導語**  
「如果角度沒有變，三角形只是放大或縮小，形狀其實相同，所以邊長比值會保持一致。」
""",
        "任務 3：從三角比連到單位圓": """
**學生任務**  
1. 先觀察直角三角形中的 sin θ = 對邊 / 斜邊。  
2. 將斜邊想成半徑。  
3. 當斜邊固定為 1 時，sin θ 就等於 y 座標，cos θ 就等於 x 座標。

**教師引導語**  
「單位圓不是新的公式，而是把斜邊固定成 1 的直角三角形概念延伸。」
""",
        "任務 4：觀察同界角": """
**學生任務**  
請比較 30°、390°、-330° 的終邊位置與三角函數值。

**觀察問題**  
1. 它們的終邊是否相同？  
2. 它們的 sin、cos、tan 是否相同？  
3. 你可以用「多轉一圈」或「少轉一圈」來說明嗎？

**教師引導語**  
「角度數字不同，不代表終邊不同。三角函數值真正看的是終邊位置。」
""",
        "任務 5：觀察象限與正負號": """
**學生任務**  
請比較 45°、135°、225°、315° 的 sin、cos、tan 正負號。

**教師引導語**  
「sin 是 y 座標，所以看上下；cos 是 x 座標，所以看左右；tan 是 y/x，所以看兩者的正負組合。」
""",
        "任務 6：觀察圖形伸縮平移": """
**學生任務**  
1. 只改變 A，觀察圖形變高或變矮。  
2. 只改變 B，觀察週期變短或變長。  
3. 只改變 C，觀察圖形左右平移。  
4. 只改變 D，觀察中線上下移動。

**教師引導語**  
「A 管高度，B 管週期，C 管左右位置，D 管上下位置。」
""",
        "任務 7：驗證三角函數基本關係式": """
**學生任務**  
1. 選擇不同角度 θ。  
2. 驗證 sin²θ + cos²θ 是否等於 1。  
3. 驗證 tan θ 是否等於 sin θ / cos θ。  
4. 比較 θ 與 90° − θ 的三角函數值。

**教師引導語**  
「三角函數不是一堆分開的公式，它們彼此之間有固定的結構關係。」
""",
    }
    st.markdown(task_text[task])
    st.markdown("---")
    st.subheader("建議課堂流程")
    st.markdown(
        """
        1. **先從直角三角形開始**：讓學生分辨對邊、鄰邊、斜邊。  
        2. **再進入相似三角形**：讓學生看出角度固定時，比值固定。  
        3. **接到單位圓**：說明斜邊固定為 1 後，sin 與 cos 變成座標。  
        4. **引入廣義角**：把角度從銳角擴展到任意角。  
        5. **觀察圖形**：讓角度連續變化，形成 sin、cos、tan 圖形。  
        6. **加入伸縮平移**：理解參數如何改變圖形。  
        7. **最後整理關係式**：用數值驗證平方、商數與餘角關係。  
        """
    )

st.markdown("---")
st.caption("執行方式：streamlit run app.py")
