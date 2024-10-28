# SunsetNotify
sky aflame(red sky ) sunset notification

|version|desc|
|---|---|
|v1|Retrieve information through Weibo crawler.| 
|v2|Obtain information via image processing, employing LangChain technology|
|v3|Update the method of image acquisition|
|v4|Update code due to website changes|
|v5|Update code due to website changes|
|v6|Update code due to website changes|


## Project Objective

This project aims to automate the analysis of sunset clouds (fire clouds). It uses Python to scrape images of sunset clouds from websites and employs OCR interfaces to extract textual information from these images. Utilizing the LangChain framework and OpenAI's API, the project converts this information into structured data for accurate analysis and prediction of sunset clouds occurrences.

## Key Features

- **Image Scraping**: Automated scraping of sunset cloud images from websites using Python.
- **Text Extraction**: Extracting key textual information from images via an OCR interface.
- **Data Processing**: Processing and transforming data into a structured format using the LangChain framework in conjunction with OpenAI API.
- **Real-time Notifications**: Timely notifying users when there's a prediction of sunset clouds.

## Technologies Used

- **Python**: For writing the scraper and integrating various components.
- **OCR Interface**: To extract text from images.
- **LangChain Framework**: For interacting with the OpenAI API.
- **OpenAI API**: For analyzing and transforming the data.

## Installation Guide

- fork this repo
- register the ocr api
- register the openai api
- run by github action

## Contribution Guidelines

### How to Contribute

- **Report Bugs**: Found an issue? Please report it in the issue tracker with a detailed description.
- **Suggest Features**: Have ideas for improvement? We'd love to hear them! Submit your suggestions as issues.
- **Submit Pull Requests**: Ready to contribute code? Great! 
  - Fork the repository.
  - Create a new branch for your changes.
  - Ensure your code adheres to our coding standards and includes tests.
  - Update documentation if necessary.
  - Submit a pull request with a clear explanation of your changes.

### Need Help?
Don't hesitate to ask questions in the project's issue tracker.

## TODO
- [ ] use docker to run
- [ ] use pm2 to run by schedule
- [x] train a model to ocr instead of using api