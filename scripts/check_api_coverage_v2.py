#!/usr/bin/env python3
"""
Improved API coverage checker with router prefix mapping
"""
import os, re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENDPOINTS_DIR = ROOT / 'app' / 'api' / 'v1' / 'endpoints'
ROUTER_FILE = ROOT / 'app' / 'api' / 'v1' / 'router.py'
COLLECTION_FILE = ROOT / 'TechSophy_Keystone_Postman_Collection.json'
REPORT_FILE = ROOT / 'api_coverage_report_v2.json'

# Required endpoints (from user) - simplified normalized forms
REQUIRED = [
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/auth/logout",
    "/api/v1/auth/refresh",
    "/api/v1/auth/me",
    "/api/v1/auth/me",  # PUT
    "/api/v1/auth/change-password",
    "/api/v1/auth/forgot-password",
    "/api/v1/auth/reset-password",
    "/api/v1/users/",
    "/api/v1/users/{id}",
    "/api/v1/projects/",
    "/api/v1/projects/{id}",
    "/api/v1/projects/{id}/stats",
    "/api/v1/projects/{id}/team",
    "/api/v1/projects/{id}/team/{user_id}",
    "/api/v1/projects/{id}/status",
    "/api/v1/projects/{id}/timeline",
    "/api/v1/requirements/",
    "/api/v1/requirements/{id}",
    "/api/v1/requirements/project/{project_id}",
    "/api/v1/requirements/{id}/analyze",
    "/api/v1/requirements/analyze",
    "/api/v1/requirements/{id}/generate-tasks",
    "/api/v1/requirements/{id}/status",
    "/api/v1/requirements/{id}/history",
    "/api/v1/requirements/{id}/approve",
    "/api/v1/requirements/{id}/reject",
    "/api/v1/tasks/",
    "/api/v1/tasks/{id}",
    "/api/v1/tasks/{id}/status",
    "/api/v1/tasks/{id}/start",
    "/api/v1/tasks/{id}/complete",
    "/api/v1/tasks/{id}/pause",
    "/api/v1/tasks/{id}/resume",
    "/api/v1/tasks/{id}/comments",
    "/api/v1/tasks/{id}/comments/{comment_id}",
    "/api/v1/tasks/{id}/assign",
    "/api/v1/tasks/{id}/unassign",
    "/api/v1/tasks/{id}/time-logs",
    "/api/v1/tasks/{id}/attachments",
    "/api/v1/agents/",
    "/api/v1/agents/{id}",
    "/api/v1/agents/{id}/execute",
    "/api/v1/agents/{id}/start",
    "/api/v1/agents/{id}/stop",
    "/api/v1/agents/{id}/actions",
    "/api/v1/agents/actions/{action_id}",
    "/api/v1/agents/actions/{action_id}/approve",
    "/api/v1/agents/actions/{action_id}/reject",
    "/api/v1/agents/actions/{action_id}/retry",
    "/api/v1/agents/analytics/overview",
    "/api/v1/agents/analytics/performance",
    "/api/v1/integrations/",
    "/api/v1/integrations/{id}",
    "/api/v1/integrations/{id}/test",
    "/api/v1/integrations/{id}/sync",
    "/api/v1/integrations/{id}/logs",
    "/api/v1/integrations/{id}/enable",
    "/api/v1/integrations/{id}/disable",
    "/api/v1/integrations/types",
    "/api/v1/integrations/{id}/webhook",
    "/api/v1/integrations/deployments/",
    "/api/v1/integrations/deployments/{id}",
    "/api/v1/integrations/deployments/{id}/rollback",
    "/api/v1/integrations/deployments/{id}/promote",
    "/api/v1/dashboard/overview",
    "/api/v1/dashboard/stats",
    "/api/v1/dashboard/metrics",
    "/api/v1/dashboard/activity-feed",
    "/api/v1/search/",
    "/api/v1/audit/logs/",
    "/api/v1/admin/health/",
    "/api/v1/files/upload/",
    "/api/v1/permissions/",
    "/api/v1/reports/"
]

# helpers
RE_METHOD = re.compile(r"@router\.(get|post|put|delete|patch)\((?P<quote>[\"'])?(?P<path>[^\"'\)]+)(?P=quote)?")
RE_INCLUDE = re.compile(r"include_router\((?P<module>\w+)\.router\s*,\s*prefix\s*=\s*['\"](?P<prefix>/[^'\"]*)['\"]")


def normalize_path(p: str) -> str:
    """Normalize paths: strip trailing slash, replace parameter patterns with {id} style"""
    if not p:
        return p
    p = p.strip()
    # remove leading/trailing quotes, whitespace
    p = p.strip(' \"\'')
    # ensure starts with /
    if not p.startswith('/'):
        p = '/' + p
    # Replace Flask style <uuid:id> or :id with {id}
    p = re.sub(r"<[^:>]+:([^>]+)>", r"{\1}", p)
    p = re.sub(r":(\w+)", r"{\1}", p)
    # Replace {param:.+} or regex groups to {param}
    p = re.sub(r"\{(\w+):[^}]+\}", r"{\1}", p)
    # collapse multiple slashes
    p = re.sub(r"//+", r"/", p)
    # strip trailing slash except root
    if p.endswith('/') and len(p) > 1:
        p = p[:-1]
    return p


def load_router_prefixes():
    mapping = {}
    if not ROUTER_FILE.exists():
        return mapping
    txt = ROUTER_FILE.read_text(encoding='utf-8')
    for m in RE_INCLUDE.finditer(txt):
        module = m.group('module')
        prefix = m.group('prefix')
        mapping[module] = prefix
    return mapping


def extract_code_paths():
    paths = set()
    prefixes = load_router_prefixes()
    if not ENDPOINTS_DIR.exists():
        return paths
    for py in ENDPOINTS_DIR.glob('*.py'):
        txt = py.read_text(encoding='utf-8')
        module = py.stem
        prefix = prefixes.get(module, '')
        for m in RE_METHOD.finditer(txt):
            raw = m.group('path')
            norm = normalize_path(raw)
            full = '/api/v1' + (prefix + norm if prefix else norm)
            full = re.sub(r"//+", '/', full)
            paths.add(full)
    return paths


def extract_collection_paths():
    paths = set()
    if not COLLECTION_FILE.exists():
        return paths
    coll = json.loads(COLLECTION_FILE.read_text(encoding='utf-8'))
    def walk(items):
        for it in items:
            if 'request' in it and 'url' in it['request']:
                url = it['request']['url']
                raw = url.get('raw') if isinstance(url, dict) else url
                if raw:
                    # extract path part after base_url
                    u = raw
                    # remove scheme and host if present
                    u = re.sub(r"https?://[^/]+", '', u)
                    # normalize
                    u = normalize_path(u)
                    paths.add(u)
            if 'item' in it:
                walk(it['item'])
    walk(coll.get('item', []))
    return paths


def main():
    code_paths = extract_code_paths()
    coll_paths = extract_collection_paths()

    report = {
        'required_count': len(REQUIRED),
        'code_paths_count': len(code_paths),
        'collection_paths_count': len(coll_paths),
        'required': []
    }

    for ep in REQUIRED:
        norm = normalize_path(ep)
        in_code = norm in code_paths
        in_coll = norm in coll_paths
        report['required'].append({'endpoint': ep, 'normalized': norm, 'in_code': in_code, 'in_collection': in_coll})

    report['code_only'] = sorted(list(code_paths - coll_paths))
    report['collection_only'] = sorted(list(coll_paths - code_paths))

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print('Wrote report to', REPORT_FILE.name)

if __name__ == '__main__':
    main()
