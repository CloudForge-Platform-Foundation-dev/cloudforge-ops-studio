
# CloudForge Ops Studio

**Governed Auto-Healer for CloudForge Platform Foundation**

CloudForge Ops Studio is the operations and remediation Studio in the CloudForge ecosystem. It is designed to help operators investigate operational events, retrieve relevant knowledge, recommend controlled repairs, and maintain an auditable record of operational decisions.

> **Status: Initial scaffold / early development.** The repository contains the initial FastAPI service skeleton, event-analysis and audit abstractions, LLM provider interfaces, configuration, and Foundation validation workflow. The end-to-end remediation flow, repair-template validation, approval enforcement, production connectors, and automated repair execution are not yet complete. This scaffold is not ready for production remediation.

## 1. Objectives

- Receive and correlate operational events from approved CloudForge services and infrastructure integrations.
- Analyze incidents and retrieve relevant operational knowledge.
- Generate recommendations based on approved repair templates rather than arbitrary commands.
- Require explicit authorization and human approval before executing repairs.
- Record decisions and outcomes for traceability and incident review.
- Integrate with CloudForge Foundation identity, security, and governance standards.

## 2. Design Principles

### Foundation as the Source of Truth

Ops Studio consumes shared contracts, policies, identity standards, and validation gates maintained by CloudForge Platform Foundation. It must not redefine or bypass Foundation requirements.

### Human-in-the-Loop Remediation

The initial milestone focuses on analysis, recommendations, and auditability. Any future repair execution capability must be explicitly approved and protected by authorization and governance controls.

### No Direct LLM Control of Production

LLM output is untrusted input. It must never be treated as an executable command, an authorization decision, or permission to modify production resources.

### Fail-Closed Governance

Missing identity validation, policy decisions, template validation, approval, or required evidence must block a repair. Errors and incomplete validation must never be treated as successful authorization.

### Least Privilege and Bounded Actions

Connectors must expose only the operations they require. Repair operations must use bounded timeouts, retry limits, idempotency controls, and verified rollback procedures where applicable.

### Auditable Operations

Events, analysis results, approval decisions, template validation, execution attempts, and outcomes should be traceable through a correlation ID.

### Provider-Independent AI

Model access should remain behind a provider abstraction, with a mock provider available for deterministic development and testing.

## 3. Intended Architecture

```text
Operational Event
       |
       v
Event Validation and Correlation ID
       |
       v
Identity, Authorization and Governance
       |
       v
Incident Analysis <----> Knowledge Retrieval
       |
       v
Recommendation and Approved Repair Template
       |
       v
Template, Parameter, Scope and Risk Validation
       |
       v
Explicit Human Approval
       |
       v
Controlled Repair Execution
       |
       v
Outcome Verification / Rollback
       |
       v
Audit Record
```

The diagram describes the intended architecture, not a claim that every stage is implemented in the current repository.

## 4. Security and Governance Requirements

Before repair execution is enabled, the implementation must enforce the following controls:

- **Identity:** Integrate with the Foundation identity contract and `cloudforge-auth-core`. Do not introduce a competing authentication scheme.
- **Governance:** Run the Foundation Governance Gate in CI. Missing validators, errors, and incomplete evidence must not result in a pass.
- **Repair templates:** Define a versioned schema, strict action allowlists, validated parameters, and explicit resource and environment scopes.
- **Approval:** Require an authenticated approver and record who approved the action, when, and for which correlation ID.
- **Command safety:** Reject arbitrary shell commands and unrestricted model-generated tool calls.
- **Execution controls:** Apply least-privilege credentials, timeouts, bounded attempts, idempotency protections, and verified rollback procedures.
- **Audit protection:** Keep secrets and sensitive payloads out of logs. Define access controls and retention requirements for audit records.
- **Testing:** Cover unauthorized actions, malformed templates, policy denials, timeouts, duplicate requests, failed repairs, and rollback scenarios.

## 5. Current Implementation Status

