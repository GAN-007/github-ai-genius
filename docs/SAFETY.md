# Safety and Legal Boundaries

GitHub AI Genius is designed for authorized engineering work, original software generation, defensive review, and license-aware repository analysis.

## Allowed uses

- Analyze repositories you own or are allowed to inspect.
- Generate original software from a written product brief.
- Refactor and improve authorized codebases.
- Review code for reliability, maintainability, and defensive security.
- Create clean-room rebuild plans when direct reuse is not legally safe.

## Disallowed uses

- Copying proprietary code without permission.
- Removing license notices or attribution requirements.
- Recreating protected brands, private assets, or proprietary UI verbatim.
- Building harmful automation or unauthorized access workflows.

## License handling

Permissive licenses may allow reuse with conditions. Copyleft, custom, missing, or proprietary licenses require review. When in doubt, the platform must generate original code rather than copying source text.

## Credential handling

Credentials belong in the user's local environment. Generated projects should read secrets from environment variables or a secret manager, never from committed source files.
