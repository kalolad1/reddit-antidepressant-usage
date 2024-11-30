# What Reddit Reveals About the Reality of Antidepressant Usage

This project analyzes Reddit posts to gather insights into antidepressant usage from self-reported patient experiences. By leveraging Reddit's API and advanced natural language processing (NLP) techniques, the project explores sentiment, demographics, adverse effects, and mentions of various antidepressants.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Author](#author)
- [License](#license)

## Introduction
This project stems from personal experiences and curiosity about the therapeutic realities of antidepressants. Reddit provides a wealth of patient-shared knowledge that, while informal, can reveal trends and insights not present in traditional medical literature. By applying modern NLP techniques, this project aims to:
- Identify patterns in antidepressant efficacy.
- Analyze patient sentiment.
- Explore adverse effects mentioned in user posts.

For full details and analysis, refer to [my write-up on Substack](#).

## Features
- **Data Collection**: Gathers posts from subreddits such as `r/mentalhealth`, `r/depression`, and `r/anxiety` using Reddit's API.
- **Filtering**: Filters posts using a large language model (GPT-4o-mini) to ensure relevance to personal experiences with antidepressants.
- **Sentiment Analysis**: Utilizes `twitter-XLM-roBERTa-base` to classify sentiment as positive, neutral, or negative.
- **Structured Data Extraction**: Extracts details like age, gender, medications, dosage, and adverse effects using JSON schemas.
- **Storage**: Writes processed posts to a MongoDB database for analysis.

## Technologies Used
- Python 3.10+
- Libraries:
  - `praw`: For Reddit API integration.
  - `logging`: For detailed logging of the process.
  - Custom modules (`post_analyzer`, `post_filterer`, etc.).
- NLP Models:
  - GPT-4o-mini for filtering and data extraction.
  - `twitter-XLM-roBERTa-base` for sentiment analysis.
- MongoDB: For database storage.

## Getting Started

### Prerequisites
- Python 3.10 or later
- MongoDB installed and running
- Reddit API credentials
- OpenAI API key for GPT-based processing

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/kalolad1/antidepressant-analysis.git
   cd antidepressant-analysis
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your Reddit API credentials in `post_collector.py`:
   ```python
   CLIENT_ID = "your_client_id"
   CLIENT_SECRET = "your_client_secret"
   USER_AGENT = "your_user_agent"
   ```
4. Configure environment variables
    ```bash
    # MongoDB
    MONGODB_URI=your_mongodb_connection_string

    # OpenAI
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage
1. Start the main script:
   ```bash
   python main.py
   ```
2. Monitor the logs to view progress and any errors.


## Author
This project was created by Darshan Kalola. I am a software engineer, and will be graduating medical school in May of 2025. I am interested in building healthtech to end all human disease. You can learn more about my work and background by visiting [my portfolio website](https://darshankalola.com).

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
