"""
Example PI Rule Extension (Phase 7).

Demonstrates contributing specialized PDD rule behavior through the
extension system instead of hand-editing `pdd_rules` directly. Any agent
scoped to 'archon' (or 'core') picks this up automatically once
`scripts/index_extension_rules.py` has indexed it.
"""

def gpu_thermal_rules():
    return [
        {
            "rule_id": "R-PDD-EXT-GPU-THERMAL-001",
            "title": "GPU Extension Thermal Guard",
            "content": (
                "Before scheduling any fine-tuning or batch-inference job on the "
                "Tesla P40 or RTX 3070, confirm current GPU temperature is below "
                "the 85C safety limit and that the thermal monitor service is "
                "active. Reject proposals that disable or bypass temperature checks."
            ),
        }
    ]


def default(pi):
    """Entry point called by ExtensionManager.load_extension."""
    pi.registerRuleProvider("archon", gpu_thermal_rules)
