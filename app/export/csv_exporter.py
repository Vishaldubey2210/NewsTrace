# Placeholder file
"""
NewsTrace CSV Exporter
Export journalist profiles to CSV format
"""

import csv
from pathlib import Path
from datetime import datetime
from typing import List
import logging

from config import Config
from app.models import Journalist

logger = logging.getLogger(__name__)


def export_to_csv(journalists: List[Journalist], outlet_id: int) -> str:
    """
    Export journalist profiles to CSV
    
    Args:
        journalists: List of journalist objects
        outlet_id: Outlet ID
        
    Returns:
        Path to generated CSV file
    """
    try:
        # Create export directory if not exists
        export_dir = Path(Config.EXPORT_PATH)
        export_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"journalists_outlet_{outlet_id}_{timestamp}.csv"
        filepath = export_dir / filename
        
        # CSV headers
        headers = [
            'ID', 'Name', 'Beat', 'Email', 'Phone', 
            'Bio', 'Profile URL', 'Twitter', 'LinkedIn',
            'Article Count', 'Influence Score', 'First Seen'
        ]
        
        # Write CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for j in journalists:
                writer.writerow([
                    j.id,
                    j.name,
                    j.beat or '',
                    j.contact_email or '',
                    j.contact_phone or '',
                    j.bio or '',
                    j.profile_url or '',
                    j.twitter_handle or '',
                    j.linkedin_url or '',
                    j.article_count,
                    f"{j.influence_score:.2f}",
                    j.first_seen.strftime('%Y-%m-%d') if j.first_seen else ''
                ])
        
        logger.info(f"✅ CSV exported: {filepath}")
        return str(filepath)
        
    except Exception as e:
        logger.error(f"CSV export failed: {e}")
        raise
