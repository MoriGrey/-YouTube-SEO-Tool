"""
Start Continuous Learning Loop
Starts the 24/7 continuous learning system
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.youtube_client import create_client
from src.modules.channel_analyzer import ChannelAnalyzer
from src.modules.keyword_researcher import KeywordResearcher
from src.modules.competitor_analyzer import CompetitorAnalyzer
from src.modules.trend_predictor import TrendPredictor
from src.modules.performance_tracker import PerformanceTracker
from src.modules.feedback_learner import FeedbackLearner
from src.modules.multi_source_integrator import MultiSourceIntegrator
from src.modules.knowledge_graph import KnowledgeGraph
from src.modules.continuous_learner import ContinuousLearner

def main():
    """Start continuous learning loop."""
    print("=" * 60)
    print("YouTube SEO AGI Tool - Continuous Learning Loop")
    print("=" * 60)
    print()
    
    # Get channel handle from environment or use default
    channel_handle = os.getenv("TARGET_CHANNEL_HANDLE", "anatolianturkishrock")
    print(f"Target Channel: @{channel_handle}")
    print()
    
    try:
        # Initialize client
        print("[1] Initializing YouTube client...")
        client = create_client()
        print("  [OK] Client initialized")
        
        # Initialize modules
        print("[2] Initializing modules...")
        channel_analyzer = ChannelAnalyzer(client)
        keyword_researcher = KeywordResearcher(client)
        competitor_analyzer = CompetitorAnalyzer(client)
        trend_predictor = TrendPredictor(client)
        performance_tracker = PerformanceTracker(client)
        feedback_learner = FeedbackLearner(client, performance_tracker)
        multi_source_integrator = MultiSourceIntegrator(client)
        knowledge_graph = KnowledgeGraph(
            client,
            performance_tracker,
            feedback_learner,
            multi_source_integrator,
            None  # competitor_benchmark not needed for basic setup
        )
        
        print("  [OK] Modules initialized")
        
        # Initialize continuous learner
        print("[3] Initializing continuous learner...")
        continuous_learner = ContinuousLearner(
            client,
            performance_tracker,
            feedback_learner,
            multi_source_integrator,
            knowledge_graph,
            trend_predictor
        )
        print("  [OK] Continuous learner initialized")
        
        # Start learning loop
        print("[4] Starting continuous learning loop...")
        result = continuous_learner.start_learning_loop(channel_handle)
        
        if result.get("status") == "started":
            print("  [OK] Learning loop started!")
            print(f"  [INFO] Learning interval: {result.get('interval_seconds', 3600) / 60:.0f} minutes")
            print()
            print("=" * 60)
            print("Continuous Learning Loop is now running!")
            print("=" * 60)
            print()
            print("The system will:")
            print("  - Take performance snapshots every hour")
            print("  - Discover new trends automatically")
            print("  - Update knowledge graph")
            print("  - Generate daily reports at 9:00 AM")
            print()
            print("Press Ctrl+C to stop the learning loop")
            print()
            
            # Keep running
            try:
                while True:
                    time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                print()
                print("[INFO] Stopping learning loop...")
                stop_result = continuous_learner.stop_learning_loop()
                print(f"  {stop_result.get('message', 'Stopped')}")
                print()
                print("[SUCCESS] Learning loop stopped successfully")
        else:
            print(f"  [ERROR] {result.get('message', 'Failed to start')}")
            return 1
            
    except Exception as e:
        print(f"[ERROR] Failed to start continuous learning: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

