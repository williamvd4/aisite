# Dependency Upgrade Plan

`requirements.txt` is currently encoded in a legacy format in the base branch, and tooling that expects text-only patches rejects diffs touching that file as binary.

## Proposed approach
1. Convert `requirements.txt` encoding in a dedicated maintenance window.
2. Apply the curated dependency set below as the new baseline.
3. Run full regression tests and security audit (`pip-audit`) after network access is available.

## Target dependency baseline

```txt
Django>=5.2,<5.3
asgiref>=3.8.1,<4
sqlparse>=0.5.2,<0.6
tzdata>=2025.2

django-environ>=0.12.0,<0.13
python-dotenv>=1.1.1,<2
whitenoise>=6.9.0,<7
gunicorn>=23.0.0,<24
str2bool>=1.1

django-theme-material-kit>=1.0.18

google-generativeai>=0.8.5,<1
PyPDF2>=3.0.1,<4
requests>=2.32.5,<3

pytest>=8.4.2,<9
pytest-django>=4.11.1,<5
coverage>=7.10.7,<8
bleach>=6.3.0,<7
Jinja2>=3.1.6,<4
```
