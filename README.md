# Mock Interview System

## Overview

The **Mock Interview System** is designed to help students overcome the fear of interviews by providing a platform where they can practice responding to interview questions confidently. This system simulates a real interview environment, allowing users to select a technology stack and respond to relevant interview questions verbally. The system converts their spoken answers into text, analyzes the responses using Natural Language Processing (NLP) techniques, and provides detailed feedback, helping students improve their answers and build confidence.

## Features

- **Technology Stack Selection:** Users can select the technology stack they wish to practice.
- **Speech-to-Text Conversion:** Verbal responses are converted to text for further analysis.
- **Secure Storage:** User responses and analysis results are securely stored in AWS S3.
- **Automated Processing:** AWS Lambda functions trigger the processing and analysis of user responses.
- **NLP Analysis:** AWS SageMaker is utilized to analyze responses using NLP techniques, providing feedback on accuracy and quality.
- **Feedback Display:** Analysis results are displayed on a user-friendly web page with an intuitive and visually appealing UI/UX, including a bar graph for easy interpretation.

## Tech Stack

- **Flask:** Develops the web application, manages user interactions, and renders web pages.
- **AWS S3:** Stores user responses and analysis results securely in the cloud.
- **AWS Lambda:** Processes user responses and triggers the analysis workflow.
- **AWS SageMaker:** Implements a notebook instance for analyzing user responses using NLP techniques.
- **Natural Language Processing (NLP):** Analyzes the content of user responses, comparing them with correct answers.
- **UI/UX Design:** Presents the analysis results on a web page, featuring a visually appealing bar graph for easy understanding.

## Process Overview

1. **User Interaction:** Students select a stack and answer interview questions verbally.
2. **Speech-to-Text Conversion:** The system converts spoken responses into text.
3. **Storage in AWS S3:** The text responses are stored in an AWS S3 bucket.
4. **Lambda Function Trigger:** An AWS Lambda function is triggered to process the text responses.
5. **Analysis in AWS SageMaker:** The text responses and correct answers are analyzed using NLP techniques in a SageMaker notebook instance.
6. **Feedback Storage:** The analysis results are stored back in the AWS S3 bucket.
7. **Results Display:** The system displays the analysis results on a web page with an intuitive UI/UX, including a bar graph for easy understanding.

## Installation

### Prerequisites

- Python 3.8+
- AWS account with access to S3, Lambda, and SageMaker
- Flask

### Clone the Repository

```bash
git clone https://github.com/yourusername/mock-interview-system.git
cd mock-interview-system
