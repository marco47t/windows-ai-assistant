"""Multi-source synthesis with citations."""

from typing import List, Dict, Tuple
from core.logger import logger


class SynthesisService:
    """Synthesize information from multiple sources."""
    
    def extract_facts(self, pages: List[Dict]) -> List[Dict]:
        """Extract key facts from multiple pages.
        
        Args:
            pages: List of page data with content
            
        Returns:
            List of facts with sources
        """
        facts = []
        
        for i, page in enumerate(pages, 1):
            # Simple fact extraction (split by sentences)
            content = page.get('content', '')
            sentences = content.split('.')
            
            # Take first 3-5 substantial sentences as facts
            for sentence in sentences[:5]:
                sentence = sentence.strip()
                if len(sentence) > 50:  # Substantial sentence
                    facts.append({
                        'text': sentence,
                        'source': page.get('url', 'Unknown'),
                        'source_title': page.get('title', 'Unknown'),
                        'source_number': i
                    })
        
        return facts
    
    def format_with_citations(self, facts: List[Dict], pages: List[Dict]) -> str:
        """Format facts with source citations.
        
        Args:
            facts: List of facts
            pages: Source pages
            
        Returns:
            Formatted text with citations
        """
        output = []
        
        # Group facts by source
        by_source = {}
        for fact in facts:
            source_num = fact['source_number']
            if source_num not in by_source:
                by_source[source_num] = []
            by_source[source_num].append(fact)
        
        # Format output
        output.append("**Information from Multiple Sources:**\n")
        
        for source_num, source_facts in sorted(by_source.items()):
            source_title = source_facts[0]['source_title']
            source_url = source_facts[0]['source']
            
            output.append(f"### Source {source_num}: {source_title}")
            output.append(f"🔗 {source_url}\n")
            
            for fact in source_facts[:3]:  # Top 3 facts per source
                output.append(f"- {fact['text']}")
            
            output.append("")
        
        # Add sources list at bottom
        output.append("\n**Sources:**")
        for i, page in enumerate(pages, 1):
            output.append(f"{i}. [{page.get('title', 'Unknown')}]({page.get('url', '#')})")
        
        return "\n".join(output)
    
    def compare_sources(self, facts: List[Dict]) -> Dict:
        """Compare information across sources.
        
        Args:
            facts: List of facts
            
        Returns:
            Comparison summary
        """
        # Simple comparison: find common keywords
        all_words = []
        for fact in facts:
            words = fact['text'].lower().split()
            all_words.extend([w for w in words if len(w) > 4])
        
        # Count word frequency
        word_count = {}
        for word in all_words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Common themes (words mentioned multiple times)
        common_themes = [
            word for word, count in word_count.items()
            if count >= 2
        ][:10]
        
        return {
            'total_sources': len(set(f['source'] for f in facts)),
            'total_facts': len(facts),
            'common_themes': common_themes
        }


# Global synthesis service
synthesis_service = SynthesisService()
