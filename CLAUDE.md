# MARKETING - Joomla Extension Project

## Project Configuration

- **Project Name**: MARKETING
- **Extension Type**: Component
- **Vendor Namespace**: NextPro
- **PHP Version**: 8.3+ (typed properties, constructor promotion, readonly, enums)
- **Joomla Version**: 5.2+ (Joomla Framework 2.0+)
- **Project Status**: Active

## Database

- **Connection Name**: marketing_dev
- **Database Type**: MariaDB 10.5+ / MySQL 8.0+
- **Table Prefix**: `#__`

## Service Layer Architecture

This extension follows the **Service Layer Pattern** to separate business logic from controllers:

- **Administrator\Service\** — Canonical implementations of all business logic
- **Services registered** in `services/provider.php` via Dependency Injection (DI)
- **Controllers delegate** to services (business logic never duplicated across Site/API/CLI)
- **All layers reuse** Administrator services unchanged
- **Data access** through Repository interfaces (never raw database queries in business logic)

**Benefits**:
- Single source of truth for business logic
- Easy to test (inject mock repositories)
- Easy to reuse across contexts (Admin UI, Site UI, REST API, CLI)
- Loose coupling between components

## Namespace Conventions

All extensions in this project use the vendor namespace `NextPro`:

- **Components**: `NextPro\Component\{ComponentName}\`
  - `NextPro\Component\{ComponentName}\Administrator\` — Backend/admin code
  - `NextPro\Component\{ComponentName}\Site\` — Frontend/public code
  - `NextPro\Component\{ComponentName}\Api\` — REST API endpoints
  - `NextPro\Component\{ComponentName}\Cli\` — CLI console commands

- **Modules**: `NextPro\Module\{ModuleName}\`
- **Plugins**: `NextPro\Plugin\{PluginGroup}\{PluginName}\`

## Coding Standards

@includes/joomla-coding-preferences.md

## Development Environment

@includes/joomla-devel-environment.md

## Extension Structure References

### Component
@includes/joomla-structure-component.md

### API
@includes/joomla-structure-api.md

### Plugin
@includes/joomla-structure-plugin.md

### Module
@includes/joomla-structure-module.md

### CLI
@includes/joomla-structure-cli.md

## Architecture References

@includes/joomla-di-patterns.md

@includes/joomla-events-system.md

## Deprecated Patterns (AVOID)

@includes/joomla-depreciated.md

## Chunked Import Pattern

@includes/joomla-chunked-import-pattern.md

## Context7 Libraries

@includes/context7.json

Additional libraries:
- **PHPUnit** — Testing framework (`/sebastianbergmann/phpunit`)
- **Symfony Console** — CLI command framework (`/symfony/console`)

## Agent Orchestration

### Standard Development Workflow

1. **Requirements** (optional) → `joomla-prd-writer`
2. **Architecture** → `joomla-architect` — **always run this before building**
3. **Implementation** (choose builders based on extension type):
   - **Component Admin**: `joomla-admin-builder`
   - **Component Site**: `joomla-site-builder`
   - **REST API**: `joomla-api-builder`
   - **CLI Commands**: `joomla-cli-builder`
   - **Modules**: `joomla-module-builder`
   - **Plugins**: `joomla-plugin-builder`
4. **Language/i18n** → `joomla-language-manager`
5. **Quality Assurance** (parallel):
   - **Code Review**: `joomla-code-reviewer`
   - **Security**: `joomla-security-auditor`
   - **Performance**: `joomla-performance-agent`
6. **Testing** → `joomla-test-engineer`
7. **Debugging** (on-demand) → `joomla-debugger`

**Use `joomla-orchestrator`** for building a complete extension from scratch and letting agents coordinate automatically. **Use direct agents** when you already know exactly which layer you're working on.

### Available Agents

@includes/available-agents.md

## Skills (Shared)

@includes/available-skills.md

## Quick Start Checklist

- [ ] Set up a local Joomla 5.2+ instance and point it at this repository's extension source
- [ ] Configure database connection `marketing_dev`
- [ ] Review `.claude/includes/joomla-coding-preferences.md` for code standards
- [ ] Review `.claude/includes/joomla-di-patterns.md` for DI patterns
- [ ] Invoke `joomla-architect` to design the extension
- [ ] Invoke appropriate builder agent(s) for implementation
- [ ] Run `vendor/bin/phpunit` to execute tests
- [ ] Invoke `joomla-code-reviewer` for a quality check

## Documentation References

**Official Documentation**:
- [Joomla 5.x Docs](https://docs.joomla.org/)
- [Joomla Framework](https://framework.joomla.org/)
- [Web Services API](https://docs.joomla.org/Selecting_a_webservice_version)
- [Symfony Console](https://symfony.com/doc/current/components/console.html)
- [PHPUnit Documentation](https://phpunit.de/documentation.html)

---

**Project Created**: 2026-08-05
**Maintained By**: Aline
**Status**: Active
