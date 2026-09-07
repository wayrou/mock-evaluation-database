import sqlite3

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Client Evaluation Dashboard",
    layout="wide",
)

st.title("Client Evaluation Dashboard")
st.caption("All client data is fictional.")

conn = sqlite3.connect("evaluation.db")


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


selected_name = st.selectbox(
    "Select Client",
    clients["name"],
)


client = clients[
    clients["name"] == selected_name
].iloc[0]


assessment_data = pd.read_sql_query(
    """
    SELECT
        c.client_id,
        c.name,
        at.assessment_name,
        at.improvement_direction,
        a.assessment_date,
        a.score
    FROM assessments a
    JOIN clients c
        ON a.client_id = c.client_id
    JOIN assessment_types at
        ON a.assessment_type_id = at.assessment_type_id
    WHERE c.client_id = ?
    ORDER BY
        at.assessment_name,
        a.assessment_date;
    """,
    conn,
    params=(int(client["client_id"]),),
)


program_data = pd.read_sql_query(
    """
    SELECT
        p.program_name,
        cp.start_date,
        cp.end_date
    FROM client_programs cp
    JOIN programs p
        ON cp.program_id = p.program_id
    WHERE cp.client_id = ?;
    """,
    conn,
    params=(int(client["client_id"]),),
)


col1, col2, col3 = st.columns(3)

col1.metric(
    "Client",
    client["name"],
)

col2.metric(
    "Status",
    client["status"],
)

col3.metric(
    "Admission Date",
    client["admission_date"],
)


if not program_data.empty:
    st.subheader("Program")

    st.write(program_data)


st.subheader("Assessment Progress")

if assessment_data.empty:
    st.info("No assessment data available for this client.")

else:
    assessment_names = assessment_data[
        "assessment_name"
    ].unique()

    for assessment_name in assessment_names:

        data = assessment_data[
            assessment_data["assessment_name"]
            == assessment_name
        ].copy()

        data["assessment_date"] = pd.to_datetime(
            data["assessment_date"]
        )

        baseline = data.iloc[0]["score"]
        latest = data.iloc[-1]["score"]
        change = latest - baseline

        direction = data.iloc[0][
            "improvement_direction"
        ]

        st.markdown(f"### {assessment_name}")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Baseline",
            baseline,
        )

        c2.metric(
            "Latest",
            latest,
        )

        c3.metric(
            "Change",
            change,
        )

        chart_data = data.set_index(
            "assessment_date"
        )[["score"]]

        st.line_chart(chart_data)


st.subheader("Assessment History")

st.dataframe(
    assessment_data[
        [
            "assessment_name",
            "assessment_date",
            "score",
        ]
    ],
    use_container_width=True,
)


conn.close()