| Component | Status |
|---|---|
| FastAPI application skeleton | Present |
| Health, readiness and liveness endpoints | Present as basic handlers |
| Event and analysis data models | Initial scaffold |
| Audit-record abstraction | In-memory scaffold; not durable or immutable storage |
| LLM provider abstraction | Incomplete scaffold |
| Mock LLM provider | Incomplete scaffold |
| Foundation reusable validation workflow | Configured to reference `reusable-gate.yml@v1.0.2` |
| Repair-template schema and allowlist validation | Not implemented |
| Approval enforcement | Not implemented |
| Automated repair execution | Not implemented |
| Production service connectors | Not implemented |
| End-to-end remediation tests | Not implemented |

This table must be updated as implementation and test evidence changes.

## 6. API Skeleton

The current FastAPI entry point defines the following endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Returns basic service information |
| GET | `/health` | Returns a basic health response |
| GET | `/ready` | Returns a basic readiness response |
| GET | `/live` | Returns a basic liveness response |

These are starter endpoints. They do not prove that downstream dependencies, identity validation, or remediation workflows are healthy.

## 7. Technology Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- HTTPX and aiohttp for future service connectors
- `cloudforge-auth_core==1.1.8`, as declared in project dependencies
- pytest, pytest-asyncio and pytest-cov
- Black and Ruff
- CloudForge Foundation reusable validation workflow

## 8. Local Development

### Prerequisites

- Python 3.11 or later
- Git

### Clone the Repository

```bash
git clone https://github.com/CloudForge-Platform-Foundation-dev/cloudforge-ops-studio.git
cd cloudforge-ops-studio
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Development warning:** The current scaffold contains incomplete provider code and should not be considered runnable or test-clean until the implementation gaps are resolved. The CI workflow is configured to run `pytest tests/ -v --tb=short`, but configuration alone is not evidence that the checks pass.

Once the application and its imports are complete, the intended local entry point is:

```bash
uvicorn src.ops_studio.api.main:app --host 127.0.0.1 --port 8000
```

## 9. Configuration and Secrets

The current settings scaffold defines configuration for:

- Application name and version
- LLM provider selection
- Internal service URLs
- Identity issuer and audience
- JWKS cache TTL
- Governance-gate enablement
- Human-approval requirements
- Repair-attempt limits
- Repair timeouts

The environment-variable mapping and startup validation still need to be implemented and documented.

Use an approved secret store or local environment variables for credentials. Never commit access tokens, private keys, or production secrets. The current `.env.example` file is empty and must be completed before the project can provide a reliable deployment setup guide.

## 10. Roadmap

### Phase 1 — Safe Recommendations and Audit

- Complete event validation and correlation.
- Integrate authenticated access to approved Foundation services.
- Implement knowledge retrieval and deterministic mock-provider tests.
- Define recommendation and repair-template contracts.
- Implement durable, access-controlled audit storage.
- Complete unit, security, and integration tests.

### Phase 2 — Approved and Constrained Remediation

- Implement template schema validation and strict action allowlists.
- Add authenticated human approval and policy enforcement.
- Implement narrowly scoped repair connectors and execution controls.
- Add timeout, idempotency, outcome-verification, and rollback tests.
- Enable repair actions only after the Foundation gate and security review pass.

### Phase 3 — Operational Maturity

- Add monitoring, alerting, operational runbooks, and release evidence.
- Establish template versioning, compatibility, and deprecation policies.
- Measure remediation success, false positives, rollback rates, and operator overrides.

## 11. Foundation Alignment

Ops Studio is a Studio within the [CloudForge Platform Foundation](https://github.com/CloudForge-Platform-Foundation-dev).

Foundation owns shared governance, identity, policies, contracts, and validation standards. Ops Studio owns its operational analysis, recommendation logic, repair-template integration, and Studio-specific implementation.

The CI workflow references the Foundation reusable gate at `v1.0.2`. Keep this reference aligned with the approved Foundation release process and document changes through reviewed commits and release notes.

## 12. Contributing

1. Open an issue or pull request describing the change and its operational and security impact.
2. Update relevant contracts, tests, and documentation alongside the implementation.
3. Test both allowed and denied paths. Never treat skipped or incomplete validation as a pass.
4. Ensure the Foundation gate and test workflow pass before merging.
5. Do not enable production repair actions without explicit security review and evidence that approval controls work correctly.

## 13. License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
