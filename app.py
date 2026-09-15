import html
import sqlite3

import altair as alt
import pandas as pd
import streamlit as st


alt.theme.enable("opaque")


# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="TCP Client Data & Outcomes",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# GLOBAL STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --ink: #18324A;
            --muted: #6B7C8B;
            --line: #E5EDF2;
            --panel: #FFFFFF;
            --canvas: #F6F8FB;
            --teal: #08A88D;
            --teal-dark: #078A76;
            --teal-soft: #E4F7F2;
            --agency-yellow: #FDC45A;
            --agency-blue: #73AEDD;
            --agency-lavender: #9292CD;
        }

        html, body, [class*="css"] {
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 0%, rgba(20, 184, 166, 0.06), transparent 30rem),
                radial-gradient(circle at 90% 8%, rgba(15, 118, 110, 0.07), transparent 26rem),
                var(--canvas);
            color: var(--ink);
        }

        .block-container {
            max-width: 1480px;
            padding-top: 1.4rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: -0.02em;
        }

        h1 {
            font-size: 2.05rem;
            font-weight: 800;
        }

        h2 {
            font-size: 1.45rem;
            font-weight: 750;
        }

        h3 {
            font-size: 1.05rem;
            font-weight: 750;
        }

        [data-testid="stMainBlockContainer"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, #18324A 0%, #17626A 48%, #08A88D 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] .block-container {
            padding: 1.25rem 1rem 2rem;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.16);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: rgba(255, 255, 255, 0.82);
        }

        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
            color: #C8E9E5;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 0.38rem 0.55rem;
            transition: background 150ms ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background: rgba(255, 255, 255, 0.16);
            color: #FFFFFF;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: rgba(255, 255, 255, 0.10);
            border-color: rgba(255, 255, 255, 0.20);
            color: #FFFFFF;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] svg {
            fill: rgba(255, 255, 255, 0.8);
        }

        [data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 16px 18px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.045);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: var(--ink);
            font-weight: 800;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 16px;
            overflow: hidden;
            background: var(--panel);
            color: var(--ink);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.035);
        }

        [data-testid="stDataFrame"] [role="grid"] {
            font-size: 0.9rem;
        }

        [data-testid="stDataFrame"] [data-testid="stDataFrameResizable"],
        [data-testid="stDataFrame"] .stDataFrameGlideDataEditor,
        [data-testid="stDataFrame"] .dvn-scroller,
        [data-testid="stDataFrame"] .dvn-underlay {
            background: var(--panel);
            color: var(--ink);
        }

        [data-testid="stDataFrame"] [role="row"] {
            color: var(--ink);
        }

        [data-testid="stDataFrame"] [role="columnheader"] {
            background: var(--teal-soft);
            color: var(--teal);
            font-weight: 750;
        }

        [data-testid="stDataFrame"] [role="gridcell"] {
            color: var(--ink);
        }

        [data-testid="stDataFrame"] [data-testid="stElementToolbar"] {
            color: #60707D;
        }

        .data-table-wrap {
            border: 1px solid var(--line);
            border-radius: 16px;
            overflow: hidden;
            background: var(--panel);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.035);
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            color: var(--ink);
            font-size: 0.9rem;
        }

        .data-table th {
            padding: 11px 14px;
            background: var(--teal-soft);
            color: var(--teal);
            text-align: left;
            font-weight: 750;
        }

        .data-table td {
            padding: 11px 14px;
            border-top: 1px solid var(--line);
            color: var(--ink);
        }

        .data-table tr:nth-child(even) td {
            background: #FBFDFC;
        }

        [data-testid="stVegaLiteChart"] {
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 14px;
            background: var(--panel);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.05);
        }

        /* Streamlit's chart data panel relies on a canvas grid that renders blank
           in the embedded browser used for this dashboard. Keep the usable chart
           controls (for example, fullscreen) and hide only that broken action. */
        [data-testid="stElementToolbarButton"]:has(
            button[aria-label="Show data"]
        ) {
            display: none !important;
        }

        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 1px solid var(--line);
            padding-bottom: 0;
        }

        [data-testid="stTabs"] [data-baseweb="tab"] {
            height: auto;
            padding: 0.65rem 1rem;
            background: transparent;
            border-radius: 12px 12px 0 0;
            color: #60707D;
            font-weight: 650;
        }

        [data-testid="stTabs"] [aria-selected="true"] {
            background: var(--panel);
            color: var(--teal);
            box-shadow: inset 0 -3px 0 var(--teal);
        }

        [data-testid="stExpander"] {
            border: 1px solid var(--line);
            border-radius: 14px;
            background: var(--panel);
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.03);
        }

        .brand-lockup {
            padding: 0.2rem 0.1rem 0.8rem;
        }

        .brand-mark {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            margin-bottom: 10px;
            border-radius: 13px;
            background: rgba(255, 255, 255, 0.13);
            border: 1px solid rgba(255, 255, 255, 0.16);
            color: #FFFFFF;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.05em;
        }

        .brand-title {
            color: #FFFFFF;
            font-size: 1.2rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }

        .sidebar-note {
            border: 1px solid rgba(255, 255, 255, 0.14);
            background: rgba(255, 255, 255, 0.07);
            border-radius: 12px;
            padding: 10px 12px;
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.75rem;
            line-height: 1.45;
        }

        .hero-card {
            display: flex;
            align-items: center;
            gap: 18px;
            padding: 22px 24px;
            margin-bottom: 20px;
            border: 1px solid #DFECE9;
            border-radius: 22px;
            background: linear-gradient(135deg, #FFFFFF 0%, #F3FAF8 100%);
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
        }

        .hero-avatar {
            flex: 0 0 auto;
            width: 68px;
            height: 68px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 20px;
            background: linear-gradient(135deg, var(--teal-dark) 0%, var(--teal) 100%);
            color: #FFFFFF;
            font-size: 1.55rem;
            font-weight: 800;
            box-shadow: 0 12px 28px rgba(8, 168, 141, 0.24);
        }

        .hero-kicker {
            color: var(--teal);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.11em;
            text-transform: uppercase;
            margin-bottom: 4px;
        }

        .hero-name {
            color: var(--ink);
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            line-height: 1.15;
        }

        .hero-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }

        .hero-chip {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 10px;
            border-radius: 999px;
            background: #FFFFFF;
            border: 1px solid #E1EDEA;
            color: #48605E;
            font-size: 0.78rem;
            font-weight: 650;
        }

        .metric-card {
            display: flex;
            align-items: center;
            gap: 14px;
            min-height: 116px;
            padding: 18px 16px;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: var(--panel);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.045);
        }

        .metric-icon {
            flex: 0 0 auto;
            width: 46px;
            height: 46px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 14px;
            background: var(--teal-soft);
            color: var(--teal);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.05em;
        }

        .metric-label {
            color: #74838F;
            font-size: 0.7rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--ink);
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            line-height: 1.12;
            margin-top: 4px;
        }

        .metric-sub {
            color: #91A0AC;
            font-size: 0.78rem;
            margin-top: 4px;
        }

        .section-header {
            margin: 10px 0 6px;
        }

        .section-title {
            color: var(--ink);
            font-size: 1.12rem;
            font-weight: 800;
            letter-spacing: -0.015em;
        }

        .section-subtitle {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: 3px;
        }

        .goal-card {
            border: 1px solid var(--line);
            border-radius: 16px;
            background: var(--panel);
            padding: 15px 16px;
            margin-bottom: 12px;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.035);
        }

        .goal-card-top {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
        }

        .goal-title {
            color: var(--ink);
            font-size: 0.95rem;
            font-weight: 750;
            line-height: 1.35;
        }

        .goal-category {
            color: #84939F;
            font-size: 0.75rem;
            margin-top: 7px;
        }

        .goal-progress {
            margin-top: 13px;
            height: 8px;
            border-radius: 999px;
            background: #EEF3F6;
            overflow: hidden;
        }

        .goal-progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--teal-dark), var(--teal));
        }

        .goal-progress-foot {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 7px;
            color: #7A8996;
            font-size: 0.75rem;
            font-weight: 650;
        }

        .status-badge {
            flex: 0 0 auto;
            display: inline-flex;
            align-items: center;
            padding: 4px 9px;
            border-radius: 999px;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            white-space: nowrap;
        }

        .status-active,
        .status-in-progress,
        .status-achieved,
        .status-completed {
            background: #E7F5F1;
            color: var(--teal);
        }

        .status-pending,
        .status-on-hold,
        .status-not-started {
            background: #FFF4D9;
            color: #A66A12;
        }

        .status-discharged,
        .status-inactive,
        .status-closed {
            background: #EEF2F5;
            color: #607080;
        }

        .empty-note {
            padding: 16px;
            border: 1px dashed #D7E3E1;
            border-radius: 14px;
            background: #FAFDFC;
            color: #6D827E;
            font-size: 0.9rem;
        }

        .muted-caption {
            color: #7B8B97;
            font-size: 0.82rem;
            margin-top: 0.2rem;
        }

        .agency-hero {
            padding: 24px 26px;
            margin-bottom: 20px;
            border-radius: 22px;
            color: #FFFFFF;
            background: linear-gradient(135deg, #18324A 0%, #17626A 58%, #08A88D 100%);
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
        }

        .agency-hero-title {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -0.025em;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

conn = sqlite3.connect("evaluation.db")


# ---------------------------------------------------------
# CLIENT LIST
# ---------------------------------------------------------

clients = pd.read_sql_query(
    """
    SELECT
        client_id,
        name,
        admission_date,
        status
    FROM clients
    ORDER BY name;
    """,
    conn,
)

clients["selector_label"] = (
    clients["name"].astype(str)
    + " — "
    + clients["client_id"].astype(str)
    + " — "
    + clients["status"].astype(str)
)
client_labels = clients.set_index("client_id")["selector_label"].to_dict()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
            <div class="brand-mark">TCP</div>
            <div class="brand-title">The Children's Place</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    view = st.radio(
        "Dashboards",
        [
            "Agency Outcomes",
            "Client Overview",
            "Client Outcomes",
        ],
        index=0,
        label_visibility="visible",
    )

    st.divider()

    if view == "Agency Outcomes":
        selected_client_id = int(clients.iloc[0]["client_id"])
    else:
        selected_client_id = st.selectbox(
            "Search Client",
            clients["client_id"].astype(int).tolist(),
            index=None,
            format_func=lambda client_id: client_labels[client_id],
            placeholder="Type a name or client ID...",
        )

    st.divider()

    st.markdown(
        """
        <div class="sidebar-note">
            All client data is fictional.
        </div>
        """,
        unsafe_allow_html=True,
    )


if selected_client_id is None:
    st.title("The Children's Place")
    st.info("Search for a client in the sidebar to view their record.")
    st.stop()


client_id = int(selected_client_id)
client = clients[clients["client_id"] == client_id].iloc[0]


# ---------------------------------------------------------
# LOAD CLIENT DATA
# ---------------------------------------------------------

program_data = pd.read_sql_query(
    """
    SELECT
        p.program_name,
        cp.start_date,
        cp.end_date
    FROM client_programs cp
    JOIN programs p
        ON cp.program_id = p.program_id
    WHERE cp.client_id = ?
    ORDER BY cp.start_date;
    """,
    conn,
    params=(client_id,),
)


caregiver_data = pd.read_sql_query(
    """
    SELECT
        caregiver_name,
        relationship,
        primary_contact
    FROM caregivers
    WHERE client_id = ?
    ORDER BY primary_contact DESC;
    """,
    conn,
    params=(client_id,),
)


attendance_summary = pd.read_sql_query(
    """
    SELECT
        COUNT(*) AS recorded_days,
        SUM(
            CASE
                WHEN ac.counts_as_present = 1
                THEN 1
                ELSE 0
            END
        ) AS present_days
    FROM attendance a
    JOIN attendance_codes ac
        ON a.attendance_code = ac.attendance_code
    WHERE a.client_id = ?;
    """,
    conn,
    params=(client_id,),
)


attendance_detail = pd.read_sql_query(
    """
    SELECT
        a.attendance_date,
        a.attendance_code,
        ac.description,
        ac.category
    FROM attendance a
    JOIN attendance_codes ac
        ON a.attendance_code = ac.attendance_code
    WHERE a.client_id = ?
    ORDER BY a.attendance_date;
    """,
    conn,
    params=(client_id,),
)


meal_summary = pd.read_sql_query(
    """
    SELECT
        meal_type,
        SUM(served) AS meals_served
    FROM meals
    WHERE client_id = ?
    GROUP BY meal_type
    ORDER BY meal_type;
    """,
    conn,
    params=(client_id,),
)


goal_data = pd.read_sql_query(
    """
    SELECT
        goal_text,
        goal_category,
        status,
        progress_percent
    FROM goals
    WHERE client_id = ?
    ORDER BY status, goal_text;
    """,
    conn,
    params=(client_id,),
)


service_summary = pd.read_sql_query(
    """
    SELECT
        service_type,
        COUNT(*) AS service_count,
        SUM(duration_minutes) AS total_minutes
    FROM services
    WHERE client_id = ?
    GROUP BY service_type
    ORDER BY service_type;
    """,
    conn,
    params=(client_id,),
)


gold_data = pd.read_sql_query(
    """
    SELECT
        gd.dimension_code,
        gd.dimension_name,
        gd.domain,
        gp.checkpoint_name,
        gp.checkpoint_number,
        gp.checkpoint_date,
        gcs.score
    FROM gold_checkpoint_scores gcs
    JOIN gold_dimensions gd
        ON gcs.dimension_id = gd.dimension_id
    JOIN gold_checkpoint_periods gp
        ON gcs.checkpoint_id = gp.checkpoint_id
    WHERE gcs.client_id = ?
    ORDER BY
        gd.domain,
        gd.dimension_code,
        gp.checkpoint_number;
    """,
    conn,
    params=(client_id,),
)


clinical_data = pd.read_sql_query(
    """
    SELECT
        at.assessment_name,
        am.measure_name,
        am.improvement_direction,
        aa.assessment_date,
        s.score
    FROM assessment_scores s
    JOIN assessment_administrations aa
        ON s.administration_id = aa.administration_id
    JOIN assessment_measures am
        ON s.measure_id = am.measure_id
    JOIN assessment_types at
        ON aa.assessment_type_id = at.assessment_type_id
    WHERE aa.client_id = ?
    ORDER BY
        at.assessment_name,
        am.measure_name,
        aa.assessment_date;
    """,
    conn,
    params=(client_id,),
)


# ---------------------------------------------------------
# SMALL RENDER HELPERS
# ---------------------------------------------------------

def esc(value):
    return html.escape(str(value))


def initials_for(name):
    parts = str(name).strip().split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def status_class(status):
    normalized = str(status).strip().lower().replace(" ", "-")
    allowed = {
        "active",
        "in-progress",
        "achieved",
        "completed",
        "pending",
        "on-hold",
        "not-started",
        "discharged",
        "inactive",
        "closed",
    }
    return normalized if normalized in allowed else ""


def section_header(title, subtitle=""):
    subtitle_html = (
        f'<div class="section-subtitle">{esc(subtitle)}</div>'
        if subtitle
        else ""
    )
    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-title">{esc(title)}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(column, icon, label, value, sublabel=""):
    icon_html = (
        f'<div class="metric-icon">{esc(icon)}</div>'
        if icon
        else ""
    )
    sublabel_html = (
        f'<div class="metric-sub">{esc(sublabel)}</div>'
        if sublabel
        else ""
    )
    card_html = (
        '<div class="metric-card">'
        f'{icon_html}'
        '<div>'
        f'<div class="metric-label">{esc(label)}</div>'
        f'<div class="metric-value">{esc(value)}</div>'
        f'{sublabel_html}'
        '</div>'
        '</div>'
    )
    column.markdown(card_html, unsafe_allow_html=True)


def render_empty(message):
    st.markdown(
        f'<div class="empty-note">{esc(message)}</div>',
        unsafe_allow_html=True,
    )


def render_table(dataframe):
    """Render tabular data as normal HTML instead of Streamlit's canvas grid.

    The canvas grid can appear as an empty white panel in some embedded/browser
    environments even when its dataframe has rows. HTML keeps the data visible
    and preserves the app's existing visual language.
    """
    table_html = dataframe.to_html(
        index=False,
        escape=True,
        classes="data-table",
        border=0,
    )
    st.markdown(
        f'<div class="data-table-wrap">{table_html}</div>',
        unsafe_allow_html=True,
    )


def render_goal_card(goal):
    progress = max(0, min(100, int(goal["progress_percent"] or 0)))
    status = str(goal["status"] or "Pending")
    category = goal.get("goal_category")
    category_html = ""
    if pd.notna(category):
        category_html = (
            f'<div class="goal-category">Category: {esc(category)}</div>'
        )

    st.markdown(
        f"""
        <div class="goal-card">
            <div class="goal-card-top">
                <div class="goal-title">{esc(goal["goal_text"])}</div>
                <span class="status-badge {status_class(status)}">
                    {esc(status)}
                </span>
            </div>
            {category_html}
            <div class="goal-progress">
                <div class="goal-progress-fill" style="width:{progress}%;"></div>
            </div>
            <div class="goal-progress-foot">
                <span>Progress</span>
                <span>{progress}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("The Children's Place")
status = str(client["status"] or "Unknown")
admission_date = str(client["admission_date"] or "—")

if view != "Agency Outcomes":
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-avatar">{esc(initials_for(client["name"]))}</div>
            <div class="hero-main">
                <div class="hero-kicker">Client Profile</div>
                <div class="hero-name">{esc(client["name"])}</div>
                <div class="hero-meta">
                    <span class="hero-chip">
                        <span class="status-badge {status_class(status)}">{esc(status)}</span>
                    </span>
                    <span class="hero-chip">Admitted {esc(admission_date)}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CLIENT OVERVIEW
# =========================================================

if view == "Client Overview":
    current_program = (
        program_data.iloc[-1]["program_name"]
        if not program_data.empty
        else "No Program"
    )

    recorded_days = int(attendance_summary.iloc[0]["recorded_days"] or 0)
    present_days = int(attendance_summary.iloc[0]["present_days"] or 0)
    attendance_rate = (
        present_days / recorded_days * 100 if recorded_days > 0 else 0
    )

    metric_cols = st.columns(4)
    metric_card(metric_cols[0], "ST", "Status", status, "Current enrollment")
    metric_card(
        metric_cols[1],
        "PR",
        "Current Program",
        current_program,
        "Most recent placement",
    )
    metric_card(
        metric_cols[2],
        "AD",
        "Admission Date",
        admission_date,
        "Initial enrollment",
    )
    metric_card(
        metric_cols[3],
        "AT",
        "Attendance",
        f"{attendance_rate:.1f}%",
        f"{present_days} of {recorded_days} recorded days present",
    )

    st.write("")

    tab_program, tab_goals, tab_attendance = st.tabs(
        [
            "Programs & Caregivers",
            "Goals & Services",
            "Attendance",
        ]
    )

    with tab_program:
        left, right = st.columns(2, gap="large")

        with left:
            section_header(
                "Program History",
                "Program placements over time.",
            )
            if not program_data.empty:
                display_programs = program_data.copy()
                display_programs.columns = [
                    "Program",
                    "Start Date",
                    "End Date",
                ]
                render_table(display_programs)
            else:
                render_empty("No program history available.")

        with right:
            section_header(
                "Caregivers",
                "Primary contacts are shown first.",
            )
            if not caregiver_data.empty:
                render_table(caregiver_data.rename(
                        columns={
                            "caregiver_name": "Caregiver",
                            "relationship": "Relationship",
                            "primary_contact": "Primary Contact",
                        }
                    ))
            else:
                render_empty("No caregiver data available.")

    with tab_goals:
        left, right = st.columns(2, gap="large")

        with left:
            section_header(
                "Active Goals",
                "Progress is shown as a percentage of the plan.",
            )
            if not goal_data.empty:
                for _, goal in goal_data.iterrows():
                    render_goal_card(goal)
            else:
                render_empty("No goals available.")

        with right:
            section_header(
                "Services",
                "Utilization across service types.",
            )
            if not service_summary.empty:
                service_display = service_summary.copy()
                service_display.columns = [
                    "Service",
                    "Count",
                    "Minutes",
                ]
                render_table(service_display)
            else:
                render_empty("No service data available.")

            st.write("")
            section_header("Meals Served", "Meal totals by type.")
            if not meal_summary.empty:
                meal_display = meal_summary.copy()
                meal_display.columns = [
                    "Meal",
                    "Served",
                ]
                render_table(meal_display)
            else:
                render_empty("No meal data available.")

    with tab_attendance:
        section_header(
            "Attendance Detail",
            "Daily attendance codes and categories.",
        )
        if not attendance_detail.empty:
            attendance_display = attendance_detail.copy()
            attendance_display.columns = [
                "Date",
                "Code",
                "Description",
                "Category",
            ]
            render_table(attendance_display)
        else:
            render_empty("No attendance data available.")


# =========================================================
# CLIENT OUTCOMES
# =========================================================

elif view == "Client Outcomes":
    section_header(
        "Classroom Development",
        "Teaching Strategies GOLD checkpoint levels.",
    )

    if gold_data.empty:
        render_empty("No Teaching Strategies GOLD checkpoint data available.")
    else:
        domain_summary = (
            gold_data.groupby(
                [
                    "domain",
                    "checkpoint_name",
                    "checkpoint_number",
                ]
            )["score"]
            .mean()
            .reset_index()
        )

        domain_summary["score"] = domain_summary["score"].round(1)

        domain_chart = (
            alt.Chart(domain_summary)
            .mark_line(
                point=True,
                strokeWidth=3,
            )
            .encode(
                x=alt.X(
                    "checkpoint_number:O",
                    title="Checkpoint",
                    axis=alt.Axis(
                        labelExpr=(
                            "datum.value == 1 ? 'Fall' : "
                            "datum.value == 2 ? 'Winter' : "
                            "datum.value == 3 ? 'Spring' : "
                            "'Summer'"
                        )
                    ),
                ),
                y=alt.Y(
                    "score:Q",
                    title="Average GOLD Level",
                    scale=alt.Scale(domain=[0, 13]),
                ),
                color=alt.Color(
                    "domain:N",
                    title="Development Area",
                    scale=alt.Scale(
                        range=[
                            "#08A88D",
                            "#078A76",
                            "#FDC45A",
                            "#73AEDD",
                            "#9292CD",
                            "#18324A",
                        ]
                    ),
                ),
                tooltip=[
                    "domain",
                    "checkpoint_name",
                    alt.Tooltip("score:Q", format=".1f"),
                ],
            )
            .properties(height=360)
            .configure_axis(
                labelColor="#12263A",
                titleColor="#12263A",
                gridColor="#E5EDF2",
            )
            .configure_legend(
                labelColor="#12263A",
                titleColor="#12263A",
            )
        )

        st.altair_chart(
            domain_chart,
            use_container_width=True,
            theme=None,
        )

        section_header(
            "GOLD Dimension Progress",
            "Explore a single development dimension.",
        )
        selected_dimension = st.selectbox(
            "Select GOLD Dimension",
            gold_data["dimension_name"].unique(),
        )

        dimension_data = gold_data[
            gold_data["dimension_name"] == selected_dimension
        ].copy()

        dimension_chart = (
            alt.Chart(dimension_data)
            .mark_line(
                point=True,
                strokeWidth=3,
                color="#08A88D",
            )
            .encode(
                x=alt.X(
                    "checkpoint_number:O",
                    title="Checkpoint",
                ),
                y=alt.Y(
                    "score:Q",
                    title="Level",
                    scale=alt.Scale(domain=[0, 13]),
                ),
                tooltip=[
                    "checkpoint_name",
                    "score",
                ],
            )
            .properties(height=300)
            .configure_axis(
                labelColor="#12263A",
                titleColor="#12263A",
                gridColor="#E5EDF2",
            )
            .configure_legend(
                labelColor="#12263A",
                titleColor="#12263A",
            )
        )

        st.altair_chart(
            dimension_chart,
            use_container_width=True,
            theme=None,
        )

    st.write("")
    section_header(
        "Clinical Outcomes",
    )

    if clinical_data.empty:
        render_empty("No clinical assessment data available.")
    else:
        assessment_names = clinical_data["assessment_name"].unique()

        if len(assessment_names) == 1:
            assessment_tabs = st.tabs([str(assessment_names[0])])
        else:
            assessment_tabs = st.tabs([str(name) for name in assessment_names])

        for assessment_name, assessment_tab in zip(
            assessment_names, assessment_tabs
        ):
            assessment_subset = clinical_data[
                clinical_data["assessment_name"] == assessment_name
            ]
            measures = assessment_subset["measure_name"].unique()

            with assessment_tab:
                selected_measure = st.selectbox(
                    "Select Measure",
                    measures,
                    key=f"measure_{assessment_name}",
                )

                measure_data = assessment_subset[
                    assessment_subset["measure_name"] == selected_measure
                ].copy()

                measure_data["assessment_date"] = pd.to_datetime(
                    measure_data["assessment_date"]
                )

                baseline = float(measure_data.iloc[0]["score"])
                latest = float(measure_data.iloc[-1]["score"])
                change = latest - baseline
                direction = measure_data.iloc[0]["improvement_direction"]
                improved = (
                    change > 0 if direction == "higher" else change < 0
                )

                change_label = "Improved" if improved else "Declined"

                metric_cols = st.columns(3)
                metric_card(
                    metric_cols[0],
                    "BL",
                    "Baseline",
                    f"{baseline:g}",
                    "First recorded score",
                )
                metric_card(
                    metric_cols[1],
                    "LT",
                    "Latest",
                    f"{latest:g}",
                    "Most recent score",
                )
                metric_card(
                    metric_cols[2],
                    "Δ",
                    "Change",
                    f"{change:+g}",
                    change_label,
                )

                st.write("")

                clinical_chart = (
                    alt.Chart(measure_data)
                    .mark_line(
                        point=True,
                        strokeWidth=3,
                        color="#08A88D",
                    )
                    .encode(
                        x=alt.X(
                            "assessment_date:T",
                            title="Assessment Date",
                        ),
                        y=alt.Y(
                            "score:Q",
                            title="Score",
                        ),
                        tooltip=[
                            alt.Tooltip(
                                "assessment_date:T",
                                title="Date",
                            ),
                            alt.Tooltip(
                                "score:Q",
                                title="Score",
                            ),
                        ],
                    )
                    .properties(height=280)
                    .configure_axis(
                        labelColor="#12263A",
                        titleColor="#12263A",
                        gridColor="#E5EDF2",
                    )
                    .configure_legend(
                        labelColor="#12263A",
                        titleColor="#12263A",
                    )
                )

                st.altair_chart(
                    clinical_chart,
                    use_container_width=True,
                    theme=None,
                )

                st.caption(
                    f"Improvement direction: higher is better"
                    if direction == "higher"
                    else "Improvement direction: lower is better"
                )


# =========================================================
# AGENCY OUTCOMES
# =========================================================

elif view == "Agency Outcomes":
    st.markdown(
        """
        <div class="agency-hero">
            <div class="agency-hero-title">Agency Outcomes</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    data_dates = pd.read_sql_query(
        """
        SELECT MIN(event_date) AS min_date, MAX(event_date) AS max_date
        FROM (
            SELECT attendance_date AS event_date FROM attendance
            UNION ALL SELECT service_date FROM services
            UNION ALL SELECT checkpoint_date FROM gold_checkpoint_periods
            UNION ALL SELECT assessment_date FROM assessment_administrations
        );
        """,
        conn,
    )
    min_date = pd.to_datetime(data_dates.iloc[0]["min_date"]).date()
    max_date = pd.to_datetime(data_dates.iloc[0]["max_date"]).date()
    program_names = pd.read_sql_query(
        "SELECT program_name FROM programs ORDER BY program_name;", conn
    )["program_name"].tolist()

    filter_cols = st.columns([1.35, 1, 1])
    reporting_period = filter_cols[0].date_input(
        "Reporting Period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    selected_program = filter_cols[1].selectbox(
        "Program", ["All Programs"] + program_names
    )
    selected_status = filter_cols[2].selectbox(
        "Client Status", ["All Clients", "Active", "Discharged"]
    )

    if isinstance(reporting_period, (tuple, list)) and len(reporting_period) == 2:
        start_date, end_date = reporting_period
    else:
        start_date, end_date = min_date, max_date
    start_iso, end_iso = start_date.isoformat(), end_date.isoformat()

    agency_clients = pd.read_sql_query(
        """
        SELECT DISTINCT c.client_id, c.status
        FROM clients c
        LEFT JOIN client_programs cp ON c.client_id = cp.client_id
        LEFT JOIN programs p ON cp.program_id = p.program_id
        WHERE c.admission_date <= :end_date
          AND (:status = 'All Clients' OR c.status = :status)
          AND (:program = 'All Programs' OR p.program_name = :program)
          AND (
              :program = 'All Programs'
              OR (COALESCE(cp.start_date, c.admission_date) <= :end_date
                  AND (cp.end_date IS NULL OR cp.end_date >= :start_date))
          );
        """,
        conn,
        params={
            "start_date": start_iso,
            "end_date": end_iso,
            "status": selected_status,
            "program": selected_program,
        },
    )
    client_ids = agency_clients["client_id"].astype(int).tolist()

    if not client_ids:
        render_empty("No clients match the selected reporting filters.")
    else:
        id_marks = ",".join("?" for _ in client_ids)
        date_params = [*client_ids, start_iso, end_iso]

        attendance = pd.read_sql_query(
            f"""
            SELECT COUNT(*) AS recorded,
                   SUM(CASE WHEN ac.counts_as_present = 1 THEN 1 ELSE 0 END) AS present
            FROM attendance a
            JOIN attendance_codes ac ON a.attendance_code = ac.attendance_code
            WHERE a.client_id IN ({id_marks})
              AND a.attendance_date BETWEEN ? AND ?;
            """,
            conn,
            params=date_params,
        ).iloc[0]
        services = pd.read_sql_query(
            f"""
            SELECT service_type, COUNT(*) AS service_count,
                   SUM(duration_minutes) AS total_minutes
            FROM services
            WHERE client_id IN ({id_marks}) AND service_date BETWEEN ? AND ?
            GROUP BY service_type ORDER BY total_minutes DESC;
            """,
            conn,
            params=date_params,
        )
        goals = pd.read_sql_query(
            f"""
            SELECT status, COUNT(*) AS goal_count
            FROM goals
            WHERE client_id IN ({id_marks})
              AND (start_date IS NULL OR start_date <= ?)
            GROUP BY status;
            """,
            conn,
            params=[*client_ids, end_iso],
        )
        gold = pd.read_sql_query(
            f"""
            SELECT gcs.client_id, gd.domain, gp.checkpoint_name,
                   gp.checkpoint_number, gp.checkpoint_date, AVG(gcs.score) AS score
            FROM gold_checkpoint_scores gcs
            JOIN gold_dimensions gd ON gcs.dimension_id = gd.dimension_id
            JOIN gold_checkpoint_periods gp ON gcs.checkpoint_id = gp.checkpoint_id
            WHERE gcs.client_id IN ({id_marks})
              AND gp.checkpoint_date BETWEEN ? AND ?
            GROUP BY gcs.client_id, gd.domain, gp.checkpoint_id
            ORDER BY gcs.client_id, gd.domain, gp.checkpoint_number;
            """,
            conn,
            params=date_params,
        )
        clinical = pd.read_sql_query(
            f"""
            SELECT aa.client_id, at.assessment_name, am.measure_name,
                   am.improvement_direction, aa.assessment_date, s.score
            FROM assessment_scores s
            JOIN assessment_administrations aa ON s.administration_id = aa.administration_id
            JOIN assessment_measures am ON s.measure_id = am.measure_id
            JOIN assessment_types at ON aa.assessment_type_id = at.assessment_type_id
            WHERE aa.client_id IN ({id_marks})
              AND aa.assessment_date BETWEEN ? AND ?
            ORDER BY aa.client_id, at.assessment_name, am.measure_name, aa.assessment_date;
            """,
            conn,
            params=date_params,
        )

        recorded = int(attendance["recorded"] or 0)
        present = int(attendance["present"] or 0)
        attendance_rate = present / recorded * 100 if recorded else 0
        service_hours = services["total_minutes"].sum() / 60 if not services.empty else 0
        total_goals = int(goals["goal_count"].sum()) if not goals.empty else 0
        achieved_goals = int(
            goals.loc[goals["status"].isin(["Achieved", "Completed"]), "goal_count"].sum()
        ) if not goals.empty else 0
        goals_rate = achieved_goals / total_goals * 100 if total_goals else 0

        headline = st.columns(4)
        metric_card(headline[0], "CH", "Children Served", f"{len(client_ids):,}", "")
        metric_card(headline[1], "AT", "Attendance", f"{attendance_rate:.0f}%", f"{present:,} of {recorded:,} recorded days")
        metric_card(headline[2], "HR", "Service Hours", f"{service_hours:,.0f}", "")
        metric_card(headline[3], "GL", "Goals Achieved", f"{goals_rate:.0f}%", f"{achieved_goals:,} of {total_goals:,} goals")

        st.write("")
        section_header(
            "Children Are Making Measurable Progress",
            "Average Teaching Strategies GOLD levels across children and checkpoints.",
        )
        if gold.empty:
            render_empty("No GOLD checkpoint data is available for this period.")
        else:
            growth_rows = []
            for (cid, domain), group in gold.groupby(["client_id", "domain"]):
                ordered = group.sort_values(["checkpoint_date", "checkpoint_number"])
                if len(ordered) >= 2:
                    growth_rows.append({"client_id": cid, "domain": domain, "growth": ordered.iloc[-1]["score"] - ordered.iloc[0]["score"]})
            growth = pd.DataFrame(growth_rows)
            improving_children = (
                growth.groupby("client_id")["growth"].mean().gt(0).mean() * 100
                if not growth.empty else 0
            )
            st.metric(
                "Children demonstrating developmental progress",
                f"{improving_children:.0f}%",
                help="Children whose average GOLD domain level increased from their first to latest checkpoint in the period.",
            )

            gold_summary = gold.groupby(
                ["domain", "checkpoint_name", "checkpoint_number"], as_index=False
            )["score"].mean()
            gold_chart = (
                alt.Chart(gold_summary)
                .mark_line(point=True, strokeWidth=3)
                .encode(
                    x=alt.X("checkpoint_number:O", title="Checkpoint", axis=alt.Axis(labelExpr="datum.value == 1 ? 'Fall' : datum.value == 2 ? 'Winter' : datum.value == 3 ? 'Spring' : 'Summer'")),
                    y=alt.Y("score:Q", title="Average GOLD Level", scale=alt.Scale(domain=[0, 13])),
                    color=alt.Color("domain:N", title="Development Area", scale=alt.Scale(range=["#08A88D", "#078A76", "#FDC45A", "#73AEDD", "#9292CD", "#18324A"])),
                    tooltip=["domain", "checkpoint_name", alt.Tooltip("score:Q", format=".1f")],
                )
                .properties(height=360)
            )
            st.altair_chart(gold_chart, use_container_width=True, theme=None)

            if not growth.empty:
                domain_growth = growth.groupby("domain", as_index=False)["growth"].mean()
                domain_growth["label"] = domain_growth["growth"].map(lambda value: f"+{value:.1f}" if value >= 0 else f"{value:.1f}")
                growth_chart = (
                    alt.Chart(domain_growth)
                    .mark_bar(cornerRadiusEnd=5, color="#08A88D")
                    .encode(
                        x=alt.X("growth:Q", title="Average level change"),
                        y=alt.Y("domain:N", title=None, sort="-x"),
                        tooltip=["domain", alt.Tooltip("growth:Q", format="+.1f")],
                    )
                    .properties(height=220, title="Average GOLD Growth by Domain")
                )
                st.altair_chart(growth_chart, use_container_width=True, theme=None)

        left, right = st.columns(2, gap="large")
        with left:
            section_header("Clinical Outcomes", "Percentage of children improving, adjusted for each measure's improvement direction.")
            if clinical.empty:
                render_empty("No clinical assessment data is available for this period.")
            else:
                improvement_rows = []
                for keys, group in clinical.groupby(["client_id", "assessment_name", "measure_name"]):
                    ordered = group.sort_values("assessment_date")
                    if len(ordered) >= 2:
                        change = ordered.iloc[-1]["score"] - ordered.iloc[0]["score"]
                        direction = ordered.iloc[0]["improvement_direction"]
                        improvement_rows.append({"assessment": keys[1], "improved": change > 0 if direction == "higher" else change < 0})
                improvement = pd.DataFrame(improvement_rows)
                if improvement.empty:
                    render_empty("At least two scores per child and measure are needed to calculate improvement.")
                else:
                    clinical_summary = improvement.groupby("assessment", as_index=False)["improved"].mean()
                    clinical_summary["percent"] = clinical_summary["improved"] * 100
                    clinical_chart = alt.Chart(clinical_summary).mark_bar(cornerRadiusEnd=5, color="#73AEDD").encode(
                        x=alt.X("percent:Q", title="Children improving (%)", scale=alt.Scale(domain=[0, 100])),
                        y=alt.Y("assessment:N", title=None, sort="-x"),
                        tooltip=["assessment", alt.Tooltip("percent:Q", format=".0f")],
                    ).properties(height=280)
                    st.altair_chart(clinical_chart, use_container_width=True, theme=None)

        with right:
            section_header("Services Delivered", "Service volume by type during the reporting period.")
            if services.empty:
                render_empty("No services were recorded for this period.")
            else:
                services["hours"] = services["total_minutes"] / 60
                service_chart = alt.Chart(services).mark_bar(cornerRadiusEnd=5, color="#FDC45A").encode(
                    x=alt.X("hours:Q", title="Service hours"),
                    y=alt.Y("service_type:N", title=None, sort="-x"),
                    tooltip=["service_type", "service_count", alt.Tooltip("hours:Q", format=".1f")],
                ).properties(height=280)
                st.altair_chart(service_chart, use_container_width=True, theme=None)

        section_header("Goal Progress", "Distribution of treatment goals for children in scope.")
        if goals.empty:
            render_empty("No goals are available for the selected clients.")
        else:
            goal_chart = alt.Chart(goals).mark_arc(innerRadius=62, outerRadius=105).encode(
                theta=alt.Theta("goal_count:Q"),
                color=alt.Color("status:N", title="Goal Status", scale=alt.Scale(range=["#08A88D", "#73AEDD", "#FDC45A", "#9292CD", "#18324A"])),
                tooltip=["status", "goal_count"],
            ).properties(height=300)
            st.altair_chart(goal_chart, use_container_width=True, theme=None)


conn.close()
