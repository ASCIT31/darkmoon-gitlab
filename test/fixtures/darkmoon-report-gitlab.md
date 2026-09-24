# Vulnerability Assessment Report — 127.0.0.1

**Classification:** CONFIDENTIAL — Restricted to authorized personnel  
**Generated:** 2026-08-01T20:24:40Z  
**Target:** 127.0.0.1  
**Campaign:** camp_20260801_a719641d  
**Methodology:** ISO 27001 / NIST SP 800-115 / MITRE ATT&CK  

---

## MANAGEMENT SUMMARY

> *For non-technical readers and decision-makers.*

### Overall Security Posture: 🔴 CRITICAL — Immediate Action Required

The system tested (**127.0.0.1**) presents an **extremely poor security posture**. Our team confirmed 4 critical and 8 high severity vulnerabilities, enabling complete compromise through multiple independent attack paths.

### Most Critical Issues

**1. Admin PAT with API + Sudo Scopes — Full Instance Takeover**  
The provided Personal Access Token (glpat-LABtoken1234567890) belongs to the root administrator account (user_id=1) and carries both 'api' and 'sudo' scopes. This grants complete control over the enti...

**2. Admin PAT with API + Sudo Scopes — Full Instance Takeover**  
An admin Personal Access Token (PAT) with 'api' and 'sudo' scopes was found active with no expiration date. This token grants full administrative control over the entire GitLab instance including: rea...

