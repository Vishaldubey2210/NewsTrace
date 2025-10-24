"""
NewsTrace Flask API Routes - COMPLETE FIXED VERSION
REST API endpoints with comprehensive error handling
"""

from flask import render_template, request, jsonify, send_file
import logging
from datetime import datetime
import traceback
import json

logger = logging.getLogger(__name__)


def register_routes(app):
    """Register all Flask routes with full error handling"""
    
    # ==================== FRONTEND ROUTES ====================
    
    @app.route('/')
    def index():
        """Landing page"""
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Main dashboard"""
        from app.database.sqlite_db import db_manager
        
        try:
            recent_jobs = db_manager.get_recent_jobs(limit=5)
            jobs_data = [job.to_dict() for job in recent_jobs]
        except Exception as e:
            logger.error(f"Dashboard error: {e}")
            jobs_data = []
        
        return render_template('dashboard.html', recent_jobs=jobs_data)
    
    @app.route('/search')
    def search_page():
        """Outlet search page"""
        return render_template('search.html')
    
    @app.route('/results/<int:outlet_id>')
    def results_page(outlet_id):
        """Journalist profiles results"""
        from app.database.sqlite_db import db_manager
        
        try:
            journalists = db_manager.get_journalists_by_outlet(outlet_id)
            outlet = db_manager.get_outlet_by_id(outlet_id)
            
            return render_template('results.html', 
                                 outlet=outlet.to_dict() if outlet else {},
                                 journalists=[j.to_dict() for j in journalists])
        except Exception as e:
            logger.error(f"Results error: {e}")
            return render_template('results.html', outlet={}, journalists=[])
    
    @app.route('/network-graph')
    def network_graph_page():
        """Network graph visualization"""
        return render_template('network_graph.html')
    
    @app.route('/analytics')
    def analytics_page():
        """Analytics and insights"""
        return render_template('analytics.html')
    
    @app.route('/compare')
    def compare_page():
        """Cross-outlet comparison"""
        return render_template('compare.html')
    
    # ==================== CORE API ROUTES ====================
    
    @app.route('/api/profile', methods=['POST'])
    def api_profile_outlet():
        """
        Start autonomous profiling for an outlet
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No JSON data provided'
                }), 400
            
            outlet_name = data.get('outlet_name', '').strip()
            
            if not outlet_name:
                return jsonify({
                    'success': False,
                    'error': 'Outlet name is required'
                }), 400
            
            logger.info(f"[API] Profile request for: {outlet_name}")
            
            # Import orchestrator
            from app.agents.orchestrator import orchestrator
            
            # Start autonomous profiling workflow
            result = orchestrator.profile_outlet(outlet_name)
            
            # Add outlet_id to response
            if result.get('success'):
                from app.database.sqlite_db import db_manager
                outlet = db_manager.get_outlet_by_name(outlet_name)
                if outlet:
                    result['outlet_id'] = outlet.id
            
            status_code = 200 if result['success'] else 500
            
            return jsonify(result), status_code
            
        except Exception as e:
            logger.error(f"[ERROR] API profile failed: {e}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/outlets', methods=['GET'])
    def api_get_outlets():
        """Get all outlets"""
        try:
            from app.database.sqlite_db import db_manager
            
            outlets = db_manager.get_all_outlets()
            
            return jsonify({
                'success': True,
                'count': len(outlets),
                'outlets': [o.to_dict() for o in outlets]
            })
            
        except Exception as e:
            logger.error(f"[ERROR] Get outlets failed: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/outlet/<int:outlet_id>', methods=['GET'])
    def api_get_outlet(outlet_id):
        """Get single outlet details"""
        try:
            from app.database.sqlite_db import db_manager
            
            outlet = db_manager.get_outlet_by_id(outlet_id)
            
            if not outlet:
                return jsonify({
                    'success': False,
                    'error': 'Outlet not found'
                }), 404
            
            return jsonify({
                'success': True,
                'outlet': outlet.to_dict()
            })
            
        except Exception as e:
            logger.error(f"[ERROR] Get outlet failed: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/outlet/<int:outlet_id>/journalists', methods=['GET'])
    def api_get_journalists(outlet_id):
        """Get all journalists for an outlet"""
        try:
            from app.database.sqlite_db import db_manager
            
            journalists = db_manager.get_journalists_by_outlet(outlet_id)
            journalists_data = [j.to_dict() for j in journalists]
            
            return jsonify({
                'success': True,
                'count': len(journalists_data),
                'journalists': journalists_data
            })
            
        except Exception as e:
            logger.error(f"[ERROR] Get journalists failed: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # ==================== NETWORK GRAPH API (FIXED) ====================
    
    @app.route('/api/network/graph/<int:outlet_id>', methods=['GET'])
    def api_get_network_graph(outlet_id):
        """
        Get network graph data for visualization - FIXED VERSION
        """
        try:
            logger.info(f"[API] Network graph requested for outlet: {outlet_id}")
            
            from app.database.sqlite_db import db_manager
            from app.database.graph_builder import graph_builder
            
            # Get journalists for outlet
            journalists = db_manager.get_journalists_by_outlet(outlet_id)
            
            if not journalists:
                logger.warning(f"[API] No journalists found for outlet: {outlet_id}")
                return jsonify({
                    'success': True,
                    'nodes': [],
                    'edges': [],
                    'stats': {
                        'total_nodes': 0,
                        'total_edges': 0,
                        'journalist_count': 0,
                        'topic_count': 0
                    }
                })
            
            # Convert to dict
            journalists_data = [j.to_dict() for j in journalists]
            
            logger.info(f"[API] Processing {len(journalists_data)} journalists")
            
            # Extract all unique topics with safety
            all_topics = set()
            
            for journalist in journalists_data:
                try:
                    # Strategy 1: Get from metadata
                    metadata = journalist.get('metadata')
                    
                    if metadata:
                        # Handle string metadata (JSON)
                        if isinstance(metadata, str):
                            try:
                                metadata = json.loads(metadata)
                            except (json.JSONDecodeError, TypeError):
                                logger.warning(f"[API] Could not parse metadata for {journalist.get('name')}")
                                metadata = {}
                        
                        # Extract topics from metadata dict
                        if isinstance(metadata, dict):
                            topics = metadata.get('topics', [])
                            if topics and isinstance(topics, list):
                                for topic in topics:
                                    if topic and isinstance(topic, str):
                                        all_topics.add(topic.strip())
                    
                    # Strategy 2: Add beat as topic
                    beat = journalist.get('beat')
                    if beat and isinstance(beat, str) and beat.strip():
                        all_topics.add(beat.strip())
                    
                except Exception as e:
                    logger.error(f"[API] Error extracting topics: {e}")
                    continue
            
            logger.info(f"[API] Extracted {len(all_topics)} unique topics")
            
            # Build graph (this handles None topics internally now)
            try:
                G = graph_builder.build_bipartite_graph(journalists_data, list(all_topics))
                
                # Check if graph is empty
                if G.number_of_nodes() == 0:
                    logger.warning("[API] Built graph is empty")
                    return jsonify({
                        'success': True,
                        'nodes': [],
                        'edges': [],
                        'stats': {
                            'total_nodes': 0,
                            'total_edges': 0,
                            'journalist_count': 0,
                            'topic_count': 0
                        }
                    })
                
                # Export to Vis.js format
                graph_data = graph_builder.export_graph_json(G)
                
                logger.info(f"[API] Successfully exported graph with {len(graph_data['nodes'])} nodes")
                
                return jsonify({
                    'success': True,
                    **graph_data
                })
                
            except Exception as graph_error:
                logger.error(f"[ERROR] Graph building failed: {graph_error}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return jsonify({
                    'success': False,
                    'error': f'Failed to build network graph: {str(graph_error)}'
                }), 500
            
        except Exception as e:
            logger.error(f"[ERROR] Network graph endpoint failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # ==================== ANALYTICS API ====================
    
    @app.route('/api/analytics/stats', methods=['GET'])
    def api_get_analytics_stats():
        """Get overall analytics statistics"""
        try:
            from app.database.sqlite_db import db_manager
            
            stats = db_manager.get_statistics()
            
            return jsonify({
                'success': True,
                'stats': stats
            })
            
        except Exception as e:
            logger.error(f"[ERROR] Analytics stats failed: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/journalists/top/<int:limit>', methods=['GET'])
    def api_get_top_journalists(limit=10):
        """Get top journalists by influence score"""
        try:
            from app.database.sqlite_db import db_manager
            
            # Get all journalists
            all_journalists = db_manager.get_all_journalists()
            
            # Convert to dict and sort by influence
            journalists_data = [j.to_dict() for j in all_journalists]
            sorted_journalists = sorted(
                journalists_data, 
                key=lambda x: x.get('influence_score', 0), 
                reverse=True
            )[:limit]
            
            return jsonify({
                'success': True,
                'count': len(sorted_journalists),
                'journalists': sorted_journalists
            })
            
        except Exception as e:
            logger.error(f"[ERROR] Top journalists failed: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # ==================== EXPORT API ====================
    
    @app.route('/api/export/csv/<int:outlet_id>', methods=['GET'])
    def api_export_csv(outlet_id):
        """Export journalist profiles to CSV"""
        try:
            from app.database.sqlite_db import db_manager
            from app.export.csv_exporter import export_to_csv
            
            journalists = db_manager.get_journalists_by_outlet(outlet_id)
            
            if not journalists:
                return jsonify({
                    'success': False,
                    'error': 'No journalists found for this outlet'
                }), 404
            
            # Generate CSV file
            csv_path = export_to_csv(journalists, outlet_id)
            
            return send_file(
                csv_path,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'journalists_outlet_{outlet_id}.csv'
            )
            
        except Exception as e:
            logger.error(f"[ERROR] CSV export failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/export/json/<int:outlet_id>', methods=['GET'])
    def api_export_json(outlet_id):
        """Export journalist profiles to JSON"""
        try:
            from app.database.sqlite_db import db_manager
            from tempfile import NamedTemporaryFile
            
            journalists = db_manager.get_journalists_by_outlet(outlet_id)
            
            if not journalists:
                return jsonify({
                    'success': False,
                    'error': 'No journalists found for this outlet'
                }), 404
            
            # Convert to dict
            data = {
                'outlet_id': outlet_id,
                'export_date': datetime.now().isoformat(),
                'count': len(journalists),
                'journalists': [j.to_dict() for j in journalists]
            }
            
            # Create temporary JSON file
            with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(data, f, indent=2)
                temp_path = f.name
            
            return send_file(
                temp_path,
                mimetype='application/json',
                as_attachment=True,
                download_name=f'journalists_outlet_{outlet_id}.json'
            )
            
        except Exception as e:
            logger.error(f"[ERROR] JSON export failed: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # ==================== JOBS API ====================
    
    @app.route('/api/jobs/recent', methods=['GET'])
    def api_recent_jobs():
        """Get recent scraping jobs"""
        try:
            from app.database.sqlite_db import db_manager
            
            limit = request.args.get('limit', 10, type=int)
            jobs = db_manager.get_recent_jobs(limit)
            jobs_data = [job.to_dict() for job in jobs]
            
            return jsonify({
                'success': True,
                'jobs': jobs_data
            })
            
        except Exception as e:
            logger.error(f"[ERROR] Recent jobs failed: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/jobs/<int:job_id>', methods=['GET'])
    def api_get_job(job_id):
        """Get specific job details"""
        try:
            from app.database.sqlite_db import db_manager
            
            job = db_manager.get_job_by_id(job_id)
            
            if not job:
                return jsonify({
                    'success': False,
                    'error': 'Job not found'
                }), 404
            
            return jsonify({
                'success': True,
                'job': job.to_dict()
            })
            
        except Exception as e:
            logger.error(f"[ERROR] Get job failed: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # ==================== UTILITY API ====================
    
    @app.route('/api/health', methods=['GET'])
    def api_health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'NewsTrace API',
            'version': '1.0.0'
        })
    
    @app.route('/api/search/detect', methods=['POST'])
    def api_detect_website():
        """Test website detection (debugging)"""
        try:
            from app.scrapers.website_detector import website_detector
            
            data = request.get_json()
            outlet_name = data.get('outlet_name', '').strip()
            
            if not outlet_name:
                return jsonify({
                    'success': False,
                    'error': 'Outlet name is required'
                }), 400
            
            result = website_detector.detect_website(outlet_name)
            
            if result:
                return jsonify({
                    'success': True,
                    **result
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Website not detected'
                }), 404
                
        except Exception as e:
            logger.error(f"[ERROR] Website detection test failed: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Endpoint not found',
                'path': request.path
            }), 404
        return render_template('index.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        logger.error(f"[ERROR] Internal server error: {error}")
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500
        return render_template('index.html'), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """405 error handler"""
        return jsonify({
            'success': False,
            'error': 'Method not allowed',
            'path': request.path,
            'method': request.method
        }), 405
    
    # Log successful registration
    logger.info("[OK] All routes registered successfully")
    logger.info(f"[OK] Total routes: {len(app.url_map._rules)}")
