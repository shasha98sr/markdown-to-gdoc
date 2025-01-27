# Markdown to Google Docs Converter

A Python script that automatically converts markdown meeting notes into well-formatted Google Docs. This tool runs in Google Colab for easy access and authentication, making it perfect for teams that want to convert their markdown notes into shareable Google Docs.

## Features

- Converts markdown meeting notes to Google Docs with proper formatting
- Maintains document structure:
  - Title as Heading 1
  - Section headers as Heading 2
  - Sub-sections as Heading 3
  - Nested bullet points with proper indentation
  - Numbered lists for action items
  - Highlighted @mentions for better visibility
- Uses Google Colab for easy authentication and execution
- No local setup required

## Quick Start

1. Open the Colab Notebook in your colab environment
2. Run the first cell to install required packages
3. Run the authentication cell - you'll need to authorize the app
4. Paste your markdown content into the `markdown_text` variable
5. Run the conversion cell
6. Click the generated link to view your Google Doc

## Detailed Setup

### Prerequisites

- Google Account
- Access to Google Colab
- Google Cloud Project with Google Docs API enabled

### Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable the Google Docs API for your project
4. No need to create credentials - Colab handles authentication

### Running the Converter

1. Open the Colab notebook
2. The notebook will handle authentication automatically
3. Paste your markdown content
4. Run the conversion
5. The script will provide a direct link to your new Google Doc

## Markdown Format Support

The converter supports the following markdown elements:

```markdown
# Main Title (Heading 1)
## Section (Heading 2)
### Subsection (Heading 3)

- Bullet points
  - Nested bullet points
    - Multiple levels supported

1. Numbered lists
2. For action items

- [ ] Checkbox items
- [x] Completed items

@mentions for highlighting team members
```

## Implementation Details

The converter uses a two-pass approach for reliable formatting:

1. First Pass:
   - Inserts all text content at once
   - Creates an index map for precise formatting

2. Second Pass:
   - Applies formatting to each element
   - Handles headings, bullets, and mentions
   - Maintains proper indentation

## Troubleshooting

If you encounter issues:

1. Make sure you're signed into the correct Google account
2. Check that the Google Docs API is enabled in your project
3. Try refreshing the Colab runtime if authentication fails
4. Verify your markdown syntax is correct

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

MIT License

## Credits

Created as part of a coding assessment project. Special thanks to the Google Docs API team for their excellent documentation.
