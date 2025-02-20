#!/usr/bin/env python3

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import pandas as pd

from perplexity_seo.analysis import compare_response_against_expectation
from perplexity_seo.providers.perplexity import Perplexity

def run_monitoring():
    st.set_page_config(page_title="Perplexity SEO Monitor", layout="wide")
    st.title("Perplexity SEO Response Monitor")

    with st.form("monitoring_form"):
        query = st.text_input(
            "Search Query",
            help="Enter the search query to monitor"
        )
        expectation = st.text_input(
            "Expectation",
            help="Enter a true/false question about what you expect to find"
        )
        end_time = st.time_input(
            "End Time",
            value=(datetime.now() + timedelta(hours=1)).time(),
            help="When should the monitoring stop?"
        )
        interval = st.number_input(
            "Monitoring Interval (seconds)",
            min_value=30,
            value=60,
            help="How often should we check the results?"
        )
        submitted = st.form_submit_button("Start Monitoring")

    if submitted:
        perplexity = Perplexity()
        results = []
        fig = go.Figure()
        chart_container = st.empty()
        
        while datetime.now().time() < end_time:
            response = perplexity.query(query)
            sentiment = compare_response_against_expectation(response, expectation)
            current_time = datetime.now()
            
            results.append({
                'timestamp': current_time,
                'sentiment': 1 if sentiment == "thumbsup" else 0
            })
            
            df = pd.DataFrame(results)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['sentiment'],
                mode='lines+markers',
                name='Sentiment'
            ))
            
            fig.update_layout(
                title='Sentiment Over Time',
                xaxis_title='Time',
                yaxis_title='Sentiment (1=👍, 0=👎)',
                yaxis=dict(tickmode='array', tickvals=[0, 1]),
                height=600
            )
            
            chart_container.plotly_chart(fig, use_container_width=True)
            time.sleep(interval)

if __name__ == "__main__":
    run_monitoring()
