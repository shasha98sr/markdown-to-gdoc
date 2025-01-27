"""
Markdown to Google Docs Converter
This script converts markdown meeting notes to a formatted Google Doc.
"""

import re
from typing import Dict, List, Tuple
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class MarkdownToGoogleDocs:
    """Handles conversion of markdown to Google Docs format."""
    
    SCOPES = ['https://www.googleapis.com/auth/documents']
    
    def __init__(self):
        """Initialize the converter with authentication."""
        self.creds = None
        self.service = None
    
    def authenticate(self, creds_path: str = None):
        """
        Authenticate with Google Docs API.
        
        Args:
            creds_path: Path to credentials JSON file
        """
        if not creds_path:
            raise ValueError("Credentials path is required")
            
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.SCOPES)
        self.creds = flow.run_local_server(port=0)
        self.service = build('docs', 'v1', credentials=self.creds)
    
    def create_document(self, title: str) -> str:
        """
        Create a new Google Doc.
        
        Args:
            title: Document title
            
        Returns:
            document_id: ID of created document
        """
        try:
            document = self.service.documents().create(body={'title': title}).execute()
            return document.get('documentId')
        except HttpError as error:
            raise Exception(f"Failed to create document: {error}")
    
    def parse_markdown(self, markdown_text: str) -> List[Dict]:
        """
        Parse markdown text into structured format.
        
        Args:
            markdown_text: Raw markdown text
            
        Returns:
            List of formatting requests for Google Docs API
        """
        requests = []
        current_index = 1  # Start after title
        
        # Split into lines
        lines = markdown_text.split('\n')
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                current_index += 1
                continue
                
            # Handle headers
            if line.startswith('#'):
                level = len(re.match(r'^#+', line).group())
                text = line.lstrip('#').strip()
                requests.extend(self._create_heading_request(text, level, current_index))
                
            # Handle checkboxes
            elif '- [ ]' in line or '- [x]' in line:
                text = line.replace('- [ ]', '').replace('- [x]', '').strip()
                requests.extend(self._create_checkbox_request(text, current_index))
                
            # Handle bullet points
            elif line.strip().startswith('*') or line.strip().startswith('-'):
                indent_level = len(re.match(r'^\s*', line).group()) // 2
                text = line.lstrip('* -').strip()
                requests.extend(self._create_bullet_request(text, indent_level, current_index))
                
            # Handle assignee mentions
            if '@' in line:
                mentions = re.finditer(r'@(\w+)', line)
                for match in mentions:
                    requests.extend(self._create_mention_style(match.group(1), current_index))
            
            current_index += 1
            
        return requests
    
    def _create_heading_request(self, text: str, level: int, index: int) -> List[Dict]:
        """Create requests for heading formatting."""
        style = {
            1: 'HEADING_1',
            2: 'HEADING_2',
            3: 'HEADING_3',
        }.get(level, 'NORMAL_TEXT')
        
        return [{
            'insertText': {
                'location': {'index': index},
                'text': f"{text}\n"
            }
        }, {
            'updateParagraphStyle': {
                'range': {
                    'startIndex': index,
                    'endIndex': index + len(text) + 1
                },
                'paragraphStyle': {'namedStyleType': style},
                'fields': 'namedStyleType'
            }
        }]
    
    def _create_checkbox_request(self, text: str, index: int) -> List[Dict]:
        """Create requests for checkbox items."""
        return [{
            'insertText': {
                'location': {'index': index},
                'text': f"{text}\n"
            }
        }, {
            'createParagraphBullets': {
                'range': {
                    'startIndex': index,
                    'endIndex': index + len(text) + 1
                },
                'bulletPreset': 'CHECKBOX'
            }
        }]
    
    def _create_bullet_request(self, text: str, indent_level: int, index: int) -> List[Dict]:
        """Create requests for bullet points with indentation."""
        return [{
            'insertText': {
                'location': {'index': index},
                'text': f"{text}\n"
            }
        }, {
            'createParagraphBullets': {
                'range': {
                    'startIndex': index,
                    'endIndex': index + len(text) + 1
                },
                'bulletPreset': 'BULLET',
                'indentLevel': indent_level
            }
        }]
    
    def _create_mention_style(self, name: str, index: int) -> List[Dict]:
        """Create requests for styling mentions."""
        return [{
            'updateTextStyle': {
                'range': {
                    'startIndex': index,
                    'endIndex': index + len(name) + 1  # +1 for @ symbol
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
        }]
    
    def convert(self, markdown_text: str, title: str = "Converted Meeting Notes") -> str:
        """
        Convert markdown text to Google Doc.
        
        Args:
            markdown_text: Raw markdown text
            title: Document title
            
        Returns:
            document_id: ID of created document
        """
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
