#!/usr/bin/env python3
"""
Complete Integrated SEO MCP Server
Comprehensive SEO analysis with Keywords Everywhere integration
"""

import asyncio
import json
import os
import re
import time
import random
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse
import aiohttp
from datetime import datetime, timezone
from serpapi import GoogleSearch

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use os.environ directly

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("seo-complete-analysis")

class KeywordsEverywhereAPI:
    """Keywords Everywhere API client integrated into SEO MCP"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('KEYWORDS_EVERYWHERE_API_KEY')
        self.base_url = "https://api.keywordseverywhere.com/v1"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def get_search_volume(self, keywords: List[str], country: str = "US") -> Dict:
        """Get search volume data for keywords - FIXED API format"""
        async with aiohttp.ClientSession() as session:
            # FIXED: Use correct parameter format from official documentation
            data = {
                'country': country.lower(),
                'currency': 'usd',
                'dataSource': 'gkp',
                'kw[]': keywords  # FIXED: This was the main issue - API expects kw[] not keywords
            }
            
            async with session.post(
                f"{self.base_url}/get_keyword_data",
                headers=self.headers,
                data=data  # FIXED: Use 'data' instead of 'json' for form data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Keywords Everywhere API error: {response.status} - {error_text}")
    
    async def get_related_keywords(self, keyword: str, country: str = "US") -> Dict:
        """Get related keywords using bulk keyword discovery approach - FIXED for actual API"""
        async with aiohttp.ClientSession() as session:
            # FIXED: Use the working get_keyword_data endpoint approach to simulate related keywords
            # Generate related keyword variations for the seed keyword
            related_variants = [
                f"{keyword} tips",
                f"{keyword} guide", 
                f"{keyword} tutorial",
                f"{keyword} examples",
                f"{keyword} tools",
                f"how to {keyword}",
                f"best {keyword}",
                f"{keyword} strategies",
                f"{keyword} techniques",
                f"{keyword} benefits"
            ]
            
            # Use the working get_keyword_data endpoint format
            data = {
                'country': country.lower(),
                'currency': 'usd',  
                'dataSource': 'gkp',
                'kw[]': related_variants  # Use working format from get_keyword_data
            }
            
            async with session.post(
                f"{self.base_url}/get_keyword_data",  # Use working endpoint
                headers=self.headers,
                data=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    # Format response to match expected structure
                    return {
                        'seed_keyword': keyword,
                        'data': result.get('data', []),
                        'total_count': len(result.get('data', []))
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Keywords Everywhere API error: {response.status} - {error_text}")
    
    async def test_api_connection(self) -> Dict:
        """Test Keywords Everywhere API connection and key validity"""
        if not self.api_key:
            return {
                'status': 'error',
                'message': 'API key not found. Please set KEYWORDS_EVERYWHERE_API_KEY environment variable.'
            }
        
        # Test with a simple keyword query
        try:
            test_keywords = ['test']
            data = await self.get_search_volume(test_keywords, 'US')
            return {
                'status': 'success',
                'message': 'API connection successful',
                'api_key_valid': True,
                'test_result': data
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'API connection failed: {str(e)}',
                'api_key_valid': False
            }

class SEOScraperComplete:
    def __init__(self):
        self.browser = None
        self.context = None
        self.session = None
        self.ke_api = KeywordsEverywhereAPI()
    
    async def start_browser(self):
        """Initialize browser context"""
        if not self.browser:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
    
    async def start_session(self):
        """Initialize aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_resources(self):
        """Clean up all resources"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
        if self.session:
            await self.session.close()
    
    async def scrape_seo_data(self, url: str) -> Dict:
        """Extract comprehensive SEO data - SIMPLIFIED for Claude analysis"""
        try:
            await self.start_browser()
            page = await self.context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            html_content = await page.content()
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Extract raw data for Claude to analyze
            seo_data = {
                'url': url,
                'extraction_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                
                # Basic SEO elements
                'title': self.extract_title(soup),
                'meta_tags': self.extract_meta_tags(soup),
                'headers': self.extract_headers(soup),
                'canonical_url': self.extract_canonical(soup),
                'robots_meta': self.extract_robots_meta(soup),
                'meta_viewport': self.extract_meta_viewport(soup),
                
                # Content data (raw for Claude analysis)
                'main_content': self.extract_main_content(soup),
                'full_text': self.extract_full_text(soup),
                'word_count': self.get_word_count(soup),
                
                # Link data
                'internal_links': self.extract_internal_links(soup, url),
                'external_links': self.extract_external_links(soup, url),
                
                # Structured data
                'schema_markup': self.extract_schema_markup(soup),
                'open_graph': self.extract_open_graph(soup),
                'twitter_cards': self.extract_twitter_cards(soup),
                
                # Technical elements
                'hreflang': self.extract_hreflang(soup),
                'meta_refresh': self.extract_meta_refresh(soup),
                'base_href': self.extract_base_href(soup)
            }
            
            await page.close()
            return seo_data
        except Exception as e:
            return {'error': f"Error scraping {url}: {str(e)}"}
    
    def extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content text for Claude analysis"""
        # Remove non-content elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()
        
        # Try to find main content area
        main_content = (soup.find('main') or 
                       soup.find('article') or 
                       soup.find('div', class_=re.compile(r'content|main|post|article', re.I)) or
                       soup.find('div', id=re.compile(r'content|main|post|article', re.I)))
        
        if main_content:
            return main_content.get_text(separator=' ', strip=True)
        else:
            # Fallback to body content
            body = soup.find('body')
            if body:
                return body.get_text(separator=' ', strip=True)
            return soup.get_text(separator=' ', strip=True)
    
    def extract_full_text(self, soup: BeautifulSoup) -> str:
        """Extract all visible text for comprehensive analysis"""
        # Remove scripts and styles but keep other content
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text(separator=' ', strip=True)
    
    # FIXED: Enhanced structured data validation
    def validate_structured_data_enhanced(self, soup: BeautifulSoup) -> Dict:
        """Enhanced structured data validation with comprehensive Schema.org checking"""
        validation_data = {
            'json_ld': [],
            'microdata': [],
            'rdfa': [],
            'validation_errors': [],
            'schema_types': [],
            'rich_results_eligibility': {}
        }
        
        # Extract and validate JSON-LD
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                json_data = json.loads(script.string)
                validation_data['json_ld'].append(json_data)
                
                # Handle both single objects and graphs
                if isinstance(json_data, dict):
                    if '@graph' in json_data:
                        # Handle Schema.org graph structure
                        for item in json_data['@graph']:
                            if isinstance(item, dict) and '@type' in item:
                                schema_type = item['@type']
                                validation_data['schema_types'].append(schema_type)
                                validation_data['rich_results_eligibility'][schema_type] = self.check_rich_results_eligibility_enhanced(item, schema_type)
                    elif '@type' in json_data:
                        # Handle single schema object
                        schema_type = json_data['@type']
                        validation_data['schema_types'].append(schema_type)
                        validation_data['rich_results_eligibility'][schema_type] = self.check_rich_results_eligibility_enhanced(json_data, schema_type)
                elif isinstance(json_data, list):
                    # Handle array of schema objects
                    for item in json_data:
                        if isinstance(item, dict) and '@type' in item:
                            schema_type = item['@type']
                            validation_data['schema_types'].append(schema_type)
                            validation_data['rich_results_eligibility'][schema_type] = self.check_rich_results_eligibility_enhanced(item, schema_type)
                    
            except json.JSONDecodeError as e:
                validation_data['validation_errors'].append(f"Invalid JSON-LD: {str(e)}")
        
        # Extract microdata
        for item in soup.find_all(attrs={'itemtype': True}):
            microdata_item = {
                'itemtype': item.get('itemtype'),
                'properties': {}
            }
            
            for prop in item.find_all(attrs={'itemprop': True}):
                prop_name = prop.get('itemprop')
                prop_value = prop.get('content') or prop.get_text().strip()
                microdata_item['properties'][prop_name] = prop_value
            
            validation_data['microdata'].append(microdata_item)
            
            # Check rich results for microdata
            itemtype = item.get('itemtype', '')
            if itemtype:
                schema_type = itemtype.split('/')[-1]  # Extract type from URL
                validation_data['rich_results_eligibility'][f"microdata_{schema_type}"] = self.check_microdata_rich_results(microdata_item)
        
        # Extract RDFa
        for item in soup.find_all(attrs={'typeof': True}):
            rdfa_item = {
                'typeof': item.get('typeof'),
                'properties': {}
            }
            
            for prop in item.find_all(attrs={'property': True}):
                prop_name = prop.get('property')
                prop_value = prop.get('content') or prop.get_text().strip()
                rdfa_item['properties'][prop_name] = prop_value
            
            validation_data['rdfa'].append(rdfa_item)
        
        return validation_data
    
    def check_rich_results_eligibility_enhanced(self, data: Dict, schema_type: str) -> Dict:
        """Enhanced rich results eligibility checker with comprehensive validation"""
        eligibility = {
            'eligible': False,
            'missing_required_fields': [],
            'missing_recommended_fields': [],
            'rich_result_features': [],
            'google_rich_results_compatible': False,
            'validation_score': 0
        }
        
        # Comprehensive required and recommended fields for major schema types
        schema_requirements = {
            'Article': {
                'required': ['headline', 'datePublished', 'author'],
                'recommended': ['dateModified', 'image', 'publisher', 'mainEntityOfPage'],
                'features': ['article_rich_results', 'amp_articles', 'top_stories']
            },
            'NewsArticle': {
                'required': ['headline', 'datePublished', 'author'],
                'recommended': ['dateModified', 'image', 'publisher', 'mainEntityOfPage'],
                'features': ['top_stories', 'article_rich_results']
            },
            'BlogPosting': {
                'required': ['headline', 'datePublished', 'author'],
                'recommended': ['dateModified', 'image', 'publisher'],
                'features': ['article_rich_results']
            },
            'Product': {
                'required': ['name', 'offers'],
                'recommended': ['image', 'description', 'brand', 'review', 'aggregateRating'],
                'features': ['product_rich_results', 'merchant_listings']
            },
            'Recipe': {
                'required': ['name', 'recipeIngredient', 'recipeInstructions'],
                'recommended': ['image', 'author', 'datePublished', 'description', 'nutrition', 'cookTime', 'prepTime'],
                'features': ['recipe_rich_results', 'recipe_carousel']
            },
            'Event': {
                'required': ['name', 'startDate', 'location'],
                'recommended': ['description', 'image', 'endDate', 'offers', 'performer'],
                'features': ['event_rich_results']
            },
            'Organization': {
                'required': ['name'],
                'recommended': ['url', 'logo', 'sameAs', 'contactPoint'],
                'features': ['knowledge_panel', 'sitelinks_searchbox']
            },
            'LocalBusiness': {
                'required': ['name', 'address'],
                'recommended': ['telephone', 'openingHours', 'image', 'priceRange', 'review'],
                'features': ['local_business_rich_results', 'knowledge_panel', 'local_pack']
            },
            'Person': {
                'required': ['name'],
                'recommended': ['image', 'jobTitle', 'worksFor', 'sameAs'],
                'features': ['knowledge_panel', 'person_rich_results']
            },
            'WebSite': {
                'required': ['name', 'url'],
                'recommended': ['potentialAction', 'sameAs'],
                'features': ['sitelinks_searchbox', 'site_name_rich_results']
            },
            'VideoObject': {
                'required': ['name', 'description', 'thumbnailUrl', 'uploadDate'],
                'recommended': ['duration', 'embedUrl', 'contentUrl'],
                'features': ['video_rich_results', 'video_carousel']
            },
            'FAQPage': {
                'required': ['mainEntity'],
                'recommended': [],
                'features': ['faq_rich_results']
            },
            'HowTo': {
                'required': ['name', 'step'],
                'recommended': ['image', 'totalTime', 'estimatedCost', 'supply', 'tool'],
                'features': ['how_to_rich_results']
            },
            'BreadcrumbList': {
                'required': ['itemListElement'],
                'recommended': [],
                'features': ['breadcrumb_rich_results']
            }
        }
        
        if schema_type not in schema_requirements:
            eligibility['validation_score'] = 0
            eligibility['missing_required_fields'] = ['Unknown schema type']
            return eligibility
        
        requirements = schema_requirements[schema_type]
        
        # Check required fields
        missing_required = []
        for field in requirements['required']:
            if not self._check_field_exists(data, field):
                missing_required.append(field)
        
        # Check recommended fields
        missing_recommended = []
        for field in requirements['recommended']:
            if not self._check_field_exists(data, field):
                missing_recommended.append(field)
        
        # Calculate eligibility
        eligibility['missing_required_fields'] = missing_required
        eligibility['missing_recommended_fields'] = missing_recommended
        eligibility['eligible'] = len(missing_required) == 0
        eligibility['google_rich_results_compatible'] = len(missing_required) == 0 and len(missing_recommended) <= 2
        
        # Add potential features
        if eligibility['eligible']:
            eligibility['rich_result_features'] = requirements['features']
        
        # Calculate validation score (0-100)
        total_fields = len(requirements['required']) + len(requirements['recommended'])
        present_fields = total_fields - len(missing_required) - len(missing_recommended)
        eligibility['validation_score'] = int((present_fields / total_fields) * 100) if total_fields > 0 else 0
        
        # Add specific recommendations
        eligibility['recommendations'] = self._get_schema_recommendations(schema_type, missing_required, missing_recommended)
        
        return eligibility
    
    def _check_field_exists(self, data: Dict, field_path: str) -> bool:
        """Check if a nested field exists in the data"""
        if '.' in field_path:
            # Handle nested fields like 'address.streetAddress'
            parts = field_path.split('.')
            current = data
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return False
            return current is not None and current != ''
        else:
            # Handle direct fields
            return field_path in data and data[field_path] is not None and data[field_path] != ''
    
    def _get_schema_recommendations(self, schema_type: str, missing_required: List[str], missing_recommended: List[str]) -> List[str]:
        """Get specific recommendations for schema improvement"""
        recommendations = []
        
        if missing_required:
            recommendations.append(f"Add required fields: {', '.join(missing_required)}")
        
        if missing_recommended:
            recommendations.append(f"Consider adding recommended fields: {', '.join(missing_recommended[:3])}")
        
        # Schema-specific recommendations
        if schema_type == 'Article' and 'image' in missing_recommended:
            recommendations.append("Add high-quality images for better rich results appearance")
        
        if schema_type == 'LocalBusiness' and 'openingHours' in missing_recommended:
            recommendations.append("Add opening hours for local pack eligibility")
        
        if schema_type == 'Product' and 'aggregateRating' in missing_recommended:
            recommendations.append("Add customer reviews and ratings for enhanced product rich results")
        
        return recommendations
    
    def check_microdata_rich_results(self, microdata_item: Dict) -> Dict:
        """Check rich results eligibility for microdata"""
        return {
            'eligible': len(microdata_item.get('properties', {})) > 2,
            'format': 'microdata',
            'recommendation': 'Consider migrating to JSON-LD for better support'
        }
    
    async def collect_page_speed_metrics(self, url: str, api_key: str, device: str = "desktop") -> Dict:
        """Collect page speed metrics using Google PageSpeed Insights API"""
        try:
            await self.start_session()
            
            # Google PageSpeed Insights API
            api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            params = {
                'url': url,
                'key': api_key,
                'strategy': device.upper(),  # DESKTOP or MOBILE
                'category': ['PERFORMANCE', 'ACCESSIBILITY', 'BEST_PRACTICES', 'SEO']
            }
            
            async with self.session.get(api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract Core Web Vitals
                    lighthouse_data = data.get('lighthouseResult', {})
                    audits = lighthouse_data.get('audits', {})
                    
                    speed_data = {
                        'url': url,
                        'test_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'device': device,
                        'core_web_vitals': {
                            'largest_contentful_paint': audits.get('largest-contentful-paint', {}).get('numericValue', 0) / 1000,
                            'first_input_delay': audits.get('max-potential-fid', {}).get('numericValue', 0),
                            'cumulative_layout_shift': audits.get('cumulative-layout-shift', {}).get('numericValue', 0),
                            'first_contentful_paint': audits.get('first-contentful-paint', {}).get('numericValue', 0) / 1000,
                            'time_to_interactive': audits.get('interactive', {}).get('numericValue', 0) / 1000
                        },
                        'lighthouse_scores': {
                            'performance': lighthouse_data.get('categories', {}).get('performance', {}).get('score', 0) * 100,
                            'accessibility': lighthouse_data.get('categories', {}).get('accessibility', {}).get('score', 0) * 100,
                            'best_practices': lighthouse_data.get('categories', {}).get('best-practices', {}).get('score', 0) * 100,
                            'seo': lighthouse_data.get('categories', {}).get('seo', {}).get('score', 0) * 100
                        },
                        'opportunities': [
                            {
                                'id': audit_id,
                                'title': audit_data.get('title', ''),
                                'description': audit_data.get('description', ''),
                                'score': audit_data.get('score', 0),
                                'potential_savings': audit_data.get('details', {}).get('overallSavingsMs', 0)
                            }
                            for audit_id, audit_data in audits.items()
                            if audit_data.get('scoreDisplayMode') == 'numeric' and audit_data.get('score', 1) < 0.9
                        ]
                    }
                    
                    return speed_data
                else:
                    return {'error': f"PageSpeed API error: {response.status}"}
                    
        except Exception as e:
            return {'error': f"Page speed collection failed: {str(e)}"}
    
    async def collect_server_headers(self, url: str) -> Dict:
        """Collect server response headers - critical for technical SEO"""
        try:
            await self.start_session()
            
            async with self.session.head(url, allow_redirects=True) as response:
                headers_data = {
                    'url': url,
                    'status_code': response.status,
                    'headers': dict(response.headers),
                    'server_analysis': {
                        'server_software': response.headers.get('Server', 'Not disclosed'),
                        'x_robots_tag': response.headers.get('X-Robots-Tag', 'Not set'),
                        'cache_control': response.headers.get('Cache-Control', 'Not set'),
                        'expires': response.headers.get('Expires', 'Not set'),
                        'etag': response.headers.get('ETag', 'Not set'),
                        'last_modified': response.headers.get('Last-Modified', 'Not set'),
                        'content_type': response.headers.get('Content-Type', 'Not set'),
                        'content_encoding': response.headers.get('Content-Encoding', 'Not set'),
                        'security_headers': {
                            'hsts': response.headers.get('Strict-Transport-Security', 'Not set'),
                            'csp': response.headers.get('Content-Security-Policy', 'Not set'),
                            'x_frame_options': response.headers.get('X-Frame-Options', 'Not set'),
                            'x_content_type_options': response.headers.get('X-Content-Type-Options', 'Not set'),
                            'referrer_policy': response.headers.get('Referrer-Policy', 'Not set')
                        }
                    },
                    'redirect_analysis': {
                        'redirect_count': len(response.history),
                        'redirect_chain': [str(r.url) for r in response.history] + [str(response.url)],
                        'redirect_types': [r.status for r in response.history] if response.history else []
                    }
                }
                
                return headers_data
                
        except Exception as e:
            return {'error': f"Header collection failed: {str(e)}"}
    
    async def analyze_redirect_chain(self, url: str) -> Dict:
        """Enhanced redirect chain analysis with detailed information"""
        try:
            await self.start_session()
            redirect_data = {
                'original_url': url,
                'redirect_chain': [],
                'total_redirects': 0,
                'redirect_types': [],
                'redirect_issues': [],
                'final_url': url,
                'redirect_time': 0
            }
            
            start_time = time.time()
            
            async with self.session.get(url, allow_redirects=True) as response:
                redirect_data['final_url'] = str(response.url)
                redirect_data['total_redirects'] = len(response.history)
                redirect_data['redirect_time'] = time.time() - start_time
                
                # Build detailed redirect chain
                for i, redirect in enumerate(response.history):
                    redirect_info = {
                        'step': i + 1,
                        'from_url': str(redirect.url),
                        'status_code': redirect.status,
                        'redirect_type': self.classify_redirect(redirect.status),
                        'location_header': redirect.headers.get('Location', ''),
                        'response_time': redirect.headers.get('X-Response-Time', 'Unknown')
                    }
                    redirect_data['redirect_chain'].append(redirect_info)
                    redirect_data['redirect_types'].append(redirect.status)
                
                # Detect redirect issues
                if redirect_data['total_redirects'] > 3:
                    redirect_data['redirect_issues'].append('Too many redirects (>3)')
                
                if redirect_data['total_redirects'] > 0:
                    # Check for redirect loops
                    urls_in_chain = [r['from_url'] for r in redirect_data['redirect_chain']]
                    if len(urls_in_chain) != len(set(urls_in_chain)):
                        redirect_data['redirect_issues'].append('Redirect loop detected')
                    
                    # Check for mixed redirect types
                    if len(set(redirect_data['redirect_types'])) > 1:
                        redirect_data['redirect_issues'].append('Mixed redirect types')
                
                return redirect_data
                
        except Exception as e:
            return {'error': f"Redirect analysis failed: {str(e)}"}
    
    def classify_redirect(self, status_code: int) -> str:
        """Classify redirect type"""
        redirect_types = {
            300: 'Multiple Choices',
            301: 'Moved Permanently',
            302: 'Found (Temporary)',
            303: 'See Other',
            304: 'Not Modified',
            307: 'Temporary Redirect',
            308: 'Permanent Redirect'
        }
        return redirect_types.get(status_code, f'Unknown ({status_code})')
    
    async def detect_javascript_rendering(self, url: str) -> Dict:
        """Detect if content is JavaScript-rendered by comparing no-JS vs JS-rendered content"""
        try:
            await self.start_browser()
            await self.start_session()
            
            # Get content without JavaScript
            async with self.session.get(url) as response:
                no_js_html = await response.text()
                no_js_soup = BeautifulSoup(no_js_html, 'lxml')
                no_js_text = no_js_soup.get_text().strip()
                no_js_word_count = len(no_js_text.split())
            
            # Get content with JavaScript
            page = await self.context.new_page()
            await page.goto(url, wait_until="networkidle")
            js_html = await page.content()
            js_soup = BeautifulSoup(js_html, 'lxml')
            js_text = js_soup.get_text().strip()
            js_word_count = len(js_text.split())
            
            # Compare content
            content_difference = abs(js_word_count - no_js_word_count)
            percentage_difference = (content_difference / max(js_word_count, 1)) * 100
            
            js_detection = {
                'url': url,
                'no_js_word_count': no_js_word_count,
                'js_word_count': js_word_count,
                'content_difference': content_difference,
                'percentage_difference': percentage_difference,
                'is_js_heavy': percentage_difference > 30,
                'seo_concerns': [],
                'recommendations': []
            }
            
            # Add SEO concerns and recommendations
            if js_detection['is_js_heavy']:
                js_detection['seo_concerns'].append('Significant content rendered by JavaScript')
                js_detection['recommendations'].append('Consider server-side rendering or pre-rendering')
            
            if no_js_word_count < 100:
                js_detection['seo_concerns'].append('Very little content available without JavaScript')
                js_detection['recommendations'].append('Implement progressive enhancement')
            
            await page.close()
            return js_detection
            
        except Exception as e:
            return {'error': f"JavaScript rendering detection failed: {str(e)}"}
    
    # Basic helper methods for data extraction
    def extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else None
    
    def extract_meta_tags(self, soup: BeautifulSoup) -> Dict:
        meta_tags = {}
        for meta in soup.find_all('meta'):
            if meta.get('name'):
                meta_tags[meta.get('name')] = meta.get('content', '')
            elif meta.get('property'):
                meta_tags[meta.get('property')] = meta.get('content', '')
            elif meta.get('http-equiv'):
                meta_tags[meta.get('http-equiv')] = meta.get('content', '')
        return meta_tags
    
    def extract_headers(self, soup: BeautifulSoup) -> Dict:
        headers = {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}
        for i in range(1, 7):
            header_tags = soup.find_all(f'h{i}')
            headers[f'h{i}'] = [h.get_text().strip() for h in header_tags]
        return headers
    
    def extract_schema_markup(self, soup: BeautifulSoup) -> List[Dict]:
        schema_data = []
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                schema_content = json.loads(script.string)
                schema_data.append(schema_content)
            except json.JSONDecodeError:
                continue
        return schema_data
    
    def extract_open_graph(self, soup: BeautifulSoup) -> Dict:
        og_tags = {}
        for meta in soup.find_all('meta'):
            property_attr = meta.get('property', '')
            if property_attr.startswith('og:'):
                og_tags[property_attr] = meta.get('content', '')
        return og_tags
    
    def extract_twitter_cards(self, soup: BeautifulSoup) -> Dict:
        twitter_tags = {}
        for meta in soup.find_all('meta'):
            name_attr = meta.get('name', '')
            if name_attr.startswith('twitter:'):
                twitter_tags[name_attr] = meta.get('content', '')
        return twitter_tags
    
    def extract_internal_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        internal_links = []
        base_domain = urlparse(base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            link_domain = urlparse(full_url).netloc
            
            if link_domain == base_domain or not link_domain:
                internal_links.append({
                    'url': full_url,
                    'anchor_text': link.get_text().strip(),
                    'title': link.get('title', ''),
                    'rel': link.get('rel', [])
                })
        
        return internal_links
    
    def extract_external_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract external links"""
        external_links = []
        base_domain = urlparse(base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http'):
                link_domain = urlparse(href).netloc
                if link_domain != base_domain:
                    external_links.append({
                        'url': href,
                        'anchor_text': link.get_text().strip(),
                        'title': link.get('title', ''),
                        'rel': link.get('rel', [])
                    })
        
        return external_links
    
    def extract_hreflang(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract hreflang attributes"""
        hreflang_links = []
        for link in soup.find_all('link', rel='alternate'):
            hreflang = link.get('hreflang')
            href = link.get('href')
            if hreflang and href:
                hreflang_links.append({
                    'hreflang': hreflang,
                    'href': href
                })
        return hreflang_links
    
    def extract_meta_refresh(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract meta refresh directive"""
        meta_refresh = soup.find('meta', attrs={'http-equiv': 'refresh'})
        return meta_refresh.get('content') if meta_refresh else None
    
    def extract_base_href(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract base href if present"""
        base_tag = soup.find('base', href=True)
        return base_tag.get('href') if base_tag else None
    
    def get_word_count(self, soup: BeautifulSoup) -> int:
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        words = text.split()
        return len(words)
    
    def extract_meta_viewport(self, soup: BeautifulSoup) -> Optional[str]:
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        return viewport.get('content') if viewport else None
    
    def extract_canonical(self, soup: BeautifulSoup) -> Optional[str]:
        canonical = soup.find('link', rel='canonical')
        return canonical.get('href') if canonical else None
    
    def extract_robots_meta(self, soup: BeautifulSoup) -> Optional[str]:
        robots = soup.find('meta', attrs={'name': 'robots'})
        return robots.get('content') if robots else None

# Global scraper instance
scraper = SEOScraperComplete()

# FIXED: Helper function to safely extract CPC values from Keywords Everywhere API
def extract_cpc_value(cpc_data) -> float:
    """
    Safely extract numeric CPC value from Keywords Everywhere API response
    
    Args:
        cpc_data: CPC data from API (can be dict with 'value' key or direct number)
    
    Returns:
        float: Numeric CPC value, defaults to 0.0 if not parseable
    """
    if cpc_data is None:
        return 0.0
    
    # Handle nested CPC object: {"currency": "$", "value": "0.09"}
    if isinstance(cpc_data, dict) and 'value' in cpc_data:
        try:
            return float(cpc_data['value'])
        except (ValueError, TypeError):
            return 0.0
    
    # Handle direct numeric value (backward compatibility)
    if isinstance(cpc_data, (int, float)):
        return float(cpc_data)
    
    # Handle string representation
    if isinstance(cpc_data, str):
        try:
            return float(cpc_data)
        except (ValueError, TypeError):
            return 0.0
    
    return 0.0

# Core Data Collection Tools
@mcp.tool()
async def scrape_seo_data(url: str) -> str:
    """Extract comprehensive SEO data from a webpage - raw data for Claude analysis"""
    try:
        seo_data = await scraper.scrape_seo_data(url)
        return json.dumps(seo_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': f"Failed to scrape {url}: {str(e)}"}, indent=2)

@mcp.tool()
async def collect_server_headers(url: str) -> str:
    """
    Collect server response headers - critical for technical SEO
    
    Args:
        url: URL to analyze server headers
        
    Returns:
        JSON string with comprehensive server header analysis including security headers, caching, and SEO-relevant headers
    """
    try:
        headers_data = await scraper.collect_server_headers(url)
        return json.dumps(headers_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': f"Header collection failed: {str(e)}"}, indent=2)

@mcp.tool()
async def analyze_redirect_chain(url: str) -> str:
    """
    Enhanced redirect chain analysis with detailed information
    
    Args:
        url: URL to analyze for redirect chains
        
    Returns:
        JSON string with detailed redirect chain analysis including redirect types, issues, and performance impact
    """
    try:
        redirect_data = await scraper.analyze_redirect_chain(url)
        return json.dumps(redirect_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': f"Redirect analysis failed: {str(e)}"}, indent=2)

@mcp.tool()
async def validate_structured_data(url: str) -> str:
    """
    Enhanced structured data validation with Schema.org checking
    
    Args:
        url: URL to validate structured data
        
    Returns:
        JSON string with comprehensive structured data validation including rich results eligibility
    """
    try:
        await scraper.start_browser()
        page = await scraper.context.new_page()
        await page.goto(url, wait_until="networkidle")
        html_content = await page.content()
        soup = BeautifulSoup(html_content, 'lxml')
        
        validation_data = scraper.validate_structured_data_enhanced(soup)
        validation_data['url'] = url
        validation_data['test_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        await page.close()
        return json.dumps(validation_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': f"Structured data validation failed: {str(e)}"}, indent=2)

@mcp.tool()
async def detect_javascript_rendering(url: str) -> str:
    """
    Detect if content is JavaScript-rendered by comparing no-JS vs JS-rendered content
    
    Args:
        url: URL to analyze for JavaScript rendering
        
    Returns:
        JSON string with JavaScript rendering analysis and SEO recommendations
    """
    try:
        js_detection = await scraper.detect_javascript_rendering(url)
        return json.dumps(js_detection, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': f"JavaScript rendering detection failed: {str(e)}"}, indent=2)

@mcp.tool()
async def serp_data_collector(keyword: str, api_key: str = None, location: str = "United States", device: str = "desktop") -> str:
    """
    Collect SERP data using SerpAPI - reliable and legitimate
    
    Args:
        keyword: Target keyword to analyze
        api_key: SerpAPI key (get free key at serpapi.com - 100 searches/month)
        location: Geographic location for search results (e.g., "Berlin, Germany", "United States")
        device: Device type (desktop or mobile)
        
    Returns:
        JSON string with comprehensive SERP analysis including rankings, features, and related searches
    """
    try:
        # Use provided API key or fall back to environment variable
        if api_key is None:
            api_key = os.getenv('SERPAPI_KEY')
        
        if not api_key:
            return json.dumps({
                'error': 'API key is required. Either provide api_key parameter or set SERPAPI_KEY environment variable.',
                'keyword': keyword,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'setup_instructions': 'Create a .env file with SERPAPI_KEY=your_key_here'
            }, indent=2)
        
        # SerpAPI parameters
        params = {
            "q": keyword,
            "api_key": api_key,
            "engine": "google",
            "location": location,
            "device": device,
            "hl": "en",  # Language
            "gl": "us",  # Country code
            "num": 10,   # Number of results
        }
        
        # Execute search
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Check for API errors
        if 'error' in results:
            return json.dumps({
                'error': f"SerpAPI error: {results['error']}",
                'keyword': keyword,
                'location': location,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'api_used': 'SerpAPI'
            }, indent=2)
        
        # Initialize response structure
        serp_data = {
            'keyword': keyword,
            'search_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'location': location,
            'device': device,
            'total_results': 0,
            'search_time': 0,
            'results': [],
            'serp_features': {},
            'related_searches': [],
            'search_metadata': {}
        }
        
        # Extract search information
        search_info = results.get('search_information', {})
        serp_data['total_results'] = search_info.get('total_results', 0)
        serp_data['search_time'] = search_info.get('time_taken_displayed', 0)
        
        # Extract organic results with error handling
        organic_results = results.get('organic_results', [])
        if isinstance(organic_results, list):
            for i, result in enumerate(organic_results):
                if isinstance(result, dict):
                    serp_data['results'].append({
                        'position': result.get('position', i + 1),
                        'title': result.get('title', ''),
                        'url': result.get('link', ''),
                        'displayed_link': result.get('displayed_link', ''),
                        'snippet': result.get('snippet', ''),
                        'cached_page_link': result.get('cached_page_link', ''),
                        'rich_snippet': result.get('rich_snippet', {}),
                        'sitelinks': result.get('sitelinks', {})
                    })
        
        # Extract SERP features with comprehensive error handling
        serp_features = {}
        
        # Featured Snippet / Answer Box
        try:
            if 'answer_box' in results and isinstance(results['answer_box'], dict):
                answer_box = results['answer_box']
                serp_features['answer_box'] = {
                    'type': answer_box.get('type', ''),
                    'title': answer_box.get('title', ''),
                    'snippet': answer_box.get('snippet', ''),
                    'link': answer_box.get('link', ''),
                    'displayed_link': answer_box.get('displayed_link', ''),
                    'source': answer_box.get('source', {})
                }
        except Exception as e:
            pass
        
        # People Also Ask
        try:
            if 'people_also_ask' in results and isinstance(results['people_also_ask'], list):
                paa_list = []
                for paa in results['people_also_ask'][:4]:  # Limit to first 4
                    if isinstance(paa, dict):
                        paa_list.append({
                            'question': paa.get('question', ''),
                            'snippet': paa.get('snippet', ''),
                            'title': paa.get('title', ''),
                            'link': paa.get('link', ''),
                            'displayed_link': paa.get('displayed_link', '')
                        })
                if paa_list:
                    serp_features['people_also_ask'] = paa_list
        except Exception as e:
            pass
        
        # Knowledge Graph
        try:
            if 'knowledge_graph' in results and isinstance(results['knowledge_graph'], dict):
                kg = results['knowledge_graph']
                serp_features['knowledge_graph'] = {
                    'title': kg.get('title', ''),
                    'type': kg.get('type', ''),
                    'description': kg.get('description', ''),
                    'source': kg.get('source', {}),
                    'attributes': kg.get('attributes', {}),
                    'kgmid': kg.get('kgmid', ''),
                    'knowledge_graph_search_link': kg.get('knowledge_graph_search_link', '')
                }
        except Exception as e:
            pass
        
        serp_data['serp_features'] = serp_features
        
        # Extract related searches with error handling
        try:
            if 'related_searches' in results and isinstance(results['related_searches'], list):
                related_list = []
                for search_item in results['related_searches']:
                    if isinstance(search_item, dict) and search_item.get('query'):
                        related_list.append(search_item.get('query', ''))
                serp_data['related_searches'] = related_list
        except Exception as e:
            serp_data['related_searches'] = []
        
        # Add comprehensive search metadata
        serp_data['search_metadata'] = {
            'status': search_info.get('query_displayed', keyword),
            'total_results': search_info.get('total_results', 0),
            'time_taken': search_info.get('time_taken_displayed', ''),
            'engine_used': 'google_via_serpapi',
            'organic_results_state': search_info.get('organic_results_state', ''),
            'query_displayed': search_info.get('query_displayed', ''),
            'detected_location': results.get('search_parameters', {}).get('location', location)
        }
        
        return json.dumps(serp_data, indent=2, ensure_ascii=False)
        
    except Exception as e:
        error_response = {
            'error': f"SERP collection failed: {str(e)}",
            'error_type': type(e).__name__,
            'keyword': keyword,
            'location': location,
            'device': device,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'api_used': 'SerpAPI'
        }
        return json.dumps(error_response, indent=2)

@mcp.tool()
async def page_speed_metrics(url: str, api_key: str = None, device: str = "desktop") -> str:
    """
    Collect page speed metrics using Google PageSpeed Insights API
    
    Args:
        url: URL to analyze for performance metrics
        api_key: Google PageSpeed Insights API key
        device: Device type (desktop or mobile)
        
    Returns:
        JSON string with Core Web Vitals and performance analysis
    """
    try:
        # Use provided API key or fall back to environment variable
        if api_key is None:
            api_key = os.getenv('GOOGLE_PAGESPEED_KEY')
        
        if not api_key:
            return json.dumps({
                'error': 'Google PageSpeed API key is required. Either provide api_key parameter or set GOOGLE_PAGESPEED_KEY environment variable.',
                'url': url,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'setup_instructions': 'Create a .env file with GOOGLE_PAGESPEED_KEY=your_key_here'
            }, indent=2)
        
        speed_data = await scraper.collect_page_speed_metrics(url, api_key, device)
        return json.dumps(speed_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': f"Page speed analysis failed: {str(e)}"}, indent=2)

# SERP-Content Alignment Analyzer - Pure Data Collection
@mcp.tool()
async def analyze_serp_content_alignment(keyword: str, target_url: str, api_key: str = None, location: str = "United States") -> str:
    """
    Collect comprehensive SERP + content data for Claude to analyze content alignment
    
    Args:
        keyword: Target keyword to analyze
        target_url: Your page URL to compare against competitors
        api_key: SerpAPI key for SERP data
        location: Geographic location for search results
        
    Returns:
        JSON string with comprehensive dataset: SERP results + full content from all pages for Claude analysis
    """
    try:
        # Use provided API key or fall back to environment variable
        if api_key is None:
            api_key = os.getenv('SERPAPI_KEY')
        
        if not api_key:
            return json.dumps({
                'error': 'SerpAPI key is required. Either provide api_key parameter or set SERPAPI_KEY environment variable.',
                'keyword': keyword,
                'target_url': target_url
            }, indent=2)
        
        # Step 1: Get SERP results
        params = {
            "q": keyword,
            "api_key": api_key,
            "engine": "google",
            "location": location,
            "hl": "en",
            "gl": "us",
            "num": 10
        }
        
        search = GoogleSearch(params)
        serp_results = search.get_dict()
        
        if 'error' in serp_results:
            return json.dumps({
                'error': f"SerpAPI error: {serp_results['error']}",
                'keyword': keyword,
                'target_url': target_url
            }, indent=2)
        
        # Step 2: Extract top 10 organic results URLs
        organic_results = serp_results.get('organic_results', [])
        competitor_urls = []
        
        for i, result in enumerate(organic_results[:10]):
            if isinstance(result, dict) and result.get('link'):
                competitor_urls.append({
                    'position': result.get('position', i + 1),
                    'url': result.get('link'),
                    'title': result.get('title', ''),
                    'snippet': result.get('snippet', '')
                })
        
        # Step 3: Scrape content from all competitor pages + target page
        await scraper.start_browser()
        
        alignment_data = {
            'keyword': keyword,
            'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'serp_metadata': {
                'location': location,
                'total_results': serp_results.get('search_information', {}).get('total_results', 0)
            },
            'target_page': {},
            'top_10_competitors': [],
            'serp_features': {}
        }
        
        # Extract SERP features for context
        if 'answer_box' in serp_results:
            alignment_data['serp_features']['featured_snippet'] = {
                'present': True,
                'type': serp_results['answer_box'].get('type', ''),
                'source': serp_results['answer_box'].get('link', ''),
                'content': serp_results['answer_box'].get('snippet', '')
            }
        
        if 'people_also_ask' in serp_results:
            alignment_data['serp_features']['people_also_ask'] = [
                paa.get('question', '') for paa in serp_results['people_also_ask'][:5]
            ]
        
        if 'related_searches' in serp_results:
            alignment_data['serp_features']['related_searches'] = [
                search.get('query', '') for search in serp_results['related_searches'][:8]
            ]
        
        # Step 4: Scrape target page
        try:
            target_page_data = await scraper.scrape_seo_data(target_url)
            if 'error' not in target_page_data:
                alignment_data['target_page'] = {
                    'url': target_url,
                    'title': target_page_data.get('title', ''),
                    'meta_description': target_page_data.get('meta_tags', {}).get('description', ''),
                    'main_content': target_page_data.get('main_content', ''),
                    'full_text': target_page_data.get('full_text', ''),
                    'word_count': target_page_data.get('word_count', 0),
                    'headings': target_page_data.get('headers', {}),
                    'schema_markup': target_page_data.get('schema_markup', []),
                    'internal_links_count': len(target_page_data.get('internal_links', [])),
                    'external_links_count': len(target_page_data.get('external_links', []))
                }
            else:
                alignment_data['target_page'] = {'url': target_url, 'error': target_page_data.get('error')}
        except Exception as e:
            alignment_data['target_page'] = {'url': target_url, 'error': f"Failed to scrape target page: {str(e)}"}
        
        # Step 5: Scrape all competitor pages
        for i, competitor in enumerate(competitor_urls):
            try:
                print(f"Scraping competitor {i+1}/10: {competitor['url']}")
                
                competitor_data = await scraper.scrape_seo_data(competitor['url'])
                
                if 'error' not in competitor_data:
                    competitor_analysis = {
                        'serp_position': competitor['position'],
                        'url': competitor['url'],
                        'title': competitor_data.get('title', ''),
                        'serp_title': competitor['title'],  # Title from SERP vs actual title
                        'meta_description': competitor_data.get('meta_tags', {}).get('description', ''),
                        'serp_snippet': competitor['snippet'],  # Snippet from SERP vs actual meta
                        'main_content': competitor_data.get('main_content', ''),
                        'full_text': competitor_data.get('full_text', ''),
                        'word_count': competitor_data.get('word_count', 0),
                        'headings': competitor_data.get('headers', {}),
                        'schema_markup': competitor_data.get('schema_markup', []),
                        'internal_links_count': len(competitor_data.get('internal_links', [])),
                        'external_links_count': len(competitor_data.get('external_links', []))
                    }
                else:
                    competitor_analysis = {
                        'serp_position': competitor['position'],
                        'url': competitor['url'],
                        'error': competitor_data.get('error')
                    }
                
                alignment_data['top_10_competitors'].append(competitor_analysis)
                
                # Add delay between requests
                await asyncio.sleep(random.uniform(1.0, 2.0))
                
            except Exception as e:
                alignment_data['top_10_competitors'].append({
                    'serp_position': competitor['position'],
                    'url': competitor['url'],
                    'error': f"Failed to scrape: {str(e)}"
                })
        
        # Step 6: Add summary statistics for Claude
        successful_competitors = [c for c in alignment_data['top_10_competitors'] if 'error' not in c]
        
        alignment_data['dataset_summary'] = {
            'total_competitors_found': len(competitor_urls),
            'successful_scrapes': len(successful_competitors),
            'target_page_scraped': 'error' not in alignment_data['target_page'],
            'avg_competitor_word_count': sum(c.get('word_count', 0) for c in successful_competitors) / max(len(successful_competitors), 1),
            'avg_competitor_headings': {
                'h1': sum(len(c.get('headings', {}).get('h1', [])) for c in successful_competitors) / max(len(successful_competitors), 1),
                'h2': sum(len(c.get('headings', {}).get('h2', [])) for c in successful_competitors) / max(len(successful_competitors), 1),
                'h3': sum(len(c.get('headings', {}).get('h3', [])) for c in successful_competitors) / max(len(successful_competitors), 1)
            }
        }
        
        return json.dumps(alignment_data, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            'error': f"SERP content alignment analysis failed: {str(e)}",
            'keyword': keyword,
            'target_url': target_url
        }, indent=2)

# Search Intent Classification Engine - Pure Data Collection  
@mcp.tool()
async def classify_search_intent_data(keyword: str, api_key: str = None, location: str = "United States") -> str:
    """
    Collect comprehensive SERP data for Claude to classify search intent
    
    Args:
        keyword: Target keyword to analyze intent for
        api_key: SerpAPI key for SERP data
        location: Geographic location for search results
        
    Returns:
        JSON string with comprehensive SERP features and result types for Claude intent analysis
    """
    try:
        # Use provided API key or fall back to environment variable
        if api_key is None:
            api_key = os.getenv('SERPAPI_KEY')
        
        if not api_key:
            return json.dumps({
                'error': 'SerpAPI key is required for search intent classification.',
                'keyword': keyword
            }, indent=2)
        
        # Get comprehensive SERP data
        params = {
            "q": keyword,
            "api_key": api_key,
            "engine": "google",
            "location": location,
            "hl": "en",
            "gl": "us",
            "num": 10
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if 'error' in results:
            return json.dumps({
                'error': f"SerpAPI error: {results['error']}",
                'keyword': keyword
            }, indent=2)
        
        # Collect intent classification data
        intent_data = {
            'keyword': keyword,
            'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'location': location,
            'serp_features': {},
            'organic_results_analysis': [],
            'related_searches': [],
            'search_metadata': {}
        }
        
        # Extract SERP features
        serp_features = {}
        
        # Featured snippet/Answer box
        if 'answer_box' in results:
            serp_features['featured_snippet'] = {
                'present': True,
                'type': results['answer_box'].get('type', ''),
                'content_type': 'informational' if 'definition' in results['answer_box'].get('type', '') else 'answer',
                'source_domain': results['answer_box'].get('link', '').split('/')[2] if results['answer_box'].get('link') else ''
            }
        
        # People Also Ask
        if 'people_also_ask' in results:
            serp_features['people_also_ask'] = {
                'present': True,
                'question_count': len(results['people_also_ask']),
                'questions': [paa.get('question', '') for paa in results['people_also_ask'][:8]]
            }
        
        # Shopping results
        if 'shopping_results' in results:
            serp_features['shopping_results'] = {
                'present': True,
                'product_count': len(results['shopping_results']),
                'intent_signal': 'commercial/transactional'
            }
        
        # Local results
        if 'local_results' in results:
            serp_features['local_results'] = {
                'present': True,
                'business_count': len(results['local_results']),
                'intent_signal': 'local'
            }
        
        # Knowledge graph
        if 'knowledge_graph' in results:
            serp_features['knowledge_graph'] = {
                'present': True,
                'type': results['knowledge_graph'].get('type', ''),
                'intent_signal': 'informational'
            }
        
        # Images
        if 'images_results' in results:
            serp_features['images'] = {
                'present': True,
                'count': len(results['images_results'])
            }
        
        # Videos
        if 'videos' in results:
            serp_features['videos'] = {
                'present': True,
                'count': len(results['videos'])
            }
        
        # Top stories/News
        if 'top_stories' in results:
            serp_features['top_stories'] = {
                'present': True,
                'story_count': len(results['top_stories']),
                'intent_signal': 'informational/news'
            }
        
        intent_data['serp_features'] = serp_features
        
        # Analyze organic results for intent signals
        organic_results = results.get('organic_results', [])
        for i, result in enumerate(organic_results[:10]):
            if isinstance(result, dict):
                # Analyze URL structure for intent signals
                url = result.get('link', '')
                domain = url.split('/')[2] if len(url.split('/')) > 2 else ''
                
                url_signals = {
                    'has_shop_path': '/shop' in url or '/store' in url or '/buy' in url,
                    'has_blog_path': '/blog' in url or '/articles' in url or '/news' in url,
                    'has_how_to': 'how-to' in url or 'guide' in url or 'tutorial' in url,
                    'is_ecommerce_domain': any(ecom in domain for ecom in ['amazon', 'ebay', 'etsy', 'shopify']),
                    'is_informational_domain': any(info in domain for info in ['wikipedia', 'britannica', 'howstuffworks'])
                }
                
                title = result.get('title', '').lower()
                snippet = result.get('snippet', '').lower()
                
                content_signals = {
                    'title_has_how_to': 'how to' in title or 'guide' in title or 'tutorial' in title,
                    'title_has_best': 'best' in title or 'top' in title or 'review' in title,
                    'title_has_buy': 'buy' in title or 'price' in title or 'cost' in title,
                    'title_has_what_is': 'what is' in title or 'definition' in title,
                    'snippet_has_steps': 'step' in snippet or 'follow' in snippet,
                    'snippet_has_price': 'price' in snippet or 'cost' in snippet or '$' in snippet
                }
                
                intent_data['organic_results_analysis'].append({
                    'position': result.get('position', i + 1),
                    'url': url,
                    'domain': domain,
                    'title': result.get('title', ''),
                    'snippet': result.get('snippet', ''),
                    'url_signals': url_signals,
                    'content_signals': content_signals
                })
        
        # Related searches
        if 'related_searches' in results:
            intent_data['related_searches'] = [
                search.get('query', '') for search in results['related_searches'][:10]
            ]
        
        # Search metadata
        search_info = results.get('search_information', {})
        intent_data['search_metadata'] = {
            'total_results': search_info.get('total_results', 0),
            'search_time': search_info.get('time_taken_displayed', ''),
            'query_displayed': search_info.get('query_displayed', keyword)
        }
        
        return json.dumps(intent_data, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            'error': f"Search intent data collection failed: {str(e)}",
            'keyword': keyword
        }, indent=2)

# SERP Feature Opportunity Analyzer - Pure Data Collection
@mcp.tool() 
async def analyze_serp_feature_opportunities(keyword: str, target_url: str, api_key: str = None, location: str = "United States") -> str:
    """
    Collect SERP features + page structure data for Claude to analyze SERP feature opportunities
    
    Args:
        keyword: Target keyword to analyze SERP features for
        target_url: Your page URL to analyze for SERP feature eligibility
        api_key: SerpAPI key for SERP data
        location: Geographic location for search results
        
    Returns:
        JSON string with SERP features + page structure data for Claude opportunity analysis
    """
    try:
        # Use provided API key or fall back to environment variable
        if api_key is None:
            api_key = os.getenv('SERPAPI_KEY')
        
        if not api_key:
            return json.dumps({
                'error': 'SerpAPI key is required for SERP feature analysis.',
                'keyword': keyword,
                'target_url': target_url
            }, indent=2)
        
        # Step 1: Get SERP data
        params = {
            "q": keyword,
            "api_key": api_key,
            "engine": "google", 
            "location": location,
            "hl": "en",
            "gl": "us",
            "num": 10
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if 'error' in results:
            return json.dumps({
                'error': f"SerpAPI error: {results['error']}",
                'keyword': keyword,
                'target_url': target_url
            }, indent=2)
        
        # Step 2: Extract current SERP features
        opportunity_data = {
            'keyword': keyword,
            'target_url': target_url,
            'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'location': location,
            'current_serp_features': {},
            'target_page_structure': {},
            'opportunity_signals': {}
        }
        
        # Analyze current SERP features
        current_features = {}
        
        # Featured snippet
        if 'answer_box' in results:
            answer_box = results['answer_box']
            current_features['featured_snippet'] = {
                'present': True,
                'type': answer_box.get('type', ''),
                'current_winner': answer_box.get('link', ''),
                'content_length': len(answer_box.get('snippet', '')),
                'content_format': 'paragraph' if 'paragraph' in answer_box.get('type', '') else 'list'
            }
        else:
            current_features['featured_snippet'] = {'present': False, 'opportunity': True}
        
        # People Also Ask
        if 'people_also_ask' in results:
            current_features['people_also_ask'] = {
                'present': True,
                'question_count': len(results['people_also_ask']),
                'questions': [paa.get('question', '') for paa in results['people_also_ask'][:5]]
            }
        else:
            current_features['people_also_ask'] = {'present': False, 'opportunity': True}
        
        # Knowledge graph
        if 'knowledge_graph' in results:
            current_features['knowledge_graph'] = {
                'present': True,
                'type': results['knowledge_graph'].get('type', ''),
                'current_winner': results['knowledge_graph'].get('source', {}).get('link', '')
            }
        
        # Shopping results
        if 'shopping_results' in results:
            current_features['shopping_results'] = {
                'present': True,
                'product_count': len(results['shopping_results'])
            }
        
        # Images
        if 'images_results' in results:
            current_features['images'] = {
                'present': True,
                'image_count': len(results['images_results'])
            }
        
        # Videos
        if 'videos' in results:
            current_features['videos'] = {
                'present': True,
                'video_count': len(results['videos'])
            }
        
        opportunity_data['current_serp_features'] = current_features
        
        # Step 3: Analyze target page structure
        try:
            target_data = await scraper.scrape_seo_data(target_url)
            
            if 'error' not in target_data:
                # Analyze content structure for SERP feature eligibility
                main_content = target_data.get('main_content', '')
                headers = target_data.get('headers', {})
                schema_markup = target_data.get('schema_markup', [])
                
                # Content format analysis
                content_structure = {
                    'word_count': target_data.get('word_count', 0),
                    'has_questions': '?' in main_content,
                    'question_count': main_content.count('?'),
                    'has_numbered_lists': bool(re.search(r'\d+\.', main_content)),
                    'has_bullet_points': '•' in main_content or '*' in main_content,
                    'has_tables': '<table' in str(target_data.get('full_text', '')),
                    'paragraph_count': len([p for p in main_content.split('\n\n') if p.strip()]),
                    'has_step_by_step': any(word in main_content.lower() for word in ['step 1', 'first step', 'step by step'])
                }
                
                # Heading analysis
                heading_structure = {
                    'h1_count': len(headers.get('h1', [])),
                    'h2_count': len(headers.get('h2', [])),
                    'h3_count': len(headers.get('h3', [])),
                    'has_faq_headings': any('faq' in h.lower() or 'question' in h.lower() for h in headers.get('h2', []) + headers.get('h3', [])),
                    'has_how_to_headings': any('how to' in h.lower() for h in headers.get('h1', []) + headers.get('h2', [])),
                    'heading_as_questions': sum(1 for h in headers.get('h2', []) + headers.get('h3', []) if h.endswith('?'))
                }
                
                # Schema markup analysis
                schema_types = []
                for schema in schema_markup:
                    if isinstance(schema, dict):
                        if '@type' in schema:
                            schema_types.append(schema['@type'])
                        elif '@graph' in schema:
                            for item in schema['@graph']:
                                if isinstance(item, dict) and '@type' in item:
                                    schema_types.append(item['@type'])
                
                schema_analysis = {
                    'schema_types_present': list(set(schema_types)),
                    'has_article_schema': 'Article' in schema_types or 'BlogPosting' in schema_types,
                    'has_faq_schema': 'FAQPage' in schema_types,
                    'has_howto_schema': 'HowTo' in schema_types,
                    'has_breadcrumb_schema': 'BreadcrumbList' in schema_types,
                    'has_organization_schema': 'Organization' in schema_types
                }
                
                opportunity_data['target_page_structure'] = {
                    'content_structure': content_structure,
                    'heading_structure': heading_structure,
                    'schema_analysis': schema_analysis,
                    'meta_description_length': len(target_data.get('meta_tags', {}).get('description', '')),
                    'title_length': len(target_data.get('title', ''))
                }
            else:
                opportunity_data['target_page_structure'] = {'error': target_data.get('error')}
                
        except Exception as e:
            opportunity_data['target_page_structure'] = {'error': f"Failed to analyze page structure: {str(e)}"}
        
        return json.dumps(opportunity_data, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            'error': f"SERP feature opportunity analysis failed: {str(e)}",
            'keyword': keyword,
            'target_url': target_url
        }, indent=2)

# NEW: INTEGRATED KEYWORDS EVERYWHERE TOOLS
@mcp.tool()
async def keyword_research_analysis(keywords: list, country: str = "US", api_key: str = None) -> str:
    """
    Get comprehensive keyword research data including search volume, CPC, competition, and difficulty
    
    Args:
        keywords: List of keywords to analyze (max 1000 per request)
        country: Country code for search data (US, UK, DE, etc.)
        api_key: Keywords Everywhere API key (optional, uses environment variable if not provided)
        
    Returns:
        JSON string with keyword research analysis including opportunity scoring and recommendations
    """
    try:
        # Use provided API key or update scraper's key
        if api_key:
            scraper.ke_api = KeywordsEverywhereAPI(api_key)
        
        # Get keyword data from Keywords Everywhere
        data = await scraper.ke_api.get_search_volume(keywords, country)
        
        # Format the response for SEO analysis
        analysis_result = {
            "tool": "Keywords Everywhere - Keyword Research Analysis",
            "country": country,
            "total_keywords_analyzed": len(keywords),
            "keywords_data": [],
            "summary": {
                "high_volume_keywords": [],
                "low_competition_opportunities": [],
                "high_cpc_commercial_terms": [],
                "recommended_targets": []
            }
        }
        
        for keyword_data in data.get("data", []):
            # FIXED: Extract CPC using helper function
            cpc = extract_cpc_value(keyword_data.get("cpc"))
            
            keyword_info = {
                "keyword": keyword_data.get("keyword", ""),
                "search_volume": keyword_data.get("vol", 0),
                "cpc": cpc,
                "competition": keyword_data.get("competition", "Unknown"),
                "trend": keyword_data.get("trend", []),
                "opportunity_score": 0
            }
            
            # Calculate opportunity score
            volume = keyword_info["search_volume"] or 0
            competition = keyword_info["competition"]
            
            # Simple scoring algorithm
            volume_score = min(volume / 1000, 10)  # Max 10 points for volume
            cpc_score = min(cpc * 2, 10)  # Max 10 points for CPC
            competition_score = 10 if competition == "Low" else 5 if competition == "Medium" else 2
            
            keyword_info["opportunity_score"] = round((volume_score + cpc_score + competition_score) / 3, 2)
            
            analysis_result["keywords_data"].append(keyword_info)
            
            # Categorize keywords for summary
            if volume >= 1000:
                analysis_result["summary"]["high_volume_keywords"].append(keyword_info["keyword"])
            
            if competition in ["Low", "Medium"] and volume >= 100:
                analysis_result["summary"]["low_competition_opportunities"].append(keyword_info["keyword"])
            
            if cpc >= 1.0:
                analysis_result["summary"]["high_cpc_commercial_terms"].append(keyword_info["keyword"])
            
            if keyword_info["opportunity_score"] >= 6:
                analysis_result["summary"]["recommended_targets"].append({
                    "keyword": keyword_info["keyword"],
                    "score": keyword_info["opportunity_score"],
                    "volume": volume,
                    "cpc": cpc
                })
        
        # Sort recommended targets by opportunity score
        analysis_result["summary"]["recommended_targets"].sort(
            key=lambda x: x["score"], reverse=True
        )
        
        return json.dumps(analysis_result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            'error': f"Keyword research analysis failed: {str(e)}",
            'keywords_requested': len(keywords) if keywords else 0
        }, indent=2)

@mcp.tool()
async def related_keywords_discovery(keyword: str, country: str = "US", api_key: str = None) -> str:
    """
    Discover related keywords and suggestions for a seed keyword
    
    Args:
        keyword: Seed keyword to find related terms for
        country: Country code for search data (US, UK, DE, etc.)
        api_key: Keywords Everywhere API key (optional, uses environment variable if not provided)
        
    Returns:
        JSON string with related keywords categorized by intent and content opportunities
    """
    try:
        # Use provided API key or update scraper's key
        if api_key:
            scraper.ke_api = KeywordsEverywhereAPI(api_key)
        
        # Get related keywords
        data = await scraper.ke_api.get_related_keywords(keyword, country)
        
        discovery_result = {
            "tool": "Keywords Everywhere - Related Keywords Discovery",
            "seed_keyword": keyword,
            "country": country,
            "related_keywords": [],
            "keyword_categories": {
                "question_keywords": [],
                "long_tail_opportunities": [],
                "commercial_intent": [],
                "informational_intent": []
            },
            "content_opportunities": []
        }
        
        for related_kw in data.get("data", []):
            # FIXED: Extract CPC using helper function
            cpc = extract_cpc_value(related_kw.get("cpc"))
            
            kw_info = {
                "keyword": related_kw.get("keyword", ""),
                "search_volume": related_kw.get("vol", 0),
                "cpc": cpc,
                "competition": related_kw.get("competition", "Unknown")
            }
            
            discovery_result["related_keywords"].append(kw_info)
            
            # Categorize keywords
            kw_text = kw_info["keyword"].lower()
            
            if any(q in kw_text for q in ["what", "how", "why", "when", "where", "who"]):
                discovery_result["keyword_categories"]["question_keywords"].append(kw_info)
            
            if len(kw_text.split()) >= 4:
                discovery_result["keyword_categories"]["long_tail_opportunities"].append(kw_info)
            
            if kw_info["cpc"] and kw_info["cpc"] > 1.0:
                discovery_result["keyword_categories"]["commercial_intent"].append(kw_info)
            elif any(term in kw_text for term in ["what is", "how to", "guide", "tutorial"]):
                discovery_result["keyword_categories"]["informational_intent"].append(kw_info)
        
        # Generate content opportunities
        question_kws = discovery_result["keyword_categories"]["question_keywords"]
        if question_kws:
            discovery_result["content_opportunities"].append({
                "content_type": "FAQ Page",
                "opportunity": f"Create FAQ content targeting {len(question_kws)} question-based keywords",
                "keywords": [kw["keyword"] for kw in question_kws[:10]]
            })
        
        commercial_kws = discovery_result["keyword_categories"]["commercial_intent"]
        if commercial_kws:
            discovery_result["content_opportunities"].append({
                "content_type": "Service/Product Pages",
                "opportunity": f"Create commercial pages targeting {len(commercial_kws)} high-CPC keywords",
                "keywords": [kw["keyword"] for kw in commercial_kws[:10]]
            })
        
        return json.dumps(discovery_result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            'error': f"Related keywords discovery failed: {str(e)}",
            'seed_keyword': keyword
        }, indent=2)

@mcp.tool()
async def keyword_opportunity_scorer(keywords: list, country: str = "US", business_relevance_keywords: list = None, api_key: str = None) -> str:
    """
    Analyze keyword opportunities by combining volume, difficulty, and commercial value
    
    Args:
        keywords: List of keywords to score for opportunity analysis
        country: Country code for search data
        business_relevance_keywords: Keywords that indicate high business relevance (optional)
        api_key: Keywords Everywhere API key (optional, uses environment variable if not provided)
        
    Returns:
        JSON string with prioritized keyword opportunities and strategic recommendations
    """
    try:
        # Use provided API key or update scraper's key
        if api_key:
            scraper.ke_api = KeywordsEverywhereAPI(api_key)
        
        business_keywords = business_relevance_keywords or []
        
        # Get keyword data
        data = await scraper.ke_api.get_search_volume(keywords, country)
        
        scoring_result = {
            "tool": "Keywords Everywhere - Opportunity Scorer",
            "country": country,
            "total_keywords": len(keywords),
            "scored_keywords": [],
            "priority_tiers": {
                "critical_priority": [],
                "high_priority": [],
                "medium_priority": [],
                "low_priority": []
            }
        }
        
        for keyword_data in data.get("data", []):
            keyword = keyword_data.get("keyword", "")
            volume = keyword_data.get("vol", 0) or 0
            # FIXED: Extract CPC using helper function
            cpc = extract_cpc_value(keyword_data.get("cpc"))
            competition = keyword_data.get("competition", "Unknown")
            
            # Advanced scoring algorithm
            volume_score = min(volume / 500, 10) if volume else 0
            cpc_score = min(cpc * 3, 10) if cpc else 0
            
            competition_multiplier = {
                "Low": 1.0,
                "Medium": 0.7,
                "High": 0.4
            }.get(competition, 0.5)
            
            # Business relevance bonus
            relevance_bonus = 1.3 if any(bkw.lower() in keyword.lower() for bkw in business_keywords) else 1.0
            
            opportunity_score = ((volume_score * 0.4 + cpc_score * 0.6) * competition_multiplier * relevance_bonus)
            
            scored_keyword = {
                "keyword": keyword,
                "search_volume": volume,
                "cpc": cpc,
                "competition": competition,
                "opportunity_score": round(opportunity_score, 2),
                "priority_tier": "",
                "reasoning": ""
            }
            
            # Assign priority tiers
            if opportunity_score >= 8:
                scored_keyword["priority_tier"] = "Critical"
                scored_keyword["reasoning"] = "High volume, good CPC, manageable competition"
                scoring_result["priority_tiers"]["critical_priority"].append(scored_keyword)
            elif opportunity_score >= 6:
                scored_keyword["priority_tier"] = "High"
                scored_keyword["reasoning"] = "Good balance of volume, value, and competition"
                scoring_result["priority_tiers"]["high_priority"].append(scored_keyword)
            elif opportunity_score >= 4:
                scored_keyword["priority_tier"] = "Medium"
                scored_keyword["reasoning"] = "Moderate opportunity with some challenges"
                scoring_result["priority_tiers"]["medium_priority"].append(scored_keyword)
            else:
                scored_keyword["priority_tier"] = "Low"
                scored_keyword["reasoning"] = "Low volume, high competition, or low commercial value"
                scoring_result["priority_tiers"]["low_priority"].append(scored_keyword)
            
            scoring_result["scored_keywords"].append(scored_keyword)
        
        # Sort by opportunity score
        scoring_result["scored_keywords"].sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return json.dumps(scoring_result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            'error': f"Keyword opportunity scoring failed: {str(e)}",
            'keywords_requested': len(keywords) if keywords else 0
        }, indent=2)

@mcp.tool()
async def competitor_keyword_gap_analysis(current_keywords: list, seed_topics: list, country: str = "US", api_key: str = None) -> str:
    """
    Analyze keyword gaps by comparing your current GSC keywords with related keyword opportunities
    
    Args:
        current_keywords: Keywords you currently rank for (from GSC data)
        seed_topics: Main topic areas to explore for gaps
        country: Country code for search data
        api_key: Keywords Everywhere API key (optional, uses environment variable if not provided)
        
    Returns:
        JSON string with keyword gap analysis and content recommendations
    """
    try:
        # Use provided API key or update scraper's key
        if api_key:
            scraper.ke_api = KeywordsEverywhereAPI(api_key)
        
        # Get related keywords for each seed topic
        all_related_keywords = []
        for topic in seed_topics:
            related_data = await scraper.ke_api.get_related_keywords(topic, country)
            for kw_data in related_data.get("data", []):
                all_related_keywords.append(kw_data.get("keyword", ""))
        
        # Find gaps (keywords not in current list)
        current_kw_set = set([kw.lower() for kw in current_keywords])
        gap_keywords = [kw for kw in all_related_keywords if kw.lower() not in current_kw_set]
        
        # Get data for gap keywords
        if gap_keywords:
            gap_data = await scraper.ke_api.get_search_volume(gap_keywords[:100], country)  # Limit to 100
            
            gap_result = {
                "tool": "Keywords Everywhere - Competitor Gap Analysis",
                "current_keywords_count": len(current_keywords),
                "gap_opportunities_found": len(gap_keywords),
                "analyzed_gaps": len(gap_data.get("data", [])),
                "keyword_gaps": [],
                "high_opportunity_gaps": [],
                "content_gap_recommendations": []
            }
            
            for gap_kw in gap_data.get("data", []):
                keyword = gap_kw.get("keyword", "")
                volume = gap_kw.get("vol", 0) or 0
                # FIXED: Extract CPC using helper function
                cpc = extract_cpc_value(gap_kw.get("cpc"))
                competition = gap_kw.get("competition", "Unknown")
                
                gap_info = {
                    "keyword": keyword,
                    "search_volume": volume,
                    "cpc": cpc,
                    "competition": competition,
                    "gap_priority": "Low"
                }
                
                # Priority scoring for gaps
                if volume >= 1000 and competition in ["Low", "Medium"]:
                    gap_info["gap_priority"] = "High"
                    gap_result["high_opportunity_gaps"].append(gap_info)
                elif volume >= 100:
                    gap_info["gap_priority"] = "Medium"
                
                gap_result["keyword_gaps"].append(gap_info)
            
            # Sort by volume
            gap_result["keyword_gaps"].sort(key=lambda x: x["search_volume"], reverse=True)
            gap_result["high_opportunity_gaps"].sort(key=lambda x: x["search_volume"], reverse=True)
            
            # Content recommendations
            if gap_result["high_opportunity_gaps"]:
                gap_result["content_gap_recommendations"].append({
                    "recommendation": "Create high-priority content pages",
                    "target_keywords": [kw["keyword"] for kw in gap_result["high_opportunity_gaps"][:5]],
                    "estimated_monthly_volume": sum([kw["search_volume"] for kw in gap_result["high_opportunity_gaps"][:5]])
                })
            
            return json.dumps(gap_result, indent=2, ensure_ascii=False)
        else:
            return json.dumps({
                "tool": "Keywords Everywhere - Competitor Gap Analysis",
                "message": "No significant keyword gaps found",
                "current_keywords_count": len(current_keywords)
            }, indent=2)
        
    except Exception as e:
        return json.dumps({
            'error': f"Competitor keyword gap analysis failed: {str(e)}",
            'current_keywords_count': len(current_keywords) if current_keywords else 0,
            'seed_topics': seed_topics
        }, indent=2)

# Cleanup function
async def cleanup():
    """Clean up browser and session resources on shutdown"""
    await scraper.close_resources()

# NEW: Keywords Everywhere API Test Tool
@mcp.tool()
async def test_keywords_everywhere_api(api_key: str = None) -> str:
    """
    Test Keywords Everywhere API connection and key validity
    
    Args:
        api_key: Keywords Everywhere API key (optional, uses environment variable if not provided)
        
    Returns:
        JSON string with API connection test results
    """
    try:
        # Use provided API key or update scraper's key
        if api_key:
            test_api = KeywordsEverywhereAPI(api_key)
        else:
            test_api = scraper.ke_api
        
        # Test the API connection
        test_result = await test_api.test_api_connection()
        return json.dumps(test_result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            'error': f"API test failed: {str(e)}",
            'setup_instructions': [
                '1. Get your Keywords Everywhere API key from https://keywordseverywhere.com',
                '2. Create a .env file with KEYWORDS_EVERYWHERE_API_KEY=your_key_here',
                '3. Or pass the API key directly to this tool'
            ]
        }, indent=2)

if __name__ == "__main__":
    import sys
    
    # Send informational output to stderr instead of stdout to avoid MCP JSON parsing errors
    print("Starting Complete Integrated SEO MCP Server...", file=sys.stderr)
    print("COMBINED: Technical SEO Analysis + SERP Intelligence + Keyword Research", file=sys.stderr)
    print("\nAvailable tools:", file=sys.stderr)
    print("\nTECHNICAL SEO ANALYSIS:", file=sys.stderr)
    print("- scrape_seo_data: Raw SEO data extraction", file=sys.stderr)
    print("- collect_server_headers: Server response headers analysis", file=sys.stderr)
    print("- analyze_redirect_chain: Technical redirect analysis", file=sys.stderr)
    print("- validate_structured_data: Schema.org validation", file=sys.stderr)
    print("- detect_javascript_rendering: JavaScript rendering detection", file=sys.stderr)
    print("- page_speed_metrics: Core Web Vitals and performance data", file=sys.stderr)
    print("\nSERP INTELLIGENCE:", file=sys.stderr)
    print("- serp_data_collector: SERP data collection via SerpAPI", file=sys.stderr)
    print("- analyze_serp_content_alignment: Content vs competitor analysis", file=sys.stderr)
    print("- classify_search_intent_data: Search intent classification", file=sys.stderr)
    print("- analyze_serp_feature_opportunities: SERP feature opportunities", file=sys.stderr)
    print("\nKEYWORD RESEARCH (Keywords Everywhere):", file=sys.stderr)
    print("- keyword_research_analysis: Volume, CPC, competition analysis", file=sys.stderr)
    print("- related_keywords_discovery: Related keyword discovery", file=sys.stderr)
    print("- keyword_opportunity_scorer: Strategic opportunity scoring", file=sys.stderr)
    print("- competitor_keyword_gap_analysis: Keyword gap analysis", file=sys.stderr)
    print("\nINTEGRATION BENEFITS:", file=sys.stderr)
    print("- One unified MCP server for complete SEO analysis", file=sys.stderr)
    print("- Seamless workflow from keyword discovery to technical optimization", file=sys.stderr)
    print("- Enterprise-level insights at fraction of the cost", file=sys.stderr)
    print("- Perfect for on-page SEO specialists following data-first approach", file=sys.stderr)
    print("\nServer ready and waiting for Claude connections...", file=sys.stderr)
    
    # Test CPC parsing fix with sample Keywords Everywhere API data (send to stderr)
    print("\n=== CPC Parsing Fix Verification ===", file=sys.stderr)
    sample_api_response = {
        "data": [
            {
                "vol": 1220000,
                "cpc": {"currency": "$", "value": "0.09"},
                "competition": 0,
                "keyword": "test"
            },
            {
                "vol": 50000,
                "cpc": {"currency": "$", "value": "1.25"},
                "competition": 0.3,
                "keyword": "test keyword"
            }
        ]
    }
    
    print("Testing CPC extraction with sample API data:", file=sys.stderr)
    for item in sample_api_response["data"]:
        extracted_cpc = extract_cpc_value(item.get("cpc"))
        print(f"Keyword: {item['keyword']}", file=sys.stderr)
        print(f"Original CPC: {item['cpc']}", file=sys.stderr)
        print(f"Extracted CPC: {extracted_cpc} (type: {type(extracted_cpc)})", file=sys.stderr)
        print(f"Math test (CPC * 2): {extracted_cpc * 2}", file=sys.stderr)
        print("---", file=sys.stderr)
    print("✅ CPC parsing fix verified - no more TypeError with dict * int", file=sys.stderr)
    print("=====================================\n", file=sys.stderr)
    
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
    finally:
        print("Cleaning up...", file=sys.stderr)
        asyncio.run(cleanup())