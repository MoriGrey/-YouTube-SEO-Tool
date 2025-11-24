"""
Integration Test Script for YouTube SEO AGI Tool
Tests all modules for importability and basic functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Test results
test_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

def test_import(module_name, class_name=None):
    """Test if a module can be imported."""
    try:
        module = __import__(module_name, fromlist=[class_name] if class_name else [])
        if class_name:
            cls = getattr(module, class_name)
            test_results["passed"].append(f"[OK] {module_name}.{class_name}")
            return cls
        else:
            test_results["passed"].append(f"[OK] {module_name}")
            return module
    except Exception as e:
        test_results["failed"].append(f"[FAIL] {module_name}.{class_name if class_name else ''}: {str(e)}")
        return None

def test_module_initialization(cls, *args, **kwargs):
    """Test if a module class can be initialized."""
    try:
        instance = cls(*args, **kwargs)
        return instance
    except Exception as e:
        test_results["warnings"].append(f"[WARN] {cls.__name__} initialization: {str(e)}")
        return None

print("=" * 60)
print("YouTube SEO AGI Tool - Integration Test")
print("=" * 60)
print()

# Test 1: Core utilities
print("[1] Testing Core Utilities...")
youtube_client = test_import("src.utils.youtube_client", "YouTubeClient")
create_client = test_import("src.utils.youtube_client", "create_client")
print()

# Test 2: Phase 2 Modules (Analysis)
print("[2] Testing Phase 2: Analysis Modules...")
ChannelAnalyzer = test_import("src.modules.channel_analyzer", "ChannelAnalyzer")
KeywordResearcher = test_import("src.modules.keyword_researcher", "KeywordResearcher")
CompetitorAnalyzer = test_import("src.modules.competitor_analyzer", "CompetitorAnalyzer")
print()

# Test 3: Phase 3 Modules (Optimization)
print("[3] Testing Phase 3: Optimization Modules...")
TitleOptimizer = test_import("src.modules.title_optimizer", "TitleOptimizer")
DescriptionGenerator = test_import("src.modules.description_generator", "DescriptionGenerator")
TagSuggester = test_import("src.modules.tag_suggester", "TagSuggester")
print()

# Test 4: Phase 4 Modules (Smart Features)
print("[4] Testing Phase 4: Smart Features...")
TrendPredictor = test_import("src.modules.trend_predictor", "TrendPredictor")
ProactiveAdvisor = test_import("src.modules.proactive_advisor", "ProactiveAdvisor")
print()

# Test 5: Phase 5 Modules (Reporting)
print("[5] Testing Phase 5: Reporting...")
ReportGenerator = test_import("src.modules.report_generator", "ReportGenerator")
print()

# Test 6: Phase 6 Modules (AGI Features)
print("[6] Testing Phase 6: AGI Features...")
PerformanceTracker = test_import("src.modules.performance_tracker", "PerformanceTracker")
MilestoneTracker = test_import("src.modules.milestone_tracker", "MilestoneTracker")
FeedbackLearner = test_import("src.modules.feedback_learner", "FeedbackLearner")
ViralPredictor = test_import("src.modules.viral_predictor", "ViralPredictor")
CompetitorBenchmark = test_import("src.modules.competitor_benchmark", "CompetitorBenchmark")
MultiSourceIntegrator = test_import("src.modules.multi_source_integrator", "MultiSourceIntegrator")
KnowledgeGraph = test_import("src.modules.knowledge_graph", "KnowledgeGraph")
ContinuousLearner = test_import("src.modules.continuous_learner", "ContinuousLearner")
CodeSelfImprover = test_import("src.modules.code_self_improver", "CodeSelfImprover")
SafetyEthicsLayer = test_import("src.modules.safety_ethics_layer", "SafetyEthicsLayer")
print()

# Test 7: Dashboard
print("[7] Testing Dashboard...")
try:
    # Just check if dashboard.py exists and can be parsed
    dashboard_path = project_root / "dashboard.py"
    if dashboard_path.exists():
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for key imports
            required_imports = [
                "from src.modules.channel_analyzer import",
                "from src.modules.performance_tracker import",
                "from src.modules.safety_ethics_layer import"
            ]
            all_imports_found = all(imp in content for imp in required_imports)
            if all_imports_found:
                test_results["passed"].append("[OK] dashboard.py imports")
            else:
                test_results["warnings"].append("[WARN] dashboard.py: Some imports may be missing")
    else:
        test_results["failed"].append("[FAIL] dashboard.py: File not found")
except Exception as e:
    test_results["failed"].append(f"[FAIL] dashboard.py: {str(e)}")
print()

# Test 8: Data directory structure
print("[8] Testing Data Directory Structure...")
data_dir = project_root / "data"
if data_dir.exists():
    test_results["passed"].append("[OK] data/ directory exists")
else:
    test_results["warnings"].append("[WARN] data/ directory does not exist (will be created on first run)")
print()

# Test 9: Requirements
print("[9] Testing Requirements...")
requirements_path = project_root / "requirements.txt"
if requirements_path.exists():
    test_results["passed"].append("[OK] requirements.txt exists")
    try:
        with open(requirements_path, 'r') as f:
            requirements = f.read()
            # Check for key dependencies
            key_deps = ["streamlit", "google-api-python-client", "python-dotenv"]
            for dep in key_deps:
                if dep in requirements:
                    test_results["passed"].append(f"[OK] {dep} in requirements.txt")
                else:
                    test_results["warnings"].append(f"[WARN] {dep} not found in requirements.txt")
    except Exception as e:
        test_results["warnings"].append(f"[WARN] Could not read requirements.txt: {str(e)}")
else:
    test_results["failed"].append("[FAIL] requirements.txt not found")
print()

# Test 10: Module initialization (without API calls)
print("[10] Testing Module Initialization (without API calls)...")
try:
    # Test modules that don't require API client
    if SafetyEthicsLayer:
        safety_layer = SafetyEthicsLayer()
        test_results["passed"].append("[OK] SafetyEthicsLayer initialization")
    
    if DescriptionGenerator:
        desc_gen = DescriptionGenerator()
        test_results["passed"].append("[OK] DescriptionGenerator initialization")
    
except Exception as e:
    test_results["warnings"].append(f"[WARN] Module initialization test: {str(e)}")
print()

# Print Results
print("=" * 60)
print("TEST RESULTS SUMMARY")
print("=" * 60)
print()

print(f"[PASSED] {len(test_results['passed'])}")
for item in test_results["passed"]:
    print(f"  {item}")

print()
print(f"[WARNINGS] {len(test_results['warnings'])}")
for item in test_results["warnings"]:
    print(f"  {item}")

print()
print(f"[FAILED] {len(test_results['failed'])}")
for item in test_results["failed"]:
    print(f"  {item}")

print()
print("=" * 60)
if len(test_results["failed"]) == 0:
    print("[SUCCESS] All critical tests passed!")
    if len(test_results["warnings"]) > 0:
        print("[WARNING] Some warnings detected - review recommended")
else:
    print("[FAILED] Some tests failed - review required")
print("=" * 60)

