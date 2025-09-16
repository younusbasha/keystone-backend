import json
import os

# Required endpoints from user (trimmed to exact path patterns)
required = [
    # Auth & Users
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/auth/logout",
    "/api/v1/auth/refresh",
    "/api/v1/auth/me",
    "/api/v1/auth/me",
    "/api/v1/auth/change-password",
    "/api/v1/auth/forgot-password",
    "/api/v1/auth/reset-password",
    "/api/v1/users/",
    "/api/v1/users/",
    "/api/v1/users/",
    "/api/v1/users/",
    # Projects
    "/api/v1/projects/",
    "/api/v1/projects/",
    "/api/v1/projects/",
    "/api/v1/projects/",
    "/api/v1/projects/",
    "/api/v1/projects/{id}/stats",
    "/api/v1/projects/{id}/team",
    "/api/v1/projects/{id}/team",
    "/api/v1/projects/{id}/team/{user_id}",
    "/api/v1/projects/{id}/status",
    "/api/v1/projects/{id}/timeline",
    # Requirements
    "/api/v1/requirements/",
    "/api/v1/requirements/",
    "/api/v1/requirements/{id}",
    "/api/v1/requirements/{id}",
    "/api/v1/requirements/{id}",
    "/api/v1/requirements/project/{project_id}",
    "/api/v1/requirements/{id}/analyze",
    "/api/v1/requirements/analyze",
    "/api/v1/requirements/{id}/generate-tasks",
    "/api/v1/requirements/{id}/status",
    "/api/v1/requirements/{id}/history",
    "/api/v1/requirements/{id}/approve",
    "/api/v1/requirements/{id}/reject",
    # Tasks (subset)
    "/api/v1/tasks/",
    "/api/v1/tasks/",
    "/api/v1/tasks/{id}",
    "/api/v1/tasks/{id}",
    "/api/v1/tasks/{id}",
    "/api/v1/tasks/{id}/status",
    "/api/v1/tasks/{id}/start",
    "/api/v1/tasks/{id}/complete",
    "/api/v1/tasks/{id}/pause",
    "/api/v1/tasks/{id}/resume",
    "/api/v1/tasks/{id}/comments",
    "/api/v1/tasks/{id}/comments",
    "/api/v1/tasks/{id}/comments/{comment_id}",
    "/api/v1/tasks/{id}/comments/{comment_id}",
    "/api/v1/tasks/{id}/assign",
    "/api/v1/tasks/{id}/unassign",
    "/api/v1/tasks/{id}/time-logs",
    "/api/v1/tasks/{id}/time-logs",
    "/api/v1/tasks/{id}/time-logs/{log_id}",
    "/api/v1/tasks/{id}/attachments",
    "/api/v1/tasks/{id}/attachments",
    "/api/v1/tasks/{id}/attachments/{attachment_id}",
    # Agents (subset)
    "/api/v1/agents/",
    "/api/v1/agents/",
    "/api/v1/agents/{id}",
    "/api/v1/agents/{id}",
    "/api/v1/agents/{id}",
    "/api/v1/agents/{id}/execute",
    "/api/v1/agents/{id}/start",
    "/api/v1/agents/{id}/stop",
    "/api/v1/agents/{id}/actions",
    "/api/v1/agents/{id}/actions",
    "/api/v1/agents/actions/{action_id}",
    "/api/v1/agents/actions/{action_id}",
    "/api/v1/agents/actions/{action_id}/approve",
    "/api/v1/agents/actions/{action_id}/reject",
    "/api/v1/agents/actions/{action_id}/retry",
    "/api/v1/agents/analytics/overview",
    "/api/v1/agents/analytics/performance",
    "/api/v1/agents/{id}/logs",
    "/api/v1/agents/{id}/metrics",
    "/api/v1/agents/{id}/configure",
    "/api/v1/agents/templates",
    # Integrations & Deployments (subset)
    "/api/v1/integrations/",
    "/api/v1/integrations/",
    "/api/v1/integrations/{id}",
    "/api/v1/integrations/{id}",
    "/api/v1/integrations/{id}",
    "/api/v1/integrations/{id}/test",
    "/api/v1/integrations/{id}/sync",
    "/api/v1/integrations/{id}/logs",
    "/api/v1/integrations/{id}/enable",
    "/api/v1/integrations/{id}/disable",
    "/api/v1/integrations/types",
    "/api/v1/integrations/{id}/webhook",
    "/api/v1/integrations/deployments/",
    "/api/v1/integrations/deployments/",
    "/api/v1/integrations/deployments/{id}",
    "/api/v1/integrations/deployments/{id}",
    "/api/v1/integrations/deployments/{id}",
    "/api/v1/integrations/deployments/{id}/rollback",
    "/api/v1/integrations/deployments/{id}/promote",
    "/api/v1/integrations/deployments/{id}/logs",
    "/api/v1/integrations/deployments/{id}/status",
    "/api/v1/integrations/deployments/{id}/restart",
    "/api/v1/integrations/deployments/environments",
    # Dashboard, Search, Audit, Admin, Files, Permissions, Reports abbreviated
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

# Read collection
coll_path = os.path.join(os.getcwd(), 'TechSophy_Keystone_Postman_Collection.json')
collection = {}
if os.path.exists(coll_path):
    collection = json.load(open(coll_path, 'r', encoding='utf-8'))

# Read code files
code_text = ''
for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'app', 'api', 'v1', 'endpoints')):
    for f in files:
        if f.endswith('.py'):
            code_text += open(os.path.join(root,f),'r',encoding='utf-8').read() + '\n'

# Flatten collection URLs
coll_urls = set()
for item in collection.get('item',[]):
    def walk(i):
        if 'request' in i and 'url' in i['request']:
            url = i['request']['url']
            raw = url.get('raw') if isinstance(url, dict) else None
            if raw:
                coll_urls.add(raw)
        for sub in i.get('item',[]):
            walk(sub)
    walk(item)

print('Checked endpoints:', len(required))
print('Found in collection / code (format: endpoint -> in_collection, in_code)')
missing = []
for ep in required:
    in_coll = any(ep.rstrip('/') in u for u in coll_urls)
    in_code = ep.replace('/api/v1','').rstrip('/') in code_text or ep.rstrip('/') in code_text
    print(f"{ep} -> {in_coll}, {in_code}")
    if not (in_coll and in_code):
        missing.append((ep,in_coll,in_code))

print('\nSUMMARY: total missing routes:', len(missing))
for m in missing[:50]:
    print(m)

# write report
open('api_coverage_report.txt','w',encoding='utf-8').write(json.dumps({'missing':missing},default=str,indent=2))
print('\nReport written to api_coverage_report.txt')

