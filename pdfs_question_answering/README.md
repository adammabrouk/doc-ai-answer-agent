# Fix your own Bike Agent 🏥

This repository contains a simple app in python 🐍 That answers questio on how to repair a motocycle, using the motocycle repaire manual ( can also be enriched with general mechanics knowledge )

The Python code uses various libraries like OpenAI, Langchain, Tiktoken, and Yaml to help in this process. The main highlight of this code is the ability to ask a set of defined questions to each insurance policy, and get detailed answers using language models. 👥

## What does the script do? 🤔

Loading Data from PDFs: 📄 The script takes as input PDF documents converts them into text data using the PdfToTextLoader.

Vectorizing dataset: 📊 The script then vectorizes the text data. This involves transforming the text data into a form that machine learning algorithms can understand.

Asking questions: ❓ Enables user to input one or many set of questions

Comparing Answers: 🆚 After gathering the responses, the script summarizes the answers and reformulates them to give a proper readable human answer.
