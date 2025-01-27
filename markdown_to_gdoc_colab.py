# Markdown to Google Docs Converter - Colab Version
# Install required packages
!pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

import sys
from google.colab import auth
from google.auth import default
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

class MarkdownToGoogleDocs:
    """Handles conversion of markdown to Google Docs format."""
    
    SCOPES = ['https://www.googleapis.com/auth/documents']
    
    def __init__(self):
        """Initialize the converter."""
        self.creds = None
        self.service = None
    
    def authenticate(self):
        """Authenticate with Google Docs API using Colab environment."""
        # Authenticate using Colab's built-in method
        auth.authenticate_user()
        
        # Get credentials from default auth
        self.creds, _ = default()
        
        # Build the service
        self.service = build('docs', 'v1', credentials=self.creds)

    def create_document(self, title: str) -> str:
        """Create a new Google Doc."""
        try:
            document = self.service.documents().create(body={'title': title}).execute()
            return document.get('documentId')
        except HttpError as error:
            raise Exception(f"Failed to create document: {error}")
    
    def parse_markdown(self, markdown_text: str) -> list:
        """Parse markdown text into structured format."""
        requests = []
        index_map = {}  # Store starting index of each line
        current_index = 1  # Start after title
        
        # First pass: Insert all text and track indices
        lines = markdown_text.split('\n')
        text_content = []
        
        for line in lines:
            if not line.strip():
                text_content.append('\n')
                current_index += 1
                continue
                
            index_map[len(text_content)] = current_index
            text_content.append(line + '\n')
            current_index += len(line) + 1
        
        # Add initial text insertion request
        requests.append({
            'insertText': {
                'location': {'index': 1},
                'text': ''.join(text_content)
            }
        })
        
        # Second pass: Apply formatting
        for i, line in enumerate(lines):
            if not line.strip():
                continue
                
            start_index = index_map[i]
            end_index = start_index + len(line)
            
            # Handle headers
            if line.startswith('#'):
                level = len(re.match(r'^#+', line).group())
                style = {
                    1: 'HEADING_1',
                    2: 'HEADING_2',
                    3: 'HEADING_3',
                }.get(level, 'NORMAL_TEXT')
                
                requests.append({
                    'updateParagraphStyle': {
                        'range': {
                            'startIndex': start_index,
                            'endIndex': end_index
                        },
                        'paragraphStyle': {'namedStyleType': style},
                        'fields': 'namedStyleType'
                    }
                })
            
            # Handle checkboxes
            elif '- [ ]' in line or '- [x]' in line:
                requests.append({
                    'createParagraphBullets': {
                        'range': {
                            'startIndex': start_index,
                            'endIndex': end_index
                        },
                        'bulletPreset': 'NUMBERED_DECIMAL_NESTED'
                    }
                })
            
            # Handle bullet points
            elif line.strip().startswith('*') or line.strip().startswith('-'):
                indent_level = len(re.match(r'^\s*', line).group()) // 2
                indent_size = 36 * indent_level
                
                requests.append({
                    'createParagraphBullets': {
                        'range': {
                            'startIndex': start_index,
                            'endIndex': end_index
                        },
                        'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                    }
                })
                
                if indent_level > 0:
                    requests.append({
                        'updateParagraphStyle': {
                            'range': {
                                'startIndex': start_index,
                                'endIndex': end_index
                            },
                            'paragraphStyle': {
                                'indentStart': {
                                    'magnitude': indent_size,
                                    'unit': 'PT'
                                },
                                'indentFirstLine': {
                                    'magnitude': indent_size,
                                    'unit': 'PT'
                                }
                            },
                            'fields': 'indentStart,indentFirstLine'
                        }
                    })
            
            # Handle assignee mentions
            if '@' in line:
                for match in re.finditer(r'@(\w+)', line):
                    mention_start = start_index + match.start()
                    mention_end = start_index + match.end()
                    requests.append({
                        'updateTextStyle': {
                            'range': {
                                'startIndex': mention_start,
                                'endIndex': mention_end
                            },
                            'textStyle': {
                                'bold': True,
                                'foregroundColor': {
                                    'color': {
                                        'rgbColor': {
                                            'blue': 0.8,
                                            'red': 0.2,
                                            'green': 0.2
                                        }
                                    }
                                }
                            },
                            'fields': 'bold,foregroundColor'
                        }
                    })
        
        return requests
    
    def convert(self, markdown_text: str, title: str = "Converted Meeting Notes") -> str:
        """Convert markdown text to Google Doc."""
        if not self.service:
            raise Exception("Not authenticated. Call authenticate() first.")
            
        try:
            # Create new document
            doc_id = self.create_document(title)
            
            # Parse markdown and get requests
            requests = self.parse_markdown(markdown_text)
            
            # Execute requests
            self.service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            return doc_id
            
        except HttpError as error:
            raise Exception(f"Failed to convert document: {error}")

# Sample markdown text
markdown_text = """# Product Team Sync - May 15, 2023

## Attendees
- Sarah Chen (Product Lead)
- Mike Johnson (Engineering)
- Anna Smith (Design)
- David Park (QA)

## Action Items
- [ ] @sarah: Finalize Q3 roadmap by Friday
- [ ] @mike: Schedule technical review for payment integration
- [ ] @anna: Share updated design system documentation
- [ ] @david: Prepare QA resource allocation proposal
"""

# Initialize and authenticate
converter = MarkdownToGoogleDocs()
converter.authenticate()  # No credentials file needed anymore

# Convert markdown to Google Doc
doc_id = converter.convert(markdown_text, "Product Team Sync Notes")
print(f"Created document: https://docs.google.com/document/d/{doc_id}/edit")
