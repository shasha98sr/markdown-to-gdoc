# Markdown to Google Docs Converter

A Python script that converts markdown meeting notes into well-formatted Google Docs using Google Docs API. This tool is designed to run in Google Colab for easy access and authentication.

## Features

- Converts markdown meeting notes to Google Docs format
- Maintains proper heading hierarchy
- Preserves bullet points and nested lists
- Converts markdown checkboxes to Google Docs checkboxes
- Highlights assignee mentions (@name)
- Preserves meeting metadata and footer information

## Prerequisites

- Google Account
- Access to Google Colab
- Google Cloud Project with Google Docs API enabled
- Required Python packages (installed automatically in Colab):
  - google-auth
  - google-auth-oauthlib
  - google-auth-httplib2
  - google-api-python-client

## Setup Instructions

1. Open the `markdown_to_gdoc.ipynb` notebook in Google Colab
2. Follow the authentication steps in the notebook
3. Upload your markdown file or use the provided sample
4. Run the notebook cells to convert your markdown to Google Docs

## Usage

1. The notebook will guide you through the authentication process
2. Once authenticated, the script will:
   - Create a new Google Doc
   - Convert and format the markdown content
   - Provide you with a link to the created document

## Project Structure

```
markdown-to-gdoc/
├── src/
│   ├── markdown_converter.py    # Main conversion logic
│   └── gdoc_formatter.py       # Google Docs formatting utilities
├── data/
│   └── sample_notes.md         # Sample markdown notes
└── README.md                   # Project documentation
```

## License

MIT License

## Contributing

Feel free to open issues or submit pull requests for any improvements.