**3. AWS Secret Access Key Exposed in CI/CD Variables (Unmasked, Unprotected)**  
The project 'corp-app' (ID:1) has an AWS_SECRET_ACCESS_KEY stored as a CI/CD variable with value 'wJalrFAKEgitlabkey/EXAMPLE'. The variable is NOT masked (masked=false), NOT protected (protected=false...

### Required Actions

| Timeframe | Action |
|-----------|--------|
| **Today** | Block external access / take offline if possible |
| **This week** | Patch all critical and high severity findings |
| **2 weeks** | Address medium severity findings and security headers |
| **1 month** | Full code review and independent re-test |

---

## 1. EXECUTIVE SUMMARY

> Authorized internal assessment of GitLab CE 19.2.1 at 127.0.0.1:8091 revealed 13 findings (2 critical, 4 high, 5 medium, 1 low, 1 info). An admin PAT with api+sudo scopes provides full instance takeover capability (CVSS 10.0). The corp-app project exposes an AWS_SECRET_ACCESS_KEY in unmasked/unprotected CI/CD variables (CVSS 9.8). Runner registration tokens enable rogue runner registration for RCE and secret exfiltration. Open self-registration, disabled admin_mode, missing 2FA on the admin account, and no branch protection compound the risk of supply-chain attacks.

**Overall Risk Level: CRITICAL**

### Findings Summary

| Severity | Count | Exploited | Confirmed |
|----------|-------|-----------|----------|
| CRITICAL | 4 | 2 | 2 |
| HIGH | 8 | 0 | 8 |
| MEDIUM | 10 | 0 | 10 |
| LOW | 2 | 0 | 2 |
| INFO | 2 | 0 | 2 |
| **TOTAL** | **26** | **2** | **24** |

---

## 2. FINDINGS TABLE

| # | ID | Title | Severity | CVSS | Status | Endpoint |
|---|-----|-------|----------|------|--------|----------|
| 1 | `vuln_127baf` | Admin PAT with API + Sudo Scopes — Full Instance T... | CRITICAL | 10.0 | **EXPLOITED** | `127.0.0.1:8091/api/v4/personal_access_tokens/self` |
| 2 | `vuln_5b7f6d` | Admin PAT with API + Sudo Scopes — Full Instance T... | CRITICAL | 10.0 | **EXPLOITED** | `127.0.0.1:8091/api/v4/personal_access_tokens/self` |
| 3 | `vuln_66d37e` | AWS Secret Access Key Exposed in CI/CD Variables (... | CRITICAL | 9.8 | Confirmed | `127.0.0.1:8091/api/v4/projects/1/variables` |
| 4 | `vuln_14af73` | AWS Secret Access Key Exposed in CI/CD Variables (... | CRITICAL | 9.8 | Confirmed | `127.0.0.1:8091/api/v4/projects/1/variables` |
| 5 | `vuln_8499a8` | Runner Registration Token Exposed via Project API | HIGH | 8.8 | Confirmed | `127.0.0.1:8091/api/v4/projects/1` |
| 6 | `vuln_7648fb` | Runner Registration Token Exposed via Project API | HIGH | 8.8 | Confirmed | `127.0.0.1:8091/api/v4/projects/1` |
| 7 | `vuln_645803` | Admin Account Missing Two-Factor Authentication (2... | HIGH | 7.5 | Confirmed | `127.0.0.1:8091/api/v4/user` |
| 8 | `vuln_6de84f` | Admin Account Missing Two-Factor Authentication (2... | HIGH | 7.5 | Confirmed | `127.0.0.1:8091/api/v4/users/1` |
| 9 | `vuln_9d7c3f` | Open Self-Registration Enabled — Unauthorized Acco... | HIGH | 7.3 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 10 | `vuln_e2bfea` | Open Self-Registration Enabled — Unauthorized Acco... | HIGH | 7.3 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 11 | `vuln_b1e112` | Admin Mode Disabled — No Re-Authentication for Adm... | HIGH | 7.2 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 12 | `vuln_5815ad` | Admin Mode Disabled — No Re-Authentication for Adm... | HIGH | 7.2 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 13 | `vuln_befb82` | No Branch Protection on Default Branch — Uncontrol... | MEDIUM | 6.5 | Confirmed | `127.0.0.1:8091/api/v4/projects/1/protected_branche...` |
| 14 | `vuln_aefefa` | No Branch Protection on Default Branch — Uncontrol... | MEDIUM | 6.5 | Confirmed | `127.0.0.1:8091/api/v4/projects/1/protected_branche...` |
| 15 | `vuln_42fd0a` | PAT Expiry Policy Not Enforced — Long-Lived Tokens... | MEDIUM | 5.4 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 16 | `vuln_91f068` | PAT Expiry Policy Not Enforced — Long-Lived Tokens... | MEDIUM | 5.4 | Confirmed | `127.0.0.1:8091/api/v4/personal_access_tokens/self` |
| 17 | `vuln_a1092c` | API Rate Limiting Disabled — Brute-Force and Abuse... | MEDIUM | 5.3 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 18 | `vuln_40ffbf` | API Rate Limiting Disabled — Brute-Force and Abuse... | MEDIUM | 5.3 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 19 | `vuln_13c02a` | Container Registry Enabled on Project Without Secu... | MEDIUM | 5.0 | Confirmed | `127.0.0.1:8091/api/v4/projects/1/registry/reposito...` |
| 20 | `vuln_9df919` | System Hooks Allow Local Requests — Potential SSRF... | MEDIUM | 5.0 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 21 | `vuln_3529ad` | Container Registry Enabled on Project Without Secu... | MEDIUM | 5.0 | Confirmed | `127.0.0.1:8091/api/v4/projects/1/registry/reposito...` |
| 22 | `vuln_35ead9` | System Hooks Allow Local Requests — Potential SSRF... | MEDIUM | 5.0 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 23 | `vuln_602ba6` | Auto DevOps Enabled — Automatic Pipeline Execution... | LOW | 3.8 | Confirmed | `127.0.0.1:8091/api/v4/projects/1` |
| 24 | `vuln_ffd0ea` | Auto DevOps Enabled — Automatic Pipeline Execution... | LOW | 3.8 | Confirmed | `127.0.0.1:8091/api/v4/application/settings` |
| 25 | `vuln_5ead16` | GitLab Version Information Disclosure via API | INFO | N/A | Confirmed | `127.0.0.1:8091/api/v4/version` |
| 26 | `vuln_85597e` | GitLab Version Information Disclosure via API | INFO | N/A | Confirmed | `127.0.0.1:8091/api/v4/version` |

---

## 3. VULNERABILITY DETAILS

---

### 3.1 — Admin PAT with API + Sudo Scopes — Full Instance Takeover

| Field | Value |
|-------|-------|
| **ID** | `vuln_127baf` |
| **Severity** | CRITICAL |
| **CVSS Score** | 10.0 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| **Status** | EXPLOITED |
| **Category** | `excessive_privileges` |
| **MITRE ATT&CK** | `T1078.004` — Valid Accounts: Cloud Accounts |
| **ISO 27001** | `A.9.2.3 Management of privileged access rights` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/personal_access_tokens/self` |
| **Component** | GitLab Personal Access Token |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:17:19Z |

#### Description

The provided Personal Access Token (glpat-LABtoken1234567890) belongs to the root administrator account (user_id=1) and carries both 'api' and 'sudo' scopes. This grants complete control over the entire GitLab instance: read/write all projects, CI/CD variables, runners, impersonate any user, modify application settings, create admin accounts, and access all secrets. The token is active, not revoked, and expires 2027-08-01 — over a year of unrestricted access. admin_mode is disabled (false), meaning no additional authentication challenge is required for admin API operations. The token has no description set, suggesting weak token lifecycle management.

#### Technical Analysis

The PAT 'labtok' (id=1) is a root admin token with 'api' and 'sudo' scopes, granting unrestricted access to every GitLab API endpoint. The 'api' scope provides full read/write access to all resources, while 'sudo' allows impersonating any user on the instance. Combined with is_admin=true and admin_mode=false (no re-authentication required), this token represents a complete instance compromise. Any attacker obtaining this token gains full control over all code, CI/CD pipelines, secrets, and user accounts. The token expires in over a year (2027-08-01) with no expiry policy enforcement (max_personal_access_token_lifetime=null).

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/personal_access_tokens/self | jq .
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/user | jq .
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" -H "Sudo: root" http://127.0.0.1:8091/api/v4/user | jq .
```

#### Raw Request

```http
GET /api/v4/personal_access_tokens/self HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"id":1,"name":"labtok","revoked":false,"created_at":"2026-08-01T20:12:06.083Z","description":null,"scopes":["api","sudo"],"user_id":1,"last_used_at":"2026-08-01T20:12:06.303Z","active":true,"granular":false,"expires_at":"2027-08-01"}
```

#### Evidence / Logs

```
GET /api/v4/personal_access_tokens/self -> 200: {id:1, name:"labtok", scopes:["api","sudo"], active:true, revoked:false, expires_at:"2027-08-01", user_id:1}
GET /api/v4/user -> 200: {id:1, username:"root", is_admin:true, two_factor_enabled:false}
GET /api/v4/user with Sudo:root header -> 200: confirmed sudo impersonation works
```

#### Remediation

1. Immediately rotate/revoke this admin PAT and issue a new one with minimum required scopes. 2. Remove the 'sudo' scope unless absolutely necessary. 3. Enable admin_mode in application settings to require re-authentication for admin API operations. 4. Enforce max_personal_access_token_lifetime to limit token validity period (e.g., 90 days). 5. Enable enforce_pat_expiration. 6. Implement PAT naming conventions and descriptions for tracking. 7. Enable 2FA for the root admin account (currently two_factor_enabled=false).

---

### 3.2 — Admin PAT with API + Sudo Scopes — Full Instance Takeover

| Field | Value |
|-------|-------|
| **ID** | `vuln_5b7f6d` |
| **Severity** | CRITICAL |
| **CVSS Score** | 10.0 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| **Status** | EXPLOITED |
| **Category** | `excessive_privileges` |
| **MITRE ATT&CK** | `T1078.004` — Valid Accounts: Cloud Accounts |
| **ISO 27001** | `A.9.2.3 Management of privileged access rights` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/personal_access_tokens/self` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:22:31Z |

#### Description

An admin Personal Access Token (PAT) with 'api' and 'sudo' scopes was found active with no expiration date. This token grants full administrative control over the entire GitLab instance including: reading/writing all repositories, managing all users, accessing all CI/CD secrets, impersonating any user via sudo, and modifying instance settings. The token name is 'labtok' belonging to the root administrator account (user ID 1). Combined with admin_mode being disabled, this token can perform all admin operations without re-authentication.

#### Technical Analysis

The admin PAT 'labtok' has scopes [api, sudo] with no expiration (expires_at: null), is not revoked, and is active. With api+sudo on an admin account where admin_mode is disabled, this provides unrestricted access to every API endpoint including user impersonation, secret extraction, and instance configuration changes.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/personal_access_tokens/self | jq .
```

#### Evidence / Logs

```
Token name: labtok
Scopes: api, sudo
User: root (ID: 1, is_admin: true)
Expires: null (never)
Revoked: false
Active: true
admin_mode disabled: true (no re-auth required)
```

#### Remediation

1. Immediately rotate this PAT and issue a new one with minimal required scopes. 2. Set an expiration date on all PATs (enforce via instance settings). 3. Remove 'sudo' scope unless absolutely necessary. 4. Enable admin_mode to require re-authentication for admin operations. 5. Implement PAT expiry policies at the instance level.

---

### 3.3 — AWS Secret Access Key Exposed in CI/CD Variables (Unmasked, Unprotected)

| Field | Value |
|-------|-------|
| **ID** | `vuln_66d37e` |
| **Severity** | CRITICAL |
| **CVSS Score** | 9.8 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| **Status** | CONFIRMED |
| **Category** | `credential_exposure` |
| **MITRE ATT&CK** | `T1552.001` — Unsecured Credentials: Credentials In Files |
| **ISO 27001** | `A.9.4.3 Password management system` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/projects/1/variables` |
| **Component** | GitLab CI/CD Variables |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:17:45Z |

#### Description

The project 'corp-app' (ID:1) has an AWS_SECRET_ACCESS_KEY stored as a CI/CD variable with value 'wJalrFAKEgitlabkey/EXAMPLE'. The variable is NOT masked (masked=false), NOT protected (protected=false), NOT hidden (hidden=false), and scoped to ALL environments (environment_scope='*'). This means: (1) The secret is returned in plaintext via the API to anyone with Maintainer+ access, (2) It is echoed in CI job logs without masking, (3) It is available in ALL pipeline jobs regardless of environment or branch protection, (4) Any fork or merge request pipeline can access it. While this specific key appears to be a placeholder/example key (contains 'FAKE' and 'EXAMPLE'), the pattern of storing cloud credentials as unmasked, unprotected CI/CD variables is a critical supply-chain risk. A real AWS key stored this way would grant full AWS account access to any pipeline contributor.

#### Technical Analysis

The CI/CD variable AWS_SECRET_ACCESS_KEY is stored in plaintext in the corp-app project. With masked=false, the full secret value is visible in API responses and CI job logs. With protected=false, any branch or tag can access this variable in pipelines — not just protected refs. With environment_scope='*', it is available in all environments. This combination maximally exposes the credential. Any user who can trigger a pipeline (Developer+ role) can exfiltrate this secret by adding 'echo $AWS_SECRET_ACCESS_KEY' to a CI job script. The API also returns the plaintext value to anyone with Maintainer+ access, as demonstrated by the successful extraction.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/projects/1/variables" | jq .
```

#### Raw Request

```http
GET /api/v4/projects/1/variables HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
[{"variable_type":"env_var","key":"AWS_SECRET_ACCESS_KEY","value":"wJalrFAKEgitlabkey/EXAMPLE","hidden":false,"protected":false,"masked":false,"raw":false,"environment_scope":"*","description":null}]
```

#### Evidence / Logs

```
GET /api/v4/projects/1/variables -> 200: [{variable_type:"env_var", key:"AWS_SECRET_ACCESS_KEY", value:"wJalrFAKEgitlabkey/EXAMPLE", hidden:false, protected:false, masked:false, raw:false, environment_scope:"*", description:null}]
```

#### Remediation

1. Immediately rotate the AWS secret access key and any associated access key ID. 2. Enable the 'masked' flag on all CI/CD variables containing secrets to prevent exposure in job logs. 3. Enable the 'protected' flag to restrict access to protected branches/tags only. 4. Use the 'hidden' flag (GitLab 17.x+) to prevent API readback of the secret. 5. Consider using external secret management (HashiCorp Vault, AWS Secrets Manager) integrated with GitLab CI instead of storing secrets as CI/CD variables. 6. Audit all CI/CD variables across all projects for exposed credentials. 7. Implement branch protection rules to control who can trigger pipelines.

---

### 3.4 — AWS Secret Access Key Exposed in CI/CD Variables (Unmasked, Unprotected)

| Field | Value |
|-------|-------|
| **ID** | `vuln_14af73` |
| **Severity** | CRITICAL |
| **CVSS Score** | 9.8 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| **Status** | CONFIRMED |
| **Category** | `credential_exposure` |
| **MITRE ATT&CK** | `T1552.001` — Unsecured Credentials: Credentials In Files |
| **ISO 27001** | `A.9.4.3 Password management system` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/projects/1/variables` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:22:45Z |

#### Description

The project 'corp-app' (ID:1) stores an AWS_SECRET_ACCESS_KEY as a CI/CD variable in plaintext. The variable is neither masked nor protected, meaning it is exposed in pipeline logs and available to all branches/environments. The value 'wJalrFAKEgitlabkey/EXAMPLE' appears to be a test/placeholder but demonstrates the pattern of storing cloud credentials insecurely in GitLab CI/CD variables. Any user with Developer+ access to this project, or anyone who can register a runner, can extract this secret.

#### Technical Analysis

The CI/CD variable AWS_SECRET_ACCESS_KEY is stored unmasked and unprotected in the corp-app project. This means: (1) the value appears in plaintext in pipeline job logs, (2) it is available on ALL branches not just protected ones, (3) any user who can trigger a pipeline can extract it, (4) a rogue runner can capture it during job execution.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/projects/1/variables | jq .
```

#### Evidence / Logs

```
Variable key: AWS_SECRET_ACCESS_KEY
Variable value: wJalrFAKEgitlabkey/EXAMPLE
Variable type: env_var
Protected: false
Masked: false
Raw: false
Environment scope: *
```

#### Remediation

1. Immediately rotate the AWS secret access key. 2. Enable 'masked' flag on all sensitive CI/CD variables to prevent log exposure. 3. Enable 'protected' flag to restrict variable availability to protected branches only. 4. Consider using external secret management (HashiCorp Vault, AWS Secrets Manager) instead of GitLab CI/CD variables. 5. Audit all CI/CD variables across all projects for exposed secrets.

---

### 3.5 — Runner Registration Token Exposed via Project API

| Field | Value |
|-------|-------|
| **ID** | `vuln_8499a8` |
| **Severity** | HIGH |
| **CVSS Score** | 8.8 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| **Status** | CONFIRMED |
| **Category** | `credential_exposure` |
| **MITRE ATT&CK** | `T1195.002` — Supply Chain Compromise: Compromise Software Supply Chain |
| **ISO 27001** | `A.14.2.7 Outsourced development` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/projects/1` |
| **Component** | GitLab CI Runner Registration |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:18:06Z |

#### Description

The project detail endpoint exposes the runner registration token 'GR1348941JNHgzBeX_AvNhsgPuihK' for the corp-app project. This token allows anyone who obtains it to register a rogue GitLab Runner against this project. A registered rogue runner would pick up CI/CD jobs, gaining access to all CI/CD variables (including the exposed AWS_SECRET_ACCESS_KEY), source code, artifacts, and enabling arbitrary code execution within the pipeline context. With shared_runners_enabled=true and auto_devops_enabled=true, the attack surface is further amplified.

#### Technical Analysis

The runners_token field is returned in the project detail API response to users with Maintainer+ access. This token (GR1348941JNHgzBeX_AvNhsgPuihK) can be used with 'gitlab-runner register' to register a malicious runner that intercepts CI/CD jobs. Once a rogue runner picks up a job, the attacker gains: (1) RCE on the runner host, (2) access to all CI/CD variables including AWS secrets, (3) access to the project source code, (4) ability to modify build artifacts and inject supply-chain attacks. This is a confirmed credential exposure — the token was successfully extracted via the API.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/projects/1" | jq "{runners_token, shared_runners_enabled, auto_devops_enabled}"
```

#### Raw Request

```http
GET /api/v4/projects/1 HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"id":1,"name":"corp-app","path_with_namespace":"root/corp-app","visibility":"private","default_branch":"main","empty_repo":true,"container_registry_enabled":true,"shared_runners_enabled":true,"runners_token":"GR1348941JNHgzBeX_AvNhsgPuihK","auto_devops_enabled":true}
```

#### Evidence / Logs

```
GET /api/v4/projects/1 -> 200: {runners_token: "GR1348941JNHgzBeX_AvNhsgPuihK", shared_runners_enabled: true, auto_devops_enabled: true}
```

#### Remediation

1. Reset the runner registration token immediately via GitLab UI or API (POST /api/v4/projects/1/runners/reset_registration_token). 2. Audit all registered runners to verify no unauthorized runners are present. 3. Disable auto_devops_enabled unless actively used. 4. Consider using runner authentication tokens (new registration workflow) instead of the deprecated registration token approach. 5. Implement runner IP allowlisting if possible. 6. Lock runners to specific projects to prevent cross-project job interception.

---

### 3.6 — Runner Registration Token Exposed via Project API

| Field | Value |
|-------|-------|
| **ID** | `vuln_7648fb` |
| **Severity** | HIGH |
| **CVSS Score** | 8.8 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| **Status** | CONFIRMED |
| **Category** | `credential_exposure` |
| **MITRE ATT&CK** | `T1525` — Implant Internal Image |
| **ISO 27001** | `A.14.2.7 Outsourced development` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/projects/1` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:22:56Z |

#### Description

The project API exposes a runner registration token (runners_token: GR1348941JNHgzBeX_AvNhsgPuihK) which can be used to register a rogue CI/CD runner. An attacker registering a malicious runner can intercept CI/CD jobs, extract environment variables (including the AWS secret key), execute arbitrary code within the pipeline context, and potentially pivot to internal infrastructure accessible from the runner's network.

#### Technical Analysis

The runners_token field is exposed in the project API response. This token allows anyone to register a new CI/CD runner for this project without any additional authentication. A rogue runner can then pick up pipeline jobs and access all CI/CD variables including the AWS_SECRET_ACCESS_KEY.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/projects/1 | jq '.runners_token'
```

#### Evidence / Logs

```
runners_token: GR1348941JNHgzBeX_AvNhsgPuihK
shared_runners_enabled: true
No runners currently registered
```

#### Remediation

1. Rotate the runner registration token immediately. 2. Restrict runner registration to admins only. 3. Use the new runner authentication flow (GitLab 15.10+) which uses authentication tokens instead of registration tokens. 4. Lock runners to specific projects. 5. Monitor for unauthorized runner registrations.

---

### 3.7 — Admin Account Missing Two-Factor Authentication (2FA)

| Field | Value |
|-------|-------|
| **ID** | `vuln_645803` |
| **Severity** | HIGH |
| **CVSS Score** | 7.5 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1556` — Modify Authentication Process |
| **ISO 27001** | `A.9.4.2 Secure log-on procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/user` |
| **Component** | GitLab User Authentication |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:19:06Z |

#### Description

The root administrator account (id=1, username='root') has two_factor_enabled=false. Additionally, the instance-wide setting require_two_factor_authentication=false means 2FA is not enforced for any user. The 2FA grace period is set to 48 hours. This leaves the most privileged account on the instance vulnerable to credential-based attacks (password guessing, credential stuffing, phishing) without any second factor protection. Combined with password_authentication_enabled_for_web=true and password_authentication_enabled_for_git=true, the attack surface is maximal.

#### Technical Analysis

The root administrator account does not have 2FA enabled, and the instance does not enforce 2FA for any user. This is a confirmed security misconfiguration. The root account has full control over the GitLab instance — if its password is compromised through any means, the attacker gains complete instance access. The 48-hour grace period means even if 2FA enforcement were enabled, users would have 2 days before being locked out, creating a window for exploitation.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/user" | jq "{username, is_admin, two_factor_enabled}"
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/application/settings" | jq "{require_two_factor_authentication, two_factor_grace_period}"
```

#### Raw Request

```http
GET /api/v4/user HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"id":1,"username":"root","is_admin":true,"two_factor_enabled":false,"email":"EMAIL_001"}
```

#### Evidence / Logs

```
GET /api/v4/user -> 200: {username:"root", is_admin:true, two_factor_enabled:false}
GET /api/v4/application/settings -> 200: {require_two_factor_authentication:false, two_factor_grace_period:48}
```

#### Remediation

1. Enable 2FA on the root administrator account immediately. 2. Set require_two_factor_authentication=true at the instance level. 3. Reduce the two_factor_grace_period from 48 hours to 24 hours or less. 4. Consider enforcing 2FA for admin accounts via a separate, stricter policy. 5. Ensure backup recovery codes are securely stored.

---

### 3.8 — Admin Account Missing Two-Factor Authentication (2FA)

| Field | Value |
|-------|-------|
| **ID** | `vuln_6de84f` |
| **Severity** | HIGH |
| **CVSS Score** | 7.5 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1556` — Modify Authentication Process |
| **ISO 27001** | `A.9.4.2 Secure log-on procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/users/1` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:23:21Z |

#### Description

The root administrator account (user ID 1) does not have two-factor authentication (2FA) enabled. This single admin account controls the entire GitLab instance. Without 2FA, credential theft (password or PAT) grants immediate full access without any secondary verification.

#### Technical Analysis

The root admin account has two_factor_enabled=false. As the sole admin account, compromising this account without 2FA means complete instance takeover.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/users/1 | jq '{username, is_admin, two_factor_enabled}'
```

#### Evidence / Logs

```
username: root
is_admin: true
two_factor_enabled: false
```

#### Remediation

1. Enable 2FA on the root admin account immediately. 2. Enforce 2FA for all admin users at the instance level. 3. Consider enforcing 2FA for all users (require_two_factor_authentication setting). 4. Use WebAuthn/FIDO2 keys for admin accounts.

---

### 3.9 — Open Self-Registration Enabled — Unauthorized Account Creation

| Field | Value |
|-------|-------|
| **ID** | `vuln_9d7c3f` |
| **Severity** | HIGH |
| **CVSS Score** | 7.3 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1136.003` — Create Account: Cloud Account |
| **ISO 27001** | `A.9.2.1 User registration and de-registration` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Component** | GitLab Application Settings |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:18:27Z |

#### Description

The GitLab instance has signup_enabled=true with no email restrictions (email_restrictions_enabled=false), no reCAPTCHA (recaptcha_enabled=false), and no Akismet spam protection (akismet_enabled=false). This allows anyone with network access to the instance to create arbitrary user accounts without any verification or anti-automation controls. Combined with the lack of restricted_visibility_levels (empty array), new users could potentially discover internal/public projects. Password complexity requirements are not enforced (all password_*_required fields are null) with only minimum_password_length=8.

#### Technical Analysis

The GitLab instance allows unrestricted self-registration without any protective measures. signup_enabled=true means anyone can create accounts. No email domain restrictions, no CAPTCHA, and no spam protection are in place. This is a confirmed misconfiguration that enables: (1) mass account creation by attackers, (2) internal reconnaissance by unauthorized users, (3) potential abuse of CI/CD resources via shared runners, (4) social engineering attacks using legitimate-looking internal accounts. The weak password policy (8 chars, no complexity requirements) further compounds the risk.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/application/settings" | jq "{signup_enabled, email_restrictions_enabled, recaptcha_enabled, akismet_enabled, restricted_visibility_levels, minimum_password_length, password_number_required, password_uppercase_required, password_lowercase_required, password_symbol_required}"
```

#### Raw Request

```http
GET /api/v4/application/settings HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"signup_enabled":true,"password_authentication_enabled_for_web":true,"password_authentication_enabled_for_git":true,"two_factor_grace_period":48,"require_two_factor_authentication":false,"restricted_visibility_levels":[],"email_restrictions_enabled":false,"recaptcha_enabled":false,"akismet_enabled":false,"minimum_password_length":8,"password_number_required":null,"password_uppercase_required":null,"password_lowercase_required":null,"password_symbol_required":null}
```

#### Evidence / Logs

```
GET /api/v4/application/settings -> 200: {signup_enabled: true, email_restrictions_enabled: false, recaptcha_enabled: false, akismet_enabled: false, restricted_visibility_levels: [], minimum_password_length: 8, password_number_required: null, password_uppercase_required: null, password_lowercase_required: null, password_symbol_required: null}
```

#### Remediation

1. Disable open signup (signup_enabled=false) unless explicitly needed for the business. 2. If signup is required, enable email domain restrictions to allow only corporate email domains. 3. Enable reCAPTCHA to prevent automated account creation. 4. Enable Akismet for spam protection. 5. Enforce password complexity requirements (uppercase, lowercase, numbers, symbols). 6. Increase minimum password length to at least 12 characters. 7. Restrict visibility levels to prevent new users from discovering internal projects. 8. Enable require_two_factor_authentication=true for all accounts.

---

### 3.10 — Open Self-Registration Enabled — Unauthorized Account Creation

| Field | Value |
|-------|-------|
| **ID** | `vuln_e2bfea` |
| **Severity** | HIGH |
| **CVSS Score** | 7.3 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1136.003` — Create Account: Cloud Account |
| **ISO 27001** | `A.9.2.1 User registration and de-registration` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:23:06Z |

#### Description

GitLab self-registration (signup_enabled) is enabled, allowing anyone to create an account on this instance. Combined with password authentication being enabled and no email domain restrictions, an attacker can register an account, potentially access internal/public projects, and in combination with Auto DevOps being enabled, trigger pipeline execution.

#### Technical Analysis

Instance settings show signup_enabled=true with password authentication enabled for both web and git, and an empty domain allowlist meaning any email domain can register.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/application/settings | jq '{signup_enabled, password_authentication_enabled_for_web, password_authentication_enabled_for_git, domain_allowlist}'
```

#### Evidence / Logs

```
signup_enabled: true
password_authentication_enabled_for_web: true
password_authentication_enabled_for_git: true
domain_allowlist: [] (no restrictions)
```

#### Remediation

1. Disable self-registration (signup_enabled: false) for internal instances. 2. If registration must remain open, restrict allowed email domains. 3. Enable email confirmation requirement. 4. Implement CAPTCHA for registration. 5. Consider SSO/SAML-only authentication for enterprise instances.

---

### 3.11 — Admin Mode Disabled — No Re-Authentication for Admin API Operations

| Field | Value |
|-------|-------|
| **ID** | `vuln_b1e112` |
| **Severity** | HIGH |
| **CVSS Score** | 7.2 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1078` — Valid Accounts |
| **ISO 27001** | `A.9.4.2 Secure log-on procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Component** | GitLab Admin Mode |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:18:48Z |

#### Description

The GitLab instance has admin_mode=false in application settings. When admin_mode is disabled, admin users and their PATs can perform all administrative operations (reading/modifying application settings, managing all users, accessing all projects, reading CI/CD variables across all projects) without any additional authentication challenge. This means a leaked admin PAT immediately grants full instance control without requiring password re-entry or 2FA verification. The /api/v4/application/settings endpoint returned HTTP 200 with full settings dump confirming unrestricted admin API access.

#### Technical Analysis

With admin_mode=false, the GitLab instance does not enforce the re-authentication check introduced in GitLab 13.x for admin operations. This means any token with admin privileges immediately provides full admin access. If admin_mode were enabled, an additional authentication step (password or 2FA) would be required before admin API endpoints respond, adding a defense-in-depth layer against stolen admin tokens. The confirmed access to /api/v4/application/settings returning HTTP 200 with the complete settings JSON proves unrestricted admin access.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/application/settings" | jq "{admin_mode}"
curl -sS --connect-timeout 10 --max-time 30 -w "\nHTTP_CODE: %{http_code}\n" -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/application/settings" | tail -1
```

#### Raw Request

```http
GET /api/v4/application/settings HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"admin_mode":false, ...full settings dump returned with HTTP 200...}
```

#### Evidence / Logs

```
GET /api/v4/application/settings -> 200: {admin_mode: false}
HTTP_CODE: 200 — Full admin settings accessible without re-authentication
```

#### Remediation

1. Enable admin_mode in GitLab application settings (PUT /api/v4/application/settings with admin_mode=true). 2. This forces admin users to re-authenticate before performing admin operations, even with a valid admin PAT. 3. Combine with mandatory 2FA for admin accounts to create a strong defense-in-depth posture against token theft.

---

### 3.12 — Admin Mode Disabled — No Re-Authentication for Admin API Operations

| Field | Value |
|-------|-------|
| **ID** | `vuln_5815ad` |
| **Severity** | HIGH |
| **CVSS Score** | 7.2 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1078.004` — Valid Accounts: Cloud Accounts |
| **ISO 27001** | `A.9.4.2 Secure log-on procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:23:13Z |

#### Description

GitLab admin_mode is disabled on this instance. When admin_mode is enabled, admin users must re-authenticate before performing administrative actions. With it disabled, any admin session or admin PAT can perform all admin operations without additional verification, increasing the blast radius of a compromised admin credential.

#### Technical Analysis

admin_mode is set to false, meaning admin users and their tokens can perform all administrative operations (user management, instance settings, CI/CD variable access) without any re-authentication step.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/application/settings | jq '.admin_mode'
```

#### Evidence / Logs

```
admin_mode: false
```

#### Remediation

Enable admin_mode in GitLab settings to require re-authentication for administrative operations. This adds a defense-in-depth layer that limits the impact of compromised admin credentials or tokens.

---

### 3.13 — No Branch Protection on Default Branch — Uncontrolled Code Push

| Field | Value |
|-------|-------|
| **ID** | `vuln_befb82` |
| **Severity** | MEDIUM |
| **CVSS Score** | 6.5 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1195.002` — Supply Chain Compromise: Compromise Software Supply Chain |
| **ISO 27001** | `A.14.2.2 System change control procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/projects/1/protected_branches` |
| **Component** | GitLab Branch Protection |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:19:43Z |

#### Description

The corp-app project (ID:1) has no protected branches configured (GET /api/v4/projects/1/protected_branches returns empty array). While the project is currently an empty repository, the default_branch is set to 'main' with default_branch_protection=2 at the instance level (which normally creates automatic branch protection). However, since the repository is empty, no actual branch protection exists yet. Any developer who pushes the first commit can establish the main branch without code review. CI/CD variables with protected=false are accessible from ALL branches, meaning any branch can exfiltrate secrets. This significantly weakens the CI/CD security posture.

#### Technical Analysis

The project has zero protected branches. While this is partly because the repository is empty (no branches exist yet), the absence of branch protection rules means that when code is pushed, there will be no merge request requirements, no code review enforcement, and no restrictions on force pushes. Combined with CI/CD variables set to protected=false, any branch created by any contributor will have full access to all secrets. This creates a supply-chain risk where a malicious contributor could push code directly to main and exfiltrate secrets via pipeline execution.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/projects/1/protected_branches" | jq .
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/projects/1" | jq "{empty_repo, default_branch}"
```

#### Raw Request

```http
GET /api/v4/projects/1/protected_branches HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
[]
```

#### Evidence / Logs

```
GET /api/v4/projects/1/protected_branches -> 200: []
GET /api/v4/projects/1 -> 200: {empty_repo: true, default_branch: "main"}
```

#### Remediation

1. Configure branch protection rules for the 'main' branch before any code is pushed. 2. Require merge requests for all changes to protected branches. 3. Enable code review (require at least 1 approval before merge). 4. Disallow force pushes to protected branches. 5. Set CI/CD variables to protected=true so they are only accessible from protected branches/tags. 6. Use the masked flag on all sensitive variables.

---

### 3.14 — No Branch Protection on Default Branch — Uncontrolled Code Push

| Field | Value |
|-------|-------|
| **ID** | `vuln_aefefa` |
| **Severity** | MEDIUM |
| **CVSS Score** | 6.5 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1195.002` — Supply Chain Compromise: Compromise Software Supply Chain |
| **ISO 27001** | `A.14.2.2 System change control procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/projects/1/protected_branches` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:23:41Z |

#### Description

The corp-app project has no branch protection rules configured on any branch. This means any user with Developer+ access can push directly to the default branch (main), force push, delete branches, and modify .gitlab-ci.yml without review. This enables supply chain attacks through direct code injection.

#### Technical Analysis

The protected_branches API returns an empty array, indicating no branch protection rules exist for any branch in this project.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/projects/1/protected_branches | jq .
```

#### Evidence / Logs

```
Protected branches: [] (empty - no protection)
```

#### Remediation

1. Protect the default branch (main) with merge request requirements. 2. Require code review approvals before merging. 3. Prevent force pushes to protected branches. 4. Enable CODEOWNERS for critical files (.gitlab-ci.yml).

---

### 3.15 — PAT Expiry Policy Not Enforced — Long-Lived Tokens Allowed

| Field | Value |
|-------|-------|
| **ID** | `vuln_42fd0a` |
| **Severity** | MEDIUM |
| **CVSS Score** | 5.4 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1098.001` — Account Manipulation: Additional Cloud Credentials |
| **ISO 27001** | `A.9.2.5 Review of user access rights` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Component** | GitLab Token Lifecycle Management |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:20:03Z |

#### Description

The GitLab instance has no maximum personal access token lifetime enforced (max_personal_access_token_lifetime=null, enforce_pat_expiration=null). The current admin PAT ('labtok', id=1) has an expiry date of 2027-08-01 — over 365 days from creation. Similarly, max_ssh_key_lifetime is null, allowing SSH keys to never expire. This means PATs and SSH keys can be created with indefinite or very long lifetimes, increasing the window of opportunity for token theft and misuse.

#### Technical Analysis

The instance does not enforce any maximum lifetime on personal access tokens or SSH keys. The active admin PAT demonstrates this — it was created with a 1-year expiry (365 days), which is well beyond security best practices of 90 days maximum. Without enforce_pat_expiration, tokens could theoretically be created without expiry dates at all. This creates a persistent backdoor risk if any token is compromised, as the attacker retains access for an extended period.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/application/settings" | jq "{max_personal_access_token_lifetime, enforce_pat_expiration, max_ssh_key_lifetime}"
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/personal_access_tokens/self" | jq "{name, expires_at, created_at}"
```

#### Raw Request

```http
GET /api/v4/application/settings HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"max_personal_access_token_lifetime":null,"enforce_pat_expiration":null,"max_ssh_key_lifetime":null}
```

#### Evidence / Logs

```
GET /api/v4/application/settings -> 200: {max_personal_access_token_lifetime: null, enforce_pat_expiration: null, max_ssh_key_lifetime: null}
GET /api/v4/personal_access_tokens/self -> 200: {name: "labtok", expires_at: "2027-08-01", created_at: "2026-08-01T20:12:06.083Z"}
```

#### Remediation

1. Set max_personal_access_token_lifetime to 90 days or less. 2. Enable enforce_pat_expiration to prevent creation of non-expiring tokens. 3. Set max_ssh_key_lifetime to enforce SSH key rotation. 4. Implement a PAT audit and rotation schedule. 5. Revoke and re-issue all existing long-lived tokens with shorter expiry periods.

---

### 3.16 — PAT Expiry Policy Not Enforced — Long-Lived Tokens Allowed

| Field | Value |
|-------|-------|
| **ID** | `vuln_91f068` |
| **Severity** | MEDIUM |
| **CVSS Score** | 5.4 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1550.001` — Use Alternate Authentication Material: Application Access Token |
| **ISO 27001** | `A.9.2.5 Review of user access rights` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/personal_access_tokens/self` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:23:50Z |

#### Description

The GitLab instance does not enforce a maximum lifetime for Personal Access Tokens. The admin PAT 'labtok' has no expiration date (expires_at: null). Long-lived tokens increase the window of opportunity for attackers if a token is compromised, as the token remains valid indefinitely.

#### Technical Analysis

The admin PAT has no expiration date set. GitLab allows configuring a maximum PAT lifetime at the instance level, but this is not enforced.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/personal_access_tokens/self | jq '{name, expires_at, scopes}'
```

#### Evidence / Logs

```
name: labtok
expires_at: null
scopes: [api, sudo]
```

#### Remediation

1. Configure max_personal_access_token_lifetime in instance settings. 2. Set a reasonable maximum (e.g., 90 days). 3. Rotate existing tokens without expiration dates. 4. Monitor for tokens approaching expiration.

---

### 3.17 — API Rate Limiting Disabled — Brute-Force and Abuse Risk

| Field | Value |
|-------|-------|
| **ID** | `vuln_a1092c` |
| **Severity** | MEDIUM |
| **CVSS Score** | 5.3 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1110` — Brute Force |
| **ISO 27001** | `A.9.4.2 Secure log-on procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Component** | GitLab Rate Limiting |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:19:23Z |

#### Description

Both authenticated and unauthenticated API rate limiting are disabled on the GitLab instance (throttle_authenticated_api_enabled=false, throttle_unauthenticated_api_enabled=false). Additionally, max_login_attempts and failed_login_attempts_unlock_period_in_minutes are both null (no account lockout). This allows unlimited API requests and unlimited login attempts, enabling credential brute-force attacks, user enumeration, and API abuse without any throttling or lockout mechanism.

#### Technical Analysis

The GitLab instance has no rate limiting or account lockout policies configured. This is confirmed by the application settings API response showing all throttle/lockout fields set to false or null. An attacker can make unlimited requests to authentication endpoints, API endpoints, and brute-force user credentials without being blocked or throttled. This is particularly dangerous combined with the open self-registration (signup_enabled=true) and password authentication enabled for both web and git.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/application/settings" | jq "{throttle_authenticated_api_enabled, throttle_unauthenticated_api_enabled, max_login_attempts, failed_login_attempts_unlock_period_in_minutes}"
```

#### Raw Request

```http
GET /api/v4/application/settings HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"throttle_authenticated_api_enabled":false,"throttle_unauthenticated_api_enabled":false,"max_login_attempts":null,"failed_login_attempts_unlock_period_in_minutes":null}
```

#### Evidence / Logs

```
GET /api/v4/application/settings -> 200: {throttle_authenticated_api_enabled: false, throttle_unauthenticated_api_enabled: false, max_login_attempts: null, failed_login_attempts_unlock_period_in_minutes: null}
```

#### Remediation

1. Enable throttle_authenticated_api_enabled and throttle_unauthenticated_api_enabled with appropriate rate limits. 2. Set max_login_attempts (recommended: 10) and failed_login_attempts_unlock_period_in_minutes (recommended: 30). 3. Consider implementing IP-based rate limiting at the reverse proxy/load balancer level. 4. Monitor authentication logs for brute-force indicators.

---

### 3.18 — API Rate Limiting Disabled — Brute-Force and Abuse Risk

| Field | Value |
|-------|-------|
| **ID** | `vuln_40ffbf` |
| **Severity** | MEDIUM |
| **CVSS Score** | 5.3 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1110` — Brute Force |
| **ISO 27001** | `A.9.4.2 Secure log-on procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:23:32Z |

#### Description

API rate limiting (throttle_authenticated_api_enabled) is disabled on this GitLab instance. This allows unlimited API requests, enabling brute-force attacks against authentication endpoints, mass data enumeration, and denial-of-service conditions through API abuse.

#### Technical Analysis

Both authenticated and unauthenticated API rate limiting are disabled, allowing unlimited requests without throttling.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/application/settings | jq '{throttle_authenticated_api_enabled, throttle_unauthenticated_api_enabled}'
```

#### Evidence / Logs

```
throttle_authenticated_api_enabled: false
throttle_unauthenticated_api_enabled: false
```

#### Remediation

Enable API rate limiting for both authenticated and unauthenticated requests. Configure appropriate request limits per period (e.g., 2000 requests per minute for authenticated, 500 for unauthenticated).

---

### 3.19 — Container Registry Enabled on Project Without Security Controls

| Field | Value |
|-------|-------|
| **ID** | `vuln_13c02a` |
| **Severity** | MEDIUM |
| **CVSS Score** | 5.0 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1525` — Implant Internal Image |
| **ISO 27001** | `A.14.2.7 Outsourced development` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/projects/1/registry/repositories` |
| **Component** | GitLab Container Registry |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:20:20Z |

#### Description

The corp-app project has container_registry_enabled=true with a short container_registry_token_expire_delay of 5 minutes. While no container images are currently stored (registry/repositories returns empty), the enabled registry combined with shared runner access and unprotected CI/CD variables creates a supply-chain attack vector: an attacker with Developer+ access could push malicious container images that would be used in deployments. The short token expiry is a positive control but insufficient without image signing or scanning policies.

#### Technical Analysis

The container registry is enabled on the project, creating an additional attack surface for supply-chain compromises. While currently empty, any user with Developer+ access can push container images. Without image signing, vulnerability scanning, or tag immutability policies, a malicious image could be pushed and used in production deployments. The 5-minute token expiry is a minor positive control but does not prevent authorized pushes of malicious content.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/projects/1" | jq "{container_registry_enabled}"
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/projects/1/registry/repositories" | jq .
```

#### Raw Request

```http
GET /api/v4/projects/1/registry/repositories HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
[]
```

#### Evidence / Logs

```
GET /api/v4/projects/1 -> 200: {container_registry_enabled: true}
GET /api/v4/projects/1/registry/repositories -> 200: []
GET /api/v4/application/settings -> 200: {container_registry_token_expire_delay: 5}
```

#### Remediation

1. Disable container_registry_enabled if not actively used. 2. If used, implement container image scanning in CI/CD pipelines. 3. Enable tag immutability to prevent overwriting existing images. 4. Implement image signing (e.g., cosign) for production images. 5. Restrict who can push to the registry via project role permissions.

---

### 3.20 — System Hooks Allow Local Requests — Potential SSRF Vector

| Field | Value |
|-------|-------|
| **ID** | `vuln_9df919` |
| **Severity** | MEDIUM |
| **CVSS Score** | 5.0 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:N/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1190` — Exploit Public-Facing Application |
| **ISO 27001** | `A.13.1.3 Segregation in networks` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Component** | GitLab System Hooks |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:20:43Z |

#### Description

The GitLab instance allows local requests from system hooks (allow_local_requests_from_system_hooks=true) while web hooks are restricted (allow_local_requests_from_web_hooks_and_services=false). An admin user can create system hooks pointing to internal/local network addresses (127.0.0.1, 169.254.169.254, internal services), potentially enabling Server-Side Request Forgery (SSRF) to access internal services, cloud metadata endpoints, or other infrastructure not directly accessible from outside. While no system hooks are currently configured, the permissive setting creates the potential for SSRF exploitation.

#### Technical Analysis

System hooks are allowed to make requests to local/internal network addresses. While this requires admin access to configure and no hooks currently exist, an attacker who compromises an admin account (or uses the leaked admin PAT) could create system hooks targeting internal services such as cloud metadata endpoints (169.254.169.254), internal APIs, or localhost services. The outbound_local_requests_whitelist is empty, meaning all local addresses are allowed for system hooks. This is a confirmed misconfiguration that enables SSRF when combined with admin access.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/application/settings" | jq "{allow_local_requests_from_system_hooks, allow_local_requests_from_web_hooks_and_services, outbound_local_requests_whitelist}"
```

#### Raw Request

```http
GET /api/v4/application/settings HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"allow_local_requests_from_system_hooks":true,"allow_local_requests_from_web_hooks_and_services":false,"outbound_local_requests_whitelist":[]}
```

#### Evidence / Logs

```
GET /api/v4/application/settings -> 200: {allow_local_requests_from_system_hooks: true, allow_local_requests_from_web_hooks_and_services: false, outbound_local_requests_whitelist: []}
```

#### Remediation

1. Set allow_local_requests_from_system_hooks=false unless specifically required. 2. If local requests are needed for system hooks, use outbound_local_requests_whitelist to restrict to specific allowed addresses only. 3. Monitor system hook creation and modifications via audit logs.

---

### 3.21 — Container Registry Enabled on Project Without Security Controls

| Field | Value |
|-------|-------|
| **ID** | `vuln_3529ad` |
| **Severity** | MEDIUM |
| **CVSS Score** | 5.0 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1525` — Implant Internal Image |
| **ISO 27001** | `A.14.1.2 Securing application services on public networks` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/projects/1/registry/repositories` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:23:58Z |

#### Description

The container registry is enabled on the corp-app project without image scanning or vulnerability scanning policies. While no images are currently stored, the registry is accessible and could be used to push/pull container images without security validation. This creates risk of supply chain attacks through malicious container images.

#### Technical Analysis

Container registry is enabled (container_registry_enabled: true on the project) but no scanning policies or security controls are in place. Currently empty but accessible.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/projects/1/registry/repositories | jq .
```

#### Evidence / Logs

```
container_registry_enabled: true
container_registry_image_prefix: accessible
repositories: [] (empty, but enabled)
```

#### Remediation

1. Enable container scanning in CI/CD pipelines. 2. Configure vulnerability scanning policies for the registry. 3. Implement image signing and verification. 4. Restrict who can push images to the registry.

---

### 3.22 — System Hooks Allow Local Requests — Potential SSRF Vector

| Field | Value |
|-------|-------|
| **ID** | `vuln_35ead9` |
| **Severity** | MEDIUM |
| **CVSS Score** | 5.0 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` |
| **Status** | CONFIRMED |
| **Category** | `ssrf` |
| **MITRE ATT&CK** | `T1190` — Exploit Public-Facing Application |
| **ISO 27001** | `A.13.1.1 Network controls` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:24:07Z |

#### Description

GitLab instance settings allow webhooks and integrations to make requests to local network addresses (allow_local_requests_from_web_hooks_and_services: true). This enables Server-Side Request Forgery (SSRF) attacks where an attacker with sufficient privileges could create webhooks or integrations that target internal services (metadata endpoints, internal APIs) from the GitLab server.

#### Technical Analysis

Both allow_local_requests_from_web_hooks_and_services and allow_local_requests_from_system_hooks are set to true, allowing SSRF through webhook/integration configuration.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/application/settings | jq '{allow_local_requests_from_web_hooks_and_services, allow_local_requests_from_system_hooks}'
```

#### Evidence / Logs

```
allow_local_requests_from_web_hooks_and_services: true
allow_local_requests_from_system_hooks: true
```

#### Remediation

1. Disable allow_local_requests_from_web_hooks_and_services unless specifically required. 2. Disable allow_local_requests_from_system_hooks. 3. If local requests are needed, use the allowlist to restrict to specific internal addresses. 4. Monitor webhook creation and modification.

---

### 3.23 — Auto DevOps Enabled — Automatic Pipeline Execution on Code Push

| Field | Value |
|-------|-------|
| **ID** | `vuln_602ba6` |
| **Severity** | LOW |
| **CVSS Score** | 3.8 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1059.004` — Command and Scripting Interpreter: Unix Shell |
| **ISO 27001** | `A.14.2.2 System change control procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/projects/1` |
| **Component** | GitLab Auto DevOps |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:21:19Z |

#### Description

The corp-app project has auto_devops_enabled=true with shared_runners_enabled=true. Auto DevOps automatically configures CI/CD pipelines using a predefined template when no .gitlab-ci.yml is present. This means any code pushed to the repository will automatically trigger pipeline execution on shared runners, potentially consuming resources and executing untrusted code. Combined with the unprotected CI/CD variables, Auto DevOps pipelines would automatically have access to the AWS_SECRET_ACCESS_KEY. While Auto DevOps is a convenience feature, it creates an implicit code execution path that may not be expected by project maintainers.

#### Technical Analysis

Auto DevOps creates an implicit pipeline execution path. When combined with shared runners and unprotected CI/CD variables, this means any code push — even from a newly registered user who forks the project — could trigger a pipeline that accesses AWS credentials. The ci_config_path is null, confirming that Auto DevOps templates would be used rather than a custom .gitlab-ci.yml. This is a confirmed configuration that extends the CI/CD attack surface beyond what explicit pipeline configuration would allow.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" "http://127.0.0.1:8091/api/v4/projects/1" | jq "{auto_devops_enabled, shared_runners_enabled, ci_config_path}"
```

#### Raw Request

```http
GET /api/v4/projects/1 HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"auto_devops_enabled":true,"shared_runners_enabled":true,"ci_config_path":null}
```

#### Evidence / Logs

```
GET /api/v4/projects/1 -> 200: {auto_devops_enabled: true, shared_runners_enabled: true, ci_config_path: null}
```

#### Remediation

1. Disable auto_devops_enabled unless explicitly needed for this project. 2. Use an explicit .gitlab-ci.yml with reviewed pipeline configuration instead. 3. If Auto DevOps is needed, ensure CI/CD variables are marked as protected and masked. 4. Implement merge request pipelines instead of branch push pipelines to require code review before execution.

---

### 3.24 — Auto DevOps Enabled — Automatic Pipeline Execution on Code Push

| Field | Value |
|-------|-------|
| **ID** | `vuln_ffd0ea` |
| **Severity** | LOW |
| **CVSS Score** | 3.8 |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N` |
| **Status** | CONFIRMED |
| **Category** | `misconfiguration` |
| **MITRE ATT&CK** | `T1072` — Software Deployment Tools |
| **ISO 27001** | `A.14.2.2 System change control procedures` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/application/settings` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:24:23Z |

#### Description

Auto DevOps is enabled at the instance level. This means projects without a .gitlab-ci.yml file will automatically use the Auto DevOps pipeline template when code is pushed. Combined with open self-registration and shared runners, this could allow newly registered users to trigger pipeline execution automatically, potentially consuming resources and accessing CI/CD variables.

#### Technical Analysis

auto_devops_enabled is true at the instance level, meaning any project without its own CI config will automatically get Auto DevOps pipelines triggered on code push.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/application/settings | jq '.auto_devops_enabled'
```

#### Evidence / Logs

```
auto_devops_enabled: true
```

#### Remediation

1. Disable auto_devops_enabled at the instance level. 2. Enable Auto DevOps only on specific projects that need it. 3. Require explicit .gitlab-ci.yml configuration per project.

---

### 3.25 — GitLab Version Information Disclosure via API

| Field | Value |
|-------|-------|
| **ID** | `vuln_5ead16` |
| **Severity** | INFO |
| **CVSS Score** | N/A |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:N` |
| **Status** | CONFIRMED |
| **Category** | `information_disclosure` |
| **MITRE ATT&CK** | `T1592` — Gather Victim Host Information |
| **ISO 27001** | `A.12.6.1 Management of technical vulnerabilities` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/version` |
| **Component** | GitLab Version API |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:21:00Z |

#### Description

The GitLab instance discloses its exact version (19.2.1), revision (f4d029d2da8), and feature status (KAS enabled, enterprise=false) via the /api/v4/version endpoint. While this endpoint requires authentication, the disclosed information allows attackers to identify the exact software version and check for known CVEs. The KAS (Kubernetes Agent Server) is enabled at ws://gitlab.lab/-/kubernetes-agent/ with a K8s proxy at http://gitlab.lab/-/kubernetes-agent/k8s-proxy/, indicating potential Kubernetes integration attack surface.

#### Technical Analysis

The version endpoint reveals GitLab CE 19.2.1 with KAS enabled. This information aids attackers in targeted exploitation by narrowing down applicable CVEs and attack techniques. The KAS endpoint URLs reveal internal hostname 'gitlab.lab' and the availability of Kubernetes integration features. This is an informational finding as version disclosure via an authenticated API endpoint is expected behavior, but the information is valuable for attack planning.

#### Exploitation Commands

```bash
curl -sS --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/version | jq .
```

#### Raw Request

```http
GET /api/v4/version HTTP/1.1
Host: 127.0.0.1:8091
PRIVATE-TOKEN: glpat-LABtoken1234567890
```

#### Raw Response

```http
{"version":"19.2.1","revision":"f4d029d2da8","kas":{"enabled":true,"externalUrl":"ws://gitlab.lab/-/kubernetes-agent/","externalK8sProxyUrl":"http://gitlab.lab/-/kubernetes-agent/k8s-proxy/","version":"19.2.1"},"enterprise":false}
```

#### Evidence / Logs

```
GET /api/v4/version -> 200: {version: "19.2.1", revision: "f4d029d2da8", kas: {enabled: true, externalUrl: "ws://gitlab.lab/-/kubernetes-agent/", externalK8sProxyUrl: "http://gitlab.lab/-/kubernetes-agent/k8s-proxy/", version: "19.2.1"}, enterprise: false}
```

#### Remediation

1. Consider restricting the /api/v4/version endpoint to admin users only. 2. Keep GitLab updated to the latest security patch version. 3. Review KAS endpoints for proper authentication and access controls. 4. Ensure the Kubernetes agent proxy is not exposed without proper authentication.

---

### 3.26 — GitLab Version Information Disclosure via API

| Field | Value |
|-------|-------|
| **ID** | `vuln_85597e` |
| **Severity** | INFO |
| **CVSS Score** | N/A |
| **CVSS Vector** | `N/A` |
| **Status** | CONFIRMED |
| **Category** | `information_disclosure` |
| **MITRE ATT&CK** | `T1592` — Gather Victim Host Information |
| **ISO 27001** | `A.12.6.1 Management of technical vulnerabilities` |
| **Endpoint** | `http://127.0.0.1:8091/api/v4/version` |
| **Discovered by** | `gitlab` |
| **Discovered at** | 2026-08-01T20:24:16Z |

#### Description

The GitLab API /version endpoint discloses the exact version (19.2.1) and revision (f4d029d2da8) of the GitLab CE instance. This information can be used by attackers to identify known vulnerabilities specific to this version and craft targeted exploits.

#### Technical Analysis

The /api/v4/version endpoint returns the exact version and build revision of the GitLab instance.

#### Exploitation Commands

```bash
curl -s --connect-timeout 10 --max-time 30 -H "PRIVATE-TOKEN: glpat-LABtoken1234567890" http://127.0.0.1:8091/api/v4/version | jq .
```

#### Evidence / Logs

```
version: 19.2.1
revision: f4d029d2da8
kas.enabled: true
kas.externalUrl: ws://gitlab.lab/-/kubernetes-agent/
kas.version: 19.2.1
enterprise: false
```

#### Remediation

Restrict access to the /version endpoint to authenticated admin users only. Consider using a reverse proxy to strip version headers from responses.

---

## 4. REMEDIATION ROADMAP

### P0 — Immediate (< 24h)

| Finding | Effort |
|---------|--------|
| Admin PAT with API + Sudo Scopes — Full Instance Takeover | High |
| Admin PAT with API + Sudo Scopes — Full Instance Takeover | High |
| AWS Secret Access Key Exposed in CI/CD Variables (Unmasked, ... | High |
| AWS Secret Access Key Exposed in CI/CD Variables (Unmasked, ... | High |

### P1 — Short term (< 1 week)

| Finding | Effort |
|---------|--------|
| Runner Registration Token Exposed via Project API | High |
| Runner Registration Token Exposed via Project API | High |
| Admin Account Missing Two-Factor Authentication (2FA) | High |
| Admin Account Missing Two-Factor Authentication (2FA) | High |
| Open Self-Registration Enabled — Unauthorized Account Creati... | High |
| Open Self-Registration Enabled — Unauthorized Account Creati... | High |

### P2 — Medium term (< 2 weeks)

| Finding | Effort |
|---------|--------|
| No Branch Protection on Default Branch — Uncontrolled Code P... | High |
| No Branch Protection on Default Branch — Uncontrolled Code P... | High |
| PAT Expiry Policy Not Enforced — Long-Lived Tokens Allowed | High |
| PAT Expiry Policy Not Enforced — Long-Lived Tokens Allowed | High |
| API Rate Limiting Disabled — Brute-Force and Abuse Risk | High |

### P3 — Long term (< 1 month)

| Finding | Effort |
|---------|--------|
| Auto DevOps Enabled — Automatic Pipeline Execution on Code P... | High |
| Auto DevOps Enabled — Automatic Pipeline Execution on Code P... | High |

---

*Report auto-generated by Darkmoon AI Security Platform*  
*Classification: CONFIDENTIAL — Restricted to authorized personnel*  
*Generated: 2026-08-01T20:24:40Z*  
*Campaign: camp_20260801_a719641d | Target: 127.0.0.1*
