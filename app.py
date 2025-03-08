from flask import Flask, request, jsonify, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Load dataset
df = pd.read_excel("final.xlsx")
df['Title'] = df['Title'].str.lower()

date_range_order = [
    "4500-4000 BCE", "4000-3500 BCE", "3500-3000 BCE", "3000-2500 BCE", "2500-2000 BCE", 
    "2000-1500 BCE", "1500-1000 BCE", "1000-500 BCE", "500-0 BCE", "0-1st", "1-3rd", "3-4th", 
    "4-5th", "5th-6th", "7-8th", "8-10th", "10-12th", "12-13th", "13-14th", "14-15th", 
    "16-17th", "18-19th", "20-21st"
]

def generate_visualization(keyword):
    artifact_df = df[df['Title'].str.contains(keyword.lower(), na=False)]
    if artifact_df.empty:
        return None

    artifact_grouped_df = artifact_df.groupby(['Range2Century', 'Region']).size().reset_index(name='Count')
    artifact_grouped_df['Range2Century'] = pd.Categorical(artifact_grouped_df['Range2Century'], categories=date_range_order, ordered=True)
    artifact_grouped_df = artifact_grouped_df.sort_values(by=['Range2Century'])

    plt.figure(figsize=(15, 8))
    ax = sns.barplot(data=artifact_grouped_df, x='Range2Century', y='Count', hue='Region')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Date Range")
    plt.ylabel("Artifact Count")
    plt.title(f"Artifacts Containing '{keyword}'")
    plt.legend(title="Region", loc='upper left')

    image_path = "static/artifact_plot.png"
    plt.savefig(image_path)
    plt.close()
    
    return image_path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    image_path = generate_visualization(keyword)
    if image_path is None:
        return jsonify({"error": "No artifacts found"}), 404

    return jsonify({"image_url": image_path})

if __name__ == '__main__':
    app.run(debug=True)
