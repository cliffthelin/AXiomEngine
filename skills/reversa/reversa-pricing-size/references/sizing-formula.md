### SOURCE:
# Sizing Formula (sizing-formula.md)

**Formula Version:** 2.0
**Schema Version of size.json:** 1.1

This document details the deterministic calculation that the `reversa-pricing-size` agent applies to transform artifacts from the forward cycle into a complexity class (`S/M/L/XL/XXL`). Version 2 of the formula abandons the linear sum of arbitrary weights and adopts a T-shirt sizing system based on tasks, with a separate risk adjustment.

## Source and Criteria

Version 1 of the Reversa system needed a user-friendly, multi-engine metric derived from files already produced in `_reversa_sdd/forward/<feature>/`.

Function Points (IFPUG, ISO/IEC 20926) and COSMIC (ISO/IEC 19761) are formal functional measurement standards, but they require specialized classification. For the Reversa UX, the best approach is an approximate agile estimate, inspired by Story Points and T-shirt sizing. Mike Cohn, in *Agile Estimating and Planning* (Addison-Wesley, 2005), describes relative estimation and approximate sizes as agile planning practices.

This formula does not claim that the size ranges represent a universal standard. It documents a simple Reversa heuristic, based on T-shirt sizing, and keeps risk factors separate to avoid false precision.

## Inputs

The inputs continue to come from `metrics`:

- `tasks.total`
- `doubts.high`, `doubts.medium`, `doubts.low`, `doubts.total`
- `plan_depth`
- `principles_touched`
- `requirements.total`, used only as a consistency check and not as the primary driver

## Step 1: Base Class Based on Task Count

`tasks.total` is the best proxy for size because the forward cycle has already broken down the feature into work units.

```
if tasks.total <= 0:       base_complexity_class = "S"
elif tasks.total <= 3:     base_complexity_class = "S"
elif tasks.total <= 7:     base_complexity_class = "M"
elif tasks.total <= 15:    base_complexity_class = "L"
elif tasks.total <= 30:    base_complexity_class = "XL"
else:                      base_complexity_class = "XXL"
```

## Step 2: Risk Points

Risk is not size. It adjusts the class upward when the feature has uncertainty, depth, or cross-impact.

```
unclassified_doubts =
  max(0, doubts.total - doubts.high - doubts.medium - doubts.low)

risk_points =
  doubts.high * 2 +
  doubts.medium * 1 +
  unclassified_doubts * 1 +
  max(0, plan_depth - 3) +
  floor(len(principles_touched) / 3)
```

`doubts.low` does not increase risk in version 2. Low-level doubts are the expected noise of refinement.

## Step 3: Risk Adjustment

```
if risk_points <= 2:       risk_adjustment_classes = 0
elif risk_points <= 5:     risk_adjustment_classes = 1
else:                      risk_adjustment_classes = 2
```

## Step 4: Final Class

Classes are ordered as follows:

```
S=0, M=1, L=2, XL=3, XXL=4
```

```
complexity_class =
  class_from_index(min(4, index(base_complexity_class) + risk_adjustment_classes))
```

## Step 5: Auxiliary `size_score`

`size_score` is kept for compatibility and quick reference. It should no longer be used to directly derive hours.

```
size_score_by_class:
  S:   15
  M:   35
  L:   60
  XL:  80
  XXL: 95
```

## Recommended Fields in `size.json`

The agent should save these fields in addition to the existing fields:

```
sizing_method = "task_tshirt_with_risk_adjustment"
base_complexity_class = <class before risk is applied>
risk_points = <integer>
risk_adjustment_classes = <0, 1, or 2>
size_score = <midpoint of the final class>
```

## Calculation Examples

### Example 1: Small Feature (S)

```
tasks.total = 3
doubts.high = 0
doubts.medium = 0
doubts.low = 0
doubts.total = 0
plan_depth = 2
principles_touched = []

base_complexity_class = S
risk_points = 0
risk_adjustment_classes = 0
complexity_class = S
size_score = 15
```

### Example 2: Medium Feature that Scales to L Due to Risk

```
tasks.total = 7
doubts.total = 3 (high=1, medium=2, low=0)
plan_depth = 3
principles_touched = ["non_destructive", "multi_engine", "handoff_pattern"]

base_complexity_class = M
risk_points = 1*2 + 2*1 + 0 + 0 + floor(3/3) = 5
risk_adjustment_classes = 1
complexity_class = L
size_score = 60
```

### Example 3: Large Feature (XL)

```
tasks.total = 12
doubts.total = 1 (high=0, medium=1, low=0)
plan_depth = 4
principles_touched = 2

base_complexity_class = L
risk_points = 0 + 1 + 0 + 1 + 0 = 2
risk_adjustment_classes = 0
complexity_class = L
size_score = 60
```

### Example 4: Giant Feature (XXL)

```
tasks.total = 31
doubts.total = 6 (high=2, medium=3, low=1)
plan_depth = 6
principles_touched = 8

base_complexity_class = XXL
risk_points = 2*2 + 3*1 + 0 + 3 + floor(8/3) = 12
risk_adjustment_classes = 2
complexity_class = XXL
size_score = 95
```

## Consistency Warnings

Requirements are not used in the primary calculation, but may generate a note:

```
if requirements.total >= 12 and tasks.total <= 3:
  notes += "Too many requirements for few tasks. Verify that tasks.md is granular enough."
```

## Limitations and Assumptions

1.  The formula measures structural size before coding, therefore it does not use LOC
2.  Tokens are not counted
3.  `size_score` is auxiliary and should not be directly converted into hours
4.  XXL should trigger a recommendation to break down the scope before pricing or coding
5.  If the class limit changes, increment the `formula_version`