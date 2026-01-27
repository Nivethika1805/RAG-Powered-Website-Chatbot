import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import Optional, List

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_website(self, url: str) -> Optional[str]:
        """Scrape main content from a website URL."""
        try:
            print(f"Starting to scrape: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            print(f"Successfully fetched URL, status: {response.status_code}")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'ads']):
                element.decompose()
            
            # Extract main content
            content = ""
            
            # Try to find main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article'))
            
            if main_content:
                content = self._extract_text_from_element(main_content)
                print(f"Found main content area, extracted {len(content)} characters")
            else:
                # Fallback to body content
                content = self._extract_text_from_element(soup.find('body'))
                print(f"Using body content, extracted {len(content)} characters")
            
            cleaned_content = self._clean_text(content)
            print(f"Final cleaned content length: {len(cleaned_content)}")
            return cleaned_content
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def _extract_text_from_element(self, element) -> str:
        """Extract text from HTML element, preserving structure."""
        if not element:
            return ""
        
        # Get text with proper spacing
        text = element.get_text(separator=' ', strip=True)
        return text
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove multiple consecutive punctuation
        text = re.sub(r'[.]{2,}', '.', text)
        # Remove extra spaces around punctuation
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        return text.strip()
    
    def scrape_multiple_pages(self, base_url: str, max_pages: int = 5) -> List[str]:
        """Scrape multiple pages from a website."""
        contents = []
        
        try:
            # Get the base page
            main_content = self.scrape_website(base_url)
            if main_content:
                contents.append(main_content)
            
            # Try to find additional links (basic implementation)
            response = self.session.get(base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            base_domain = urlparse(base_url).netloc
            links_found = 0
            
            for link in soup.find_all('a', href=True):
                if links_found >= max_pages - 1:
                    break
                    
                href = link['href']
                full_url = urljoin(base_url, href)
                
                # Only follow links to the same domain
                if urlparse(full_url).netloc == base_domain:
                    content = self.scrape_website(full_url)
                    if content and content not in contents:
                        contents.append(content)
                        links_found += 1
                        
        except Exception as e:
            print(f"Error in multi-page scraping: {e}")
        
        return contents
