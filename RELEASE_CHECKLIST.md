# RoboTrace Release Checklist

Generated UTC: `2026-06-26T06:56:08.570632+00:00`

## Before GitHub publish

- [ ] Read `reports/robotrace_report.md`
- [ ] Read `reports/limitations.md`
- [ ] Read `PUBLIC_CLAIMS.md`
- [ ] Confirm `github_release/security/stage10_secret_scan.md` shows no blocking secret findings
- [ ] Confirm tests pass
- [ ] Confirm no giant raw files are accidentally staged
- [ ] Confirm no token values appear anywhere
- [ ] Confirm README does not overclaim real policy/hardware performance

## Before Hugging Face publish

- [ ] Inspect `hf_release/dataset_card/README.md`
- [ ] Inspect `hf_release/space_app/app.py`
- [ ] Upload `hf_release/space_app/` only as a Space
- [ ] Upload `hf_release/` or curated artifact bundle as Dataset-style release
- [ ] Do not upload private tokens or Kaggle secrets

## Suggested first GitHub commit

```text
Add RoboTrace staged evaluation pipeline and evidence reports
```
