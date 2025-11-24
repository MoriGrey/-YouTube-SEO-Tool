"""
Functional Test Script - Tests module functionality without requiring all dependencies
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("YouTube SEO AGI Tool - Functional Test")
print("=" * 60)
print()

# Test modules that don't require external dependencies
test_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

# Test 1: SafetyEthicsLayer (no external deps)
print("[1] Testing SafetyEthicsLayer...")
try:
    from src.modules.safety_ethics_layer import SafetyEthicsLayer
    layer = SafetyEthicsLayer()
    
    # Test content safety check
    result = layer.check_content_safety(
        title="Test Video Title",
        description="This is a test description",
        tags=["test", "video"]
    )
    
    assert "risk_score" in result
    assert "safety_status" in result
    assert result["safety_status"] in ["safe", "low_risk", "medium_risk", "high_risk"]
    test_results["passed"].append("[OK] SafetyEthicsLayer.check_content_safety()")
    
    # Test recommendation filtering
    recommendations = ["Good recommendation", "Click here now!", "Free subscribers"]
    filtered = layer.filter_recommendations(recommendations)
    assert "safe_recommendations" in filtered
    assert "filtered_out" in filtered
    test_results["passed"].append("[OK] SafetyEthicsLayer.filter_recommendations()")
    
    # Test statistics
    stats = layer.get_safety_statistics()
    assert "total_checks" in stats
    test_results["passed"].append("[OK] SafetyEthicsLayer.get_safety_statistics()")
    
    print("  [OK] SafetyEthicsLayer - All tests passed")
except Exception as e:
    test_results["failed"].append(f"[FAIL] SafetyEthicsLayer: {str(e)}")
    print(f"  [FAIL] SafetyEthicsLayer: {str(e)}")
print()

# Test 2: DescriptionGenerator (no external deps)
print("[2] Testing DescriptionGenerator...")
try:
    from src.modules.description_generator import DescriptionGenerator
    gen = DescriptionGenerator()
    
    # Test description generation
    desc = gen.generate_description(
        video_title="Test Video",
        keywords=["test", "video"],
        song_name="Test Song"
    )
    
    assert isinstance(desc, dict)
    assert "description" in desc
    assert len(desc["description"]) > 0
    test_results["passed"].append("[OK] DescriptionGenerator.generate_description()")
    
    print("  [OK] DescriptionGenerator - All tests passed")
except Exception as e:
    test_results["failed"].append(f"[FAIL] DescriptionGenerator: {str(e)}")
    print(f"  [FAIL] DescriptionGenerator: {str(e)}")
print()

# Test 3: Check data directory structure
print("[3] Testing Data Directory...")
data_dir = project_root / "data"
if not data_dir.exists():
    data_dir.mkdir(exist_ok=True)
    test_results["warnings"].append("[WARN] Created data/ directory")
else:
    test_results["passed"].append("[OK] data/ directory exists")

# Check if data files can be created
try:
    test_file = data_dir / "test.json"
    import json
    with open(test_file, 'w') as f:
        json.dump({"test": True}, f)
    test_file.unlink()  # Clean up
    test_results["passed"].append("[OK] Data directory is writable")
except Exception as e:
    test_results["failed"].append(f"[FAIL] Data directory: {str(e)}")
print()

# Test 4: Check dashboard imports structure
print("[4] Testing Dashboard Structure...")
dashboard_path = project_root / "dashboard.py"
if dashboard_path.exists():
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Check for all Phase 6 modules
        phase6_modules = [
            "PerformanceTracker",
            "MilestoneTracker",
            "FeedbackLearner",
            "ViralPredictor",
            "CompetitorBenchmark",
            "MultiSourceIntegrator",
            "KnowledgeGraph",
            "ContinuousLearner",
            "CodeSelfImprover",
            "SafetyEthicsLayer"
        ]
        
        missing = []
        for module in phase6_modules:
            if f"from src.modules" in content and module in content:
                test_results["passed"].append(f"[OK] Dashboard imports {module}")
            else:
                missing.append(module)
        
        if missing:
            test_results["warnings"].append(f"[WARN] Dashboard may be missing: {', '.join(missing)}")
        else:
            test_results["passed"].append("[OK] All Phase 6 modules in dashboard")
else:
    test_results["failed"].append("[FAIL] dashboard.py not found")
print()

# Test 5: Check module file structure
print("[5] Testing Module Files...")
modules_dir = project_root / "src" / "modules"
expected_modules = [
    "channel_analyzer.py",
    "keyword_researcher.py",
    "competitor_analyzer.py",
    "title_optimizer.py",
    "description_generator.py",
    "tag_suggester.py",
    "trend_predictor.py",
    "proactive_advisor.py",
    "report_generator.py",
    "performance_tracker.py",
    "milestone_tracker.py",
    "feedback_learner.py",
    "viral_predictor.py",
    "competitor_benchmark.py",
    "multi_source_integrator.py",
    "knowledge_graph.py",
    "continuous_learner.py",
    "code_self_improver.py",
    "safety_ethics_layer.py"
]

for module_file in expected_modules:
    module_path = modules_dir / module_file
    if module_path.exists():
        test_results["passed"].append(f"[OK] {module_file} exists")
    else:
        test_results["failed"].append(f"[FAIL] {module_file} not found")

print()

# Print Results
print("=" * 60)
print("FUNCTIONAL TEST RESULTS")
print("=" * 60)
print()

print(f"[PASSED] {len(test_results['passed'])}")
for item in test_results["passed"][:10]:  # Show first 10
    print(f"  {item}")
if len(test_results["passed"]) > 10:
    print(f"  ... and {len(test_results['passed']) - 10} more")

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
    print("[SUCCESS] All functional tests passed!")
    if len(test_results["warnings"]) > 0:
        print("[WARNING] Some warnings detected")
else:
    print("[FAILED] Some tests failed")
print("=" * 60)

