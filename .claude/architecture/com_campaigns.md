# Architecture: com_campaigns — Campaign & Lead Management

**Vendor**: NextPro
**Extension type**: Component
**Joomla target**: 5.2+ / PHP 8.3+
**Architect**: joomla-architect (persona adopted per `.claude/agents/joomla/joomla-architect.md`)
**Status**: Proposed

---

## 0. Context & Research

### 0.1 Scope decision

No PRD was supplied. Per the task brief, I selected a **Campaign & Lead Management** component (`com_campaigns`): marketing staff create **Campaigns** (email, social, PPC, events, etc.), the site (and external tools) capture **Leads**, and every lead is attributed back to the campaign(s) that produced it — both a curated manual association and an automatic multi-touch tracking log. This is the most common "marketing component" shape for a Joomla site (landing pages + lead capture + attribution reporting) and exercises all five Joomla table classifications, which makes it a good architectural showcase.

### 0.2 Research performed

- Read `includes/joomla-coding-preferences.md` — case convention, DataModel pattern, Table-only-writes rule, deprecated-toolbar rule, manifest naming.
- Read `includes/joomla-di-patterns.md` — service provider shape, DataModel+Service registration pattern, `bootComponent()` bridge.
- Read `includes/joomla-events-system.md` — `SubscriberInterface`, typed event classes, naming conventions.
- Read `includes/joomla-depreciated.md` — cross-checked every proposed pattern against this list (see §8, no violations found).
- Read `includes/joomla-structure-component.md` — directory layout, view conventions, hierarchical-list rules (not applicable — no hierarchical table here).
- Read `CLAUDE.md` — confirmed vendor namespace `NextPro`, four-context layering (Administrator/Site/Api/Cli), PHP 8.3+ mandate, `marketing_dev` DB connection.

No existing extension code exists in this repository (fresh project), so no legacy-pattern discovery was needed.

### 0.3 Case-convention note (applies throughout this document)

Per `joomla-coding-preferences.md`, every name-resolved class's entity segment must collapse to a single capitalised word. All entities chosen for this component are already single English words (**Campaign**, **Lead**), or were deliberately collapsed during naming (**Leadsource**, **Leadactivity**, **Leadcampaignmap**, **Attribution**) so no further contraction is needed downstream. The one deliberate **exception** is custom `*Event` classes (§5) — see the note under §5.1 for why these follow core Joomla's own multi-word `Event` naming (`AfterSaveEvent`, `ItemProcessedEvent`) rather than the entity-collapse rule, since Event classes are never resolved via `ucfirst(strtolower())`.

---

## 1. Namespace Map

```
NextPro\Component\Campaigns\Administrator\
├── Controller\
│   ├── CampaignController.php          — FormController (single campaign)
│   ├── CampaignsController.php         — AdminController (campaign list actions)
│   ├── LeadController.php              — FormController (single lead)
│   ├── LeadsController.php             — AdminController (lead list actions: assign, convert, export)
│   ├── LeadsourceController.php        — FormController
│   ├── LeadsourcesController.php       — AdminController
│   └── DisplayController.php           — default controller (routes to Dashboard)
├── Enum\
│   ├── Campaignstatus.php              — Draft|Active|Paused|Completed|Archived
│   ├── Campaignchannel.php             — Email|Social|Ppc|Seo|Event|Referral|Direct|Other
│   ├── Leadstatus.php                  — New|Contacted|Qualified|Unqualified|Converted|Lost
│   ├── Activitytype.php                — StatusChange|Note|EmailSent|FormSubmit|CallLogged|Assigned
│   └── Touchtype.php                   — First|Middle|Last|Conversion
├── Event\
│   ├── LeadConvertedEvent.php
│   ├── LeadStatusChangedEvent.php
│   ├── CampaignActivatedEvent.php
│   ├── CampaignBudgetExceededEvent.php
│   └── AttributionCapturedEvent.php
├── Extension\
│   └── CampaignsComponent.php          — BootableExtensionInterface, exposes getContainer()
├── Field\
│   ├── LeadstatusField.php             — select, backed by Leadstatus enum
│   ├── CampaignstatusField.php         — select, backed by Campaignstatus enum
│   └── CampaignField.php               — modal picker (choose a campaign to associate with a lead)
├── Helper\
│   └── CampaignsHelper.php             — ContentHelper::getActions() wrapper, dashboard KPI formatting
├── Model\
│   ├── CampaignModel.php               — AdminModel (canonical CRUD + validation)
│   ├── CampaignsModel.php              — ListModel (canonical list query)
│   ├── CampaignDataModel.php           — BaseDatabaseModel, sole DB access for CampaignService
│   ├── LeadModel.php                   — AdminModel (canonical CRUD + validation)
│   ├── LeadsModel.php                  — ListModel
│   ├── LeadDataModel.php               — BaseDatabaseModel, sole DB access for LeadService
│   ├── LeadsourceModel.php             — AdminModel
│   ├── LeadsourcesModel.php            — ListModel
│   ├── LeadsourceDataModel.php         — BaseDatabaseModel
│   ├── AttributionsModel.php           — ListModel (read-only attribution log viewer)
│   ├── AttributionDataModel.php        — BaseDatabaseModel, sole DB access for AttributionService
│   ├── LeadactivitiesModel.php         — ListModel (read-only activity timeline)
│   ├── LeadactivityDataModel.php       — BaseDatabaseModel, sole DB access for LeadactivityService
│   └── DashboardModel.php              — BaseDatabaseModel (KPI aggregates for admin dashboard view)
├── Service\
│   ├── CampaignServiceInterface.php
│   ├── CampaignService.php             — CANONICAL: activate/pause/complete/archive, ROI calc
│   ├── LeadServiceInterface.php
│   ├── LeadService.php                 — CANONICAL: convert, assign, score, status transitions
│   ├── AttributionServiceInterface.php
│   ├── AttributionService.php          — CANONICAL: multi-touch capture, first/last-touch resolution
│   ├── LeadactivityServiceInterface.php
│   └── LeadactivityService.php         — CANONICAL: activity/audit trail logging
├── Table\
│   ├── CampaignTable.php
│   ├── LeadTable.php
│   ├── LeadsourceTable.php
│   ├── LeadcampaignmapTable.php        — minimal link-table CUD
│   ├── AttributionTable.php            — insert-mostly log table
│   └── LeadactivityTable.php           — insert-mostly log table
└── View\
    ├── Campaign\HtmlView.php
    ├── Campaigns\HtmlView.php
    ├── Lead\HtmlView.php
    ├── Leads\HtmlView.php
    ├── Leadsource\HtmlView.php
    ├── Leadsources\HtmlView.php
    ├── Leadactivities\HtmlView.php     — activity timeline sub-view for a lead
    └── Dashboard\HtmlView.php          — KPI widgets (leads by status, campaign ROI)

NextPro\Component\Campaigns\Site\
├── Controller\
│   ├── DisplayController.php           — public campaign landing / capture-form display
│   └── LeadController.php              — extends Administrator\Controller\LeadController; public form submit
├── Helper\
│   └── CampaignsHelper.php             — route-building helper for landing/thank-you pages
├── Model\
│   ├── CampaignModel.php               — extends Administrator\Model\CampaignModel (+ published/access filter)
│   └── LeadModel.php                   — extends Administrator\Model\LeadModel (+ honeypot/spam-guard fields only)
├── Service\
│   └── Router.php                      — RouterView-based SEF for campaign landing pages (alias-only, flat)
└── View\
    ├── Campaign\HtmlView.php           — public landing page
    └── Leadcapture\HtmlView.php        — embeddable capture form (menu-item driven)

NextPro\Component\Campaigns\Api\
├── Controller\
│   ├── LeadsController.php             — extends ApiController; POST ingestion endpoint
│   └── CampaignsController.php         — extends ApiController; read-only reporting endpoint
└── View\
    ├── Lead\JsonApiView.php
    ├── Leads\JsonApiView.php
    ├── Campaign\JsonApiView.php
    └── Campaigns\JsonApiView.php

NextPro\Component\Campaigns\Cli\
└── Command\
    └── RecalculateattributionCommand.php  — extends AbstractCommand; nightly first/last-touch recompute
```

**DRY placement summary**: every validation rule, save/delete rule, ACL check, and business workflow lives once in `Administrator\Model\*` and `Administrator\Service\*`. Site models override only the read-path (published/access filtering); Site's `LeadController` calls `parent::save()` for all persistence logic. Api controllers inject Administrator DataModels/Services directly via `bootComponent()` — no duplicated business rules. Cli command injects `AttributionService` via constructor DI.

---

## 2. DI Wiring Plan

`administrator/components/com_campaigns/services/provider.php`:

```php
<?php

defined('_JEXEC') or die;

use Joomla\CMS\Dispatcher\ComponentDispatcherFactoryInterface;
use Joomla\CMS\Extension\ComponentInterface;
use Joomla\CMS\Extension\Service\Provider\CategoryFactory;
use Joomla\CMS\Extension\Service\Provider\ComponentDispatcherFactory;
use Joomla\CMS\Extension\Service\Provider\MVCFactory;
use Joomla\CMS\Extension\Service\Provider\RouterFactory;
use Joomla\CMS\HTML\Registry;
use Joomla\CMS\MVC\Factory\MVCFactoryInterface;
use Joomla\DI\Container;
use Joomla\DI\ServiceProviderInterface;
use NextPro\Component\Campaigns\Administrator\Extension\CampaignsComponent;
use NextPro\Component\Campaigns\Administrator\Model\AttributionDataModel;
use NextPro\Component\Campaigns\Administrator\Model\CampaignDataModel;
use NextPro\Component\Campaigns\Administrator\Model\LeadactivityDataModel;
use NextPro\Component\Campaigns\Administrator\Model\LeadDataModel;
use NextPro\Component\Campaigns\Administrator\Model\LeadsourceDataModel;
use NextPro\Component\Campaigns\Administrator\Service\AttributionService;
use NextPro\Component\Campaigns\Administrator\Service\AttributionServiceInterface;
use NextPro\Component\Campaigns\Administrator\Service\CampaignService;
use NextPro\Component\Campaigns\Administrator\Service\CampaignServiceInterface;
use NextPro\Component\Campaigns\Administrator\Service\LeadactivityService;
use NextPro\Component\Campaigns\Administrator\Service\LeadactivityServiceInterface;
use NextPro\Component\Campaigns\Administrator\Service\LeadService;
use NextPro\Component\Campaigns\Administrator\Service\LeadServiceInterface;

return new class () implements ServiceProviderInterface {
    public function register(Container $container): void
    {
        // --- Core component factories -----------------------------------
        $container->registerServiceProvider(new CategoryFactory('\\NextPro\\Component\\Campaigns'));
        $container->registerServiceProvider(new ComponentDispatcherFactory('\\NextPro\\Component\\Campaigns'));
        $container->registerServiceProvider(new MVCFactory('\\NextPro\\Component\\Campaigns'));
        $container->registerServiceProvider(new RouterFactory('\\NextPro\\Component\\Campaigns'));

        // --- DataModels (sole DB access layer for Services) -------------
        $container->set(CampaignDataModel::class, fn (Container $c) =>
            $c->get(MVCFactoryInterface::class)->createModel('CampaignData', 'Administrator', ['ignore_request' => true]));

        $container->set(LeadDataModel::class, fn (Container $c) =>
            $c->get(MVCFactoryInterface::class)->createModel('LeadData', 'Administrator', ['ignore_request' => true]));

        $container->set(LeadsourceDataModel::class, fn (Container $c) =>
            $c->get(MVCFactoryInterface::class)->createModel('LeadsourceData', 'Administrator', ['ignore_request' => true]));

        $container->set(AttributionDataModel::class, fn (Container $c) =>
            $c->get(MVCFactoryInterface::class)->createModel('AttributionData', 'Administrator', ['ignore_request' => true]));

        $container->set(LeadactivityDataModel::class, fn (Container $c) =>
            $c->get(MVCFactoryInterface::class)->createModel('LeadactivityData', 'Administrator', ['ignore_request' => true]));

        // --- Business logic services (DataModels + Services only) ------
        $container->set(LeadactivityServiceInterface::class, fn (Container $c) =>
            new LeadactivityService($c->get(LeadactivityDataModel::class)));
        $container->alias(LeadactivityService::class, LeadactivityServiceInterface::class);

        $container->set(AttributionServiceInterface::class, fn (Container $c) =>
            new AttributionService(
                $c->get(AttributionDataModel::class),
                $c->get(LeadDataModel::class),
                $c->get(CampaignDataModel::class),
            ));
        $container->alias(AttributionService::class, AttributionServiceInterface::class);

        $container->set(LeadServiceInterface::class, fn (Container $c) =>
            new LeadService(
                $c->get(LeadDataModel::class),
                $c->get(CampaignDataModel::class),
                $c->get(LeadactivityServiceInterface::class),
            ));
        $container->alias(LeadService::class, LeadServiceInterface::class);

        $container->set(CampaignServiceInterface::class, fn (Container $c) =>
            new CampaignService(
                $c->get(CampaignDataModel::class),
                $c->get(LeadDataModel::class),
                $c->get(AttributionServiceInterface::class),
                $c->get(LeadactivityServiceInterface::class),
            ));
        $container->alias(CampaignService::class, CampaignServiceInterface::class);

        // --- Component extension -----------------------------------------
        $container->set(
            ComponentInterface::class,
            function (Container $container) {
                $component = new CampaignsComponent($container->get(ComponentDispatcherFactoryInterface::class));
                $component->setMVCFactory($container->get(MVCFactoryInterface::class));
                $component->setRegistry($container->get(Registry::class));
                $component->setRouterFactory($container->get(RouterFactory::class));

                return $component;
            }
        );
    }
};
```

**`CampaignsComponent`** implements `BootableExtensionInterface`, stores the container from `boot()`, and exposes an `@internal getContainer(): ContainerInterface` per the `bootComponent()` bridge pattern — required because the Api controllers, the Cli command, and a companion System plugin (§5.3) all need to resolve `LeadService`/`AttributionService`/`CampaignService` from **outside** the component's own MVC stack.

No service ever injects `DatabaseInterface` or `MVCFactoryInterface` directly — only DataModels and other Services, per `joomla-di-patterns.md`.

---

## 3. Class Hierarchy & Contracts

### 3.1 Base classes extended

| Class | Extends | Notes |
|---|---|---|
| `CampaignModel` | `Joomla\CMS\MVC\Model\AdminModel` | canonical CRUD; uses `DebugErrorAwareTrait` |
| `CampaignsModel` | `Joomla\CMS\MVC\Model\ListModel` | canonical list query; uses `DebugErrorAwareTrait` |
| `LeadModel` | `AdminModel` | canonical CRUD; uses `DebugErrorAwareTrait` |
| `LeadsModel` | `ListModel` | uses `DebugErrorAwareTrait` |
| `LeadsourceModel` | `AdminModel` | uses `DebugErrorAwareTrait` |
| `LeadsourcesModel` | `ListModel` | uses `DebugErrorAwareTrait` |
| `AttributionsModel` | `ListModel` | read-only; uses `DebugErrorAwareTrait` |
| `LeadactivitiesModel` | `ListModel` | read-only; uses `DebugErrorAwareTrait` |
| `*DataModel` (×5) | `Joomla\CMS\MVC\Model\BaseDatabaseModel` | no `DebugErrorAwareTrait` per convention |
| `DashboardModel` | `BaseDatabaseModel` | KPI aggregate reads |
| `CampaignTable` / `LeadTable` / `LeadsourceTable` / `LeadcampaignmapTable` / `AttributionTable` / `LeadactivityTable` | `Joomla\CMS\Table\Table` | every write path — including the link table and the two log tables — goes through a `Table` class; no raw insert/update in Models or Services (Joomla-first philosophy, no exceptions) |
| `CampaignController` / `LeadController` / `LeadsourceController` | `Joomla\CMS\MVC\Controller\FormController` | |
| `CampaignsController` / `LeadsController` / `LeadsourcesController` | `Joomla\CMS\MVC\Controller\AdminController` | |
| `Site\Controller\LeadController` | `Administrator\Controller\LeadController` | overrides only redirect target |
| `Api\Controller\LeadsController` / `CampaignsController` | `Joomla\CMS\MVC\Controller\ApiController` | |
| `Cli\Command\RecalculateattributionCommand` | `Joomla\Console\Command\AbstractCommand` | |
| `CampaignsComponent` | `Joomla\CMS\Extension\MVCComponent` implements `BootableExtensionInterface` | |

### 3.2 Service interfaces

```php
interface CampaignServiceInterface
{
    public function activate(int $campaignId): void;
    public function pause(int $campaignId): void;
    public function complete(int $campaignId): void;
    public function archive(int $campaignId): void;
    public function calculateRoi(int $campaignId): array;
    public function getPerformanceSummary(int $campaignId): array;
}

interface LeadServiceInterface
{
    public function convert(int $leadId, ?int $campaignId = null): void;
    public function assignTo(int $leadId, int $userId): void;
    public function recalculateScore(int $leadId): int;
    public function changeStatus(int $leadId, Leadstatus $status, ?string $note = null): void;
}

interface AttributionServiceInterface
{
    public function captureTouch(array $touchData): void;
    public function determineFirstTouch(int $leadId): ?int;
    public function determineLastTouch(int $leadId): ?int;
    public function getAttributionReport(int $campaignId): array;
}

interface LeadactivityServiceInterface
{
    public function log(int $leadId, Activitytype $type, string $description, ?int $campaignId = null): void;
    public function getTimeline(int $leadId): array;
}
```

`LeadService` depends on: `LeadDataModel`, `CampaignDataModel`, `LeadactivityServiceInterface`.
`CampaignService` depends on: `CampaignDataModel`, `LeadDataModel`, `AttributionServiceInterface`, `LeadactivityServiceInterface`.
`AttributionService` depends on: `AttributionDataModel`, `LeadDataModel`, `CampaignDataModel`.
`LeadactivityService` depends on: `LeadactivityDataModel`.

None inject `DatabaseInterface`. The `Leadcampaignmap` link table has **no dedicated DataModel** — `LeadDataModel` and `CampaignDataModel` instantiate `LeadcampaignmapTable` directly for `attachCampaign()`/`detachCampaign()` calls (minimal join table, no business validation needed beyond uniqueness, which the table's `UNIQUE KEY` enforces).

### 3.3 Enums (PHP 8.3 backed enums)

```php
enum Campaignstatus: string
{
    case Draft = 'draft';
    case Active = 'active';
    case Paused = 'paused';
    case Completed = 'completed';
    case Archived = 'archived';
}

enum Campaignchannel: string
{
    case Email = 'email';
    case Social = 'social';
    case Ppc = 'ppc';
    case Seo = 'seo';
    case Event = 'event';
    case Referral = 'referral';
    case Direct = 'direct';
    case Other = 'other';
}

enum Leadstatus: string
{
    case New = 'new';
    case Contacted = 'contacted';
    case Qualified = 'qualified';
    case Unqualified = 'unqualified';
    case Converted = 'converted';
    case Lost = 'lost';
}

enum Activitytype: string
{
    case StatusChange = 'status_change';
    case Note = 'note';
    case EmailSent = 'email_sent';
    case FormSubmit = 'form_submit';
    case CallLogged = 'call_logged';
    case Assigned = 'assigned';
}

enum Touchtype: string
{
    case First = 'first';
    case Middle = 'middle';
    case Last = 'last';
    case Conversion = 'conversion';
}
```

All are single-word entity names per the case convention (`Publicationstate`-style), stored as `VARCHAR` columns (see §4), and consumed by `LeadstatusField`/`CampaignstatusField` custom form fields.

---

## 4. Database Schema

Table classification applied per `joomla-architect.md` §Phase 4 rules. No hierarchical/nested-set table is needed — campaigns are grouped via Joomla's core `#__categories` (extension `com_campaigns.campaign`), not a custom parent-child tree, so no `parent_id`/`lft`/`rgt`/`level` columns anywhere in this schema (see ADR-3 rationale is separate; category use is a design default, not an ADR-worthy fork).

No DB-level `FOREIGN KEY` constraints are used, matching Joomla core convention (e.g. `#__contentitem_tag_map`) — referential integrity is enforced in the Service/DataModel layer, not the schema.

### 4.1 `#__campaigns_campaigns` — CORE/CRUD table

User-managed entity with full workflow, scheduling, and per-item ACL (marketing team members may own individual campaigns) → **full standard field set** including the optional `asset_id`, `alias`, `publish_up`/`publish_down`, `language`.

```sql
CREATE TABLE IF NOT EXISTS `#__campaigns_campaigns` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `asset_id` INT UNSIGNED NOT NULL DEFAULT 0,
    `title` VARCHAR(255) NOT NULL DEFAULT '',
    `alias` VARCHAR(400) NOT NULL DEFAULT '',
    `description` TEXT,
    `catid` INT UNSIGNED NOT NULL DEFAULT 0,
    `channel` VARCHAR(20) NOT NULL DEFAULT 'other',
    `status` VARCHAR(20) NOT NULL DEFAULT 'draft',
    `budget` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `actual_spend` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `goal_leads` INT UNSIGNED NOT NULL DEFAULT 0,
    `start_date` DATE DEFAULT NULL,
    `end_date` DATE DEFAULT NULL,
    `utm_source` VARCHAR(100) NOT NULL DEFAULT '',
    `utm_medium` VARCHAR(100) NOT NULL DEFAULT '',
    `utm_campaign` VARCHAR(100) NOT NULL DEFAULT '',
    `target_url` VARCHAR(2048) NOT NULL DEFAULT '',
    `params` TEXT,
    `state` TINYINT(1) NOT NULL DEFAULT 0,
    `ordering` INT NOT NULL DEFAULT 0,
    `access` INT UNSIGNED NOT NULL DEFAULT 1,
    `created` DATETIME NOT NULL,
    `created_by` INT UNSIGNED NOT NULL DEFAULT 0,
    `modified` DATETIME DEFAULT NULL,
    `modified_by` INT UNSIGNED NOT NULL DEFAULT 0,
    `checked_out` INT UNSIGNED DEFAULT NULL,
    `checked_out_time` DATETIME DEFAULT NULL,
    `publish_up` DATETIME DEFAULT NULL,
    `publish_down` DATETIME DEFAULT NULL,
    `language` CHAR(7) NOT NULL DEFAULT '*',
    PRIMARY KEY (`id`),
    KEY `idx_state` (`state`),
    KEY `idx_created_by` (`created_by`),
    KEY `idx_access` (`access`),
    KEY `idx_checked_out` (`checked_out`),
    KEY `idx_language` (`language`),
    KEY `idx_alias` (`alias`(191)),
    KEY `idx_catid` (`catid`),
    KEY `idx_status` (`status`),
    KEY `idx_channel` (`channel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Note: `status` (business lifecycle: draft/active/paused/completed/archived) is intentionally distinct from Joomla's native `state` (publish/unpublish/archive/trash) — see ADR-3.

### 4.2 `#__campaigns_leads` — CORE/CRUD table

User-managed entity, full CRUD via admin forms → **mandatory standard field set**. No `asset_id`/`alias`/`publish_*`/`language` — leads are not published content, have no SEF alias, and per-item ACL is deliberately handled via `assigned_to` + `core.edit.own` rather than the asset table (see ADR-2).

```sql
CREATE TABLE IF NOT EXISTS `#__campaigns_leads` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(150) NOT NULL DEFAULT '',
    `last_name` VARCHAR(150) NOT NULL DEFAULT '',
    `email` VARCHAR(255) NOT NULL DEFAULT '',
    `phone` VARCHAR(50) NOT NULL DEFAULT '',
    `company` VARCHAR(255) NOT NULL DEFAULT '',
    `job_title` VARCHAR(150) NOT NULL DEFAULT '',
    `source_id` INT UNSIGNED NOT NULL DEFAULT 0,
    `first_touch_campaign_id` INT UNSIGNED DEFAULT NULL,
    `last_touch_campaign_id` INT UNSIGNED DEFAULT NULL,
    `lead_status` VARCHAR(20) NOT NULL DEFAULT 'new',
    `score` INT NOT NULL DEFAULT 0,
    `assigned_to` INT UNSIGNED NOT NULL DEFAULT 0,
    `converted_date` DATETIME DEFAULT NULL,
    `notes` TEXT,
    `state` TINYINT(1) NOT NULL DEFAULT 1,
    `ordering` INT NOT NULL DEFAULT 0,
    `access` INT UNSIGNED NOT NULL DEFAULT 1,
    `created` DATETIME NOT NULL,
    `created_by` INT UNSIGNED NOT NULL DEFAULT 0,
    `modified` DATETIME DEFAULT NULL,
    `modified_by` INT UNSIGNED NOT NULL DEFAULT 0,
    `checked_out` INT UNSIGNED DEFAULT NULL,
    `checked_out_time` DATETIME DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_state` (`state`),
    KEY `idx_created_by` (`created_by`),
    KEY `idx_access` (`access`),
    KEY `idx_checked_out` (`checked_out`),
    KEY `idx_email` (`email`(191)),
    KEY `idx_lead_status` (`lead_status`),
    KEY `idx_source_id` (`source_id`),
    KEY `idx_assigned_to` (`assigned_to`),
    KEY `idx_first_touch_campaign` (`first_touch_campaign_id`),
    KEY `idx_last_touch_campaign` (`last_touch_campaign_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4.3 `#__campaigns_sources` — SECONDARY entity table

Admin-managed reference data (Website Form, Trade Show, Cold Call, Referral, Paid Ad, Organic Search, …) → **minimum field set only**: `state`, `created`, `created_by`, `modified`, `modified_by`.

```sql
CREATE TABLE IF NOT EXISTS `#__campaigns_sources` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(150) NOT NULL DEFAULT '',
    `description` VARCHAR(255) NOT NULL DEFAULT '',
    `is_default` TINYINT(1) NOT NULL DEFAULT 0,
    `state` TINYINT(1) NOT NULL DEFAULT 1,
    `created` DATETIME NOT NULL,
    `created_by` INT UNSIGNED NOT NULL DEFAULT 0,
    `modified` DATETIME DEFAULT NULL,
    `modified_by` INT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    KEY `idx_state` (`state`),
    KEY `idx_created_by` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4.4 `#__campaigns_lead_campaign_map` — LINK/JOIN table

Curated, user-editable many-to-many association between a Lead and any Campaign a sales rep manually tags for reporting (distinct from the automatic tracking log in §4.5) → **minimal columns only**, no system fields.

```sql
CREATE TABLE IF NOT EXISTS `#__campaigns_lead_campaign_map` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `lead_id` INT UNSIGNED NOT NULL,
    `campaign_id` INT UNSIGNED NOT NULL,
    `ordering` INT NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_lead_campaign` (`lead_id`, `campaign_id`),
    KEY `idx_campaign_id` (`campaign_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4.5 `#__campaigns_attributions` — SYSTEM/LOG table

Auto-generated by the tracking pixel / UTM capture on every touch (site form view, API webhook) → **only `created` + relevant foreign keys/data**, insert-only, no `modified`/`state`.

```sql
CREATE TABLE IF NOT EXISTS `#__campaigns_attributions` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `lead_id` INT UNSIGNED NOT NULL,
    `campaign_id` INT UNSIGNED DEFAULT NULL,
    `touch_type` VARCHAR(20) NOT NULL DEFAULT 'middle',
    `utm_source` VARCHAR(100) NOT NULL DEFAULT '',
    `utm_medium` VARCHAR(100) NOT NULL DEFAULT '',
    `utm_campaign` VARCHAR(100) NOT NULL DEFAULT '',
    `utm_content` VARCHAR(100) NOT NULL DEFAULT '',
    `utm_term` VARCHAR(100) NOT NULL DEFAULT '',
    `referrer_url` VARCHAR(2048) NOT NULL DEFAULT '',
    `landing_url` VARCHAR(2048) NOT NULL DEFAULT '',
    `created` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_lead_id` (`lead_id`),
    KEY `idx_campaign_id` (`campaign_id`),
    KEY `idx_touch_type` (`touch_type`),
    KEY `idx_created` (`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4.6 `#__campaigns_lead_activities` — SYSTEM/LOG table

Auto-generated audit trail (status changes, notes, emails, calls) → **only `created` + FKs + activity payload**, insert-only.

```sql
CREATE TABLE IF NOT EXISTS `#__campaigns_lead_activities` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `lead_id` INT UNSIGNED NOT NULL,
    `campaign_id` INT UNSIGNED DEFAULT NULL,
    `activity_type` VARCHAR(20) NOT NULL DEFAULT 'note',
    `description` TEXT,
    `created` DATETIME NOT NULL,
    `created_by` INT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    KEY `idx_lead_id` (`lead_id`),
    KEY `idx_campaign_id` (`campaign_id`),
    KEY `idx_activity_type` (`activity_type`),
    KEY `idx_created` (`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4.7 Table classification summary

| Table | Classification | System-field set applied |
|---|---|---|
| `#__campaigns_campaigns` | Core/CRUD | Full + asset_id, alias, publish_up/down, language |
| `#__campaigns_leads` | Core/CRUD | Full (no asset_id/alias/publish/language — see ADR-2) |
| `#__campaigns_sources` | Secondary | Minimum (state, created(_by), modified(_by)) |
| `#__campaigns_lead_campaign_map` | Link/join | None — FKs + ordering only |
| `#__campaigns_attributions` | System/log | `created` only + FKs/payload |
| `#__campaigns_lead_activities` | System/log | `created`, `created_by` + FKs/payload |

### 4.8 Versioning

Initial schema ships as `administrator/components/com_campaigns/sql/install.mysql.utf8.sql`. Future changes follow the Git-Stage Rule in `sql/updates/mysql/` (unstaged file = current WIP; sealed once committed) per `joomla-coding-preferences.md`.

---

## 5. Event Flow

### 5.1 Core Joomla events inherited automatically

`CampaignModel`, `LeadModel`, and `LeadsourceModel` all extend `AdminModel`, so `onContentBeforeSave` / `onContentAfterSave` / `onContentChangeState` / `onContentBeforeDelete` / `onContentAfterDelete` fire automatically on every save/delete with contexts `com_campaigns.campaign`, `com_campaigns.lead`, and `com_campaigns.leadsource` respectively — no custom dispatch code is needed for these; they come free from the base class.

**Naming note**: custom `*Event` classes below follow core Joomla's own convention (`AfterSaveEvent`, `ItemProcessedEvent` — both multi-word) rather than the entity-collapse rule, because Event classes are constructed with an explicit FQCN and are never resolved via `ucfirst(strtolower())`. This is consistent with the worked example already in `joomla-events-system.md`.

### 5.2 Custom events dispatched by this component

| Event name | Event class | Dispatched by | Arguments |
|---|---|---|---|
| `onCampaignsLeadConverted` | `LeadConvertedEvent` | `LeadService::convert()` | `lead`, `campaignId` |
| `onCampaignsLeadStatusChanged` | `LeadStatusChangedEvent` | `LeadService::changeStatus()` | `lead`, `oldStatus`, `newStatus` |
| `onCampaignsCampaignActivated` | `CampaignActivatedEvent` | `CampaignService::activate()` | `campaign` |
| `onCampaignsCampaignBudgetExceeded` | `CampaignBudgetExceededEvent` | `CampaignService` (checked on every spend update) | `campaign`, `budget`, `actualSpend` |
| `onCampaignsAttributionCaptured` | `AttributionCapturedEvent` | `AttributionService::captureTouch()` | `lead`, `campaign`, `touchType` |

Example dispatch (`CampaignService::activate()`):

```php
$event = new CampaignActivatedEvent('onCampaignsCampaignActivated', [
    'subject' => $campaign,
    'context' => 'com_campaigns.campaign',
]);

$this->dispatcher->dispatch($event->getName(), $event);
```

Services receive `DispatcherInterface` via constructor injection (not `Factory::getApplication()->getDispatcher()`), consistent with the DI-over-service-locator principle.

### 5.3 Plugin integration points

- **`onCampaignsLeadConverted`** — a companion `plg_system_campaignscrm` (out of scope here) could sync converted leads to an external CRM.
- **`onCampaignsCampaignBudgetExceeded`** — a notification plugin can alert the campaign owner via `Factory::getMailer()`.
- **`onUserAfterSave`** (core event, **hooked into**, not dispatched) — a small companion system plugin subscribes to this to auto-match/merge a newly registered site user with an existing Lead by email, calling `LeadService::convert()`. This plugin resolves the service via `Factory::getApplication()->bootComponent('com_campaigns')->getContainer()->get(LeadServiceInterface::class)` per the `bootComponent()` bridge pattern.
- **`onCampaignsAttributionCaptured`** — analytics/webhook plugins can forward the touch to an external ad-platform conversion API in real time.

### 5.4 Why not core Workflow

Campaign lifecycle is **not** implemented on Joomla's core `WorkflowServiceInterface` (used by `com_content`). See ADR-4.

---

## 6. ACL Matrix

### 6.1 `access.xml` structure

```xml
<?xml version="1.0" encoding="utf-8"?>
<access component="com_campaigns">
    <section name="component">
        <action name="core.admin"              title="JACTION_ADMIN"              description="JACTION_ADMIN_COMPONENT_DESC" />
        <action name="core.manage"             title="JACTION_MANAGE"             description="JACTION_MANAGE_COMPONENT_DESC" />
        <action name="core.create"             title="JACTION_CREATE"             description="JACTION_CREATE_COMPONENT_DESC" />
        <action name="core.delete"             title="JACTION_DELETE"             description="JACTION_DELETE_COMPONENT_DESC" />
        <action name="core.edit"               title="JACTION_EDIT"               description="JACTION_EDIT_COMPONENT_DESC" />
        <action name="core.edit.state"         title="JACTION_EDITSTATE"          description="JACTION_EDITSTATE_COMPONENT_DESC" />
        <action name="core.edit.own"           title="JACTION_EDITOWN"            description="JACTION_EDITOWN_COMPONENT_DESC" />
        <action name="campaigns.convert.lead"  title="COM_CAMPAIGNS_ACTION_CONVERT_LEAD"  description="COM_CAMPAIGNS_ACTION_CONVERT_LEAD_DESC" />
        <action name="campaigns.assign.lead"   title="COM_CAMPAIGNS_ACTION_ASSIGN_LEAD"   description="COM_CAMPAIGNS_ACTION_ASSIGN_LEAD_DESC" />
        <action name="campaigns.export"        title="COM_CAMPAIGNS_ACTION_EXPORT"        description="COM_CAMPAIGNS_ACTION_EXPORT_DESC" />
        <action name="campaigns.view.report"   title="COM_CAMPAIGNS_ACTION_VIEW_REPORT"   description="COM_CAMPAIGNS_ACTION_VIEW_REPORT_DESC" />
        <action name="campaigns.manage.sources" title="COM_CAMPAIGNS_ACTION_MANAGE_SOURCES" description="COM_CAMPAIGNS_ACTION_MANAGE_SOURCES_DESC" />
    </section>
    <section name="campaign">
        <action name="core.delete"     title="JACTION_DELETE"     description="JACTION_DELETE_COMPONENT_DESC" />
        <action name="core.edit"       title="JACTION_EDIT"       description="JACTION_EDIT_COMPONENT_DESC" />
        <action name="core.edit.state" title="JACTION_EDITSTATE"  description="JACTION_EDITSTATE_COMPONENT_DESC" />
        <action name="core.edit.own"   title="JACTION_EDITOWN"    description="JACTION_EDITOWN_COMPONENT_DESC" />
    </section>
</access>
```

### 6.2 Permission matrix

| Action | Scope | Granted by default to | Checked in |
|---|---|---|---|
| `core.admin` | Component | Super Users | Options/config screen |
| `core.manage` | Component | Manager, Administrator | backend menu visibility |
| `core.create` | Component | Manager | `CampaignController::save()`, `LeadController::save()` |
| `core.edit` | Component + per-item (`campaign` asset) | Manager | `CampaignController::save()` (any record) |
| `core.edit.own` | Component + per-item | Publisher-equivalent role | `LeadController::save()` when `created_by === user->id`, and `CampaignController::save()` via asset inheritance |
| `core.edit.state` | Component + per-item | Manager | publish/unpublish/archive/trash toolbar actions |
| `core.delete` | Component + per-item | Manager | `CampaignsController::delete()`, `LeadsController::delete()` |
| `campaigns.convert.lead` | Component | Manager, Sales role | `LeadService::convert()` guard in `LeadController` |
| `campaigns.assign.lead` | Component | Manager | `LeadService::assignTo()` guard |
| `campaigns.export` | Component | Manager (privacy-sensitive — PII export) | `LeadsController::export()` |
| `campaigns.view.report` | Component | Manager, Marketing role | `CampaignController::report()`, Dashboard view |
| `campaigns.manage.sources` | Component | Manager | `LeadsourceController`/`LeadsourcesController` |

### 6.3 Entity-level ACL notes

- **Campaign** uses `asset_id` → full per-item ACL via the Joomla assets table, inheriting from the `com_campaigns` component asset. This lets a marketing lead grant `core.edit` on one specific campaign to a junior team member without giving them `core.edit` component-wide.
- **Lead** deliberately has **no** `asset_id` / per-item asset-table ACL. Row-level ownership is enforced via `assigned_to` (current owner) and `created_by` (creator), checked in `LeadService`/`LeadModel`, not the asset table — see ADR-2 for rationale.
- Views check `Factory::getApplication()->getIdentity()->authorise('action', 'com_campaigns')` (component-level) or `->authorise('action', 'com_campaigns.campaign.' . $id)` (item-level, Campaign only).

---

## 7. Routing & URL Design (site-facing — minimal, justified)

The component needs exactly one site-facing capability: an embeddable lead-capture form (via menu item) and, optionally, a public campaign landing page addressed by its `alias`. No category tree browsing is exposed publicly, so a full `RouterView`-based nested router is unnecessary — flat alias-based lookup suffices.

- **Menu item types**: "Campaign Landing Page" (`view=campaign&id=`), "Lead Capture Form" (`view=leadcapture&campaign_id=`).
- **SEF pattern**: `/campaigns/{campaign-alias}` → `index.php?option=com_campaigns&view=campaign&id={id}` via `Site\Service\Router` built on `Joomla\CMS\Component\Router\RouterView` with a single, non-hierarchical view.
- Lead-capture submissions POST to `Site\Controller\LeadController::save()`, which calls `parent::save()` (Administrator's full validation/persist path) and redirects to a "thank you" display state — no business logic duplicated in Site.

---

## 8. API Design (REST — minimal, justified)

External marketing tools (landing-page builders, ad platforms, Zapier-style automation, other CRMs) commonly need to **push leads in** and **pull campaign performance out** — this is a mainstream, expected integration point for a lead-management component, so a REST surface is included.

| Method | Endpoint | Controller | Purpose | Auth |
|---|---|---|---|---|
| `POST` | `/api/index.php/v1/campaigns/leads` | `Api\Controller\LeadsController::add()` | External webhook ingestion — creates a Lead + captures an `Attribution` touch in one call | API token, scoped to `core.create` |
| `GET` | `/api/index.php/v1/campaigns/leads/{id}` | `Api\Controller\LeadsController::item()` | Fetch a single lead (CRM sync) | API token, `core.edit` or `core.edit.own` |
| `GET` | `/api/index.php/v1/campaigns/campaigns` | `Api\Controller\CampaignsController::index()` | List campaigns for reporting dashboards | API token, `campaigns.view.report` |
| `GET` | `/api/index.php/v1/campaigns/campaigns/{id}` | `Api\Controller\CampaignsController::item()` | Campaign detail incl. ROI summary | API token, `campaigns.view.report` |

All endpoints use Administrator `LeadDataModel`/`CampaignDataModel`/services directly (via `bootComponent()`), returning JSON:API documents through `JsonApiView`. No business logic is duplicated — `LeadsController::add()` calls `LeadServiceInterface`/`AttributionServiceInterface` exactly as the Site capture form does.

---

## 9. Architecture Decision Records

### ADR-1: Dual attribution model — curated link table + automatic system log

**Status**: Accepted
**Context**: A lead can be associated with a campaign in two conceptually different ways: (a) a sales rep manually tags a lead as related to a campaign for reporting purposes, and (b) the system automatically records every tracked touchpoint (UTM click, form view, landing-page visit) as the lead moves through multiple campaigns before converting.
**Decision**: Model these as two separate tables with different classifications — `#__campaigns_lead_campaign_map` (LINK/JOIN, minimal, user-curated, unique pair constraint) and `#__campaigns_attributions` (SYSTEM/LOG, append-only, one row per touch, `created`-only system fields).
**Consequences**: No ambiguity between "why is this pair linked" (curated) and "when/how did this touch happen" (log). Reporting queries against `attributions` can be timestamp-ordered without competing with the curated map's uniqueness constraint. Slight duplication of the `(lead_id, campaign_id)` relationship across two tables is an acceptable trade-off for clarity.
**Alternatives considered**: A single table with a `source` discriminator column (`manual` vs `auto`) — rejected because it would force the LINK table's "no system fields, unique pair" shape and the LOG table's "append-only, no uniqueness, timestamped" shape into one schema, defeating the purpose of Joomla's table-classification rules.

### ADR-2: Lead entity uses ownership-field ACL, not asset-table ACL

**Status**: Accepted
**Context**: Core/CRUD tables optionally get `asset_id` for per-item ACL via the Joomla assets table. Leads are high-volume (potentially thousands/month) and their access-control need is simple: "the assigned owner and managers can edit," not arbitrary per-record permission grants to arbitrary users/groups.
**Decision**: Omit `asset_id` from `#__campaigns_leads`. Enforce row-level access via `assigned_to` + `created_by` checked in `LeadService`/`LeadModel`, combined with the standard `core.edit.own` component-level action.
**Consequences**: Simpler schema, no per-lead entry in `#__assets` (avoids assets-table bloat at high lead volume), simpler queries (no asset join for permission checks). Trade-off: cannot grant a specific non-owner user `core.edit` on one specific lead without giving them `core.edit` component-wide — deemed acceptable since lead reassignment (`campaigns.assign.lead`) already solves the "wrong owner" case.
**Alternatives considered**: Full asset-table ACL identical to Campaign — rejected due to write/storage overhead at lead volume and because the ownership model already satisfies the real business requirement.

### ADR-3: `status` (business lifecycle) kept separate from Joomla's native `state` (publish state)

**Status**: Accepted
**Context**: Joomla's `state` column is a fixed 4-value publication switch (1/0/2/-2) tied to toolbar publish/unpublish/archive/trash actions and view-level access filtering. Campaigns also need a richer, independent business lifecycle (`draft → active → paused/completed → archived`) that drives budget validation and ROI reporting, not visibility.
**Decision**: Add a distinct `status VARCHAR(20)` column (backed by the `Campaignstatus` enum) alongside the standard `state` column; `CampaignService::activate()/pause()/complete()/archive()` mutate `status` and are entirely independent of the `state` toolbar actions.
**Consequences**: Two "state-like" columns on one table, which could look redundant to a future reader — mitigated with inline schema comments and this ADR. Enables campaign-specific business rules (e.g., "cannot `activate()` without `start_date`/`end_date` set") without overloading Joomla's publish-state semantics or blocking normal publish/unpublish/trash behaviour.
**Alternatives considered**: Overload `state` with extra negative/high values to represent business status — rejected as it would conflict with core Joomla's fixed interpretation of `state` in toolbar buttons, batch processing, and list-view filters.

### ADR-4: Campaign lifecycle implemented via Service methods, not core Workflow

**Status**: Accepted
**Context**: Joomla core provides a generic `WorkflowServiceInterface`/`#__workflow_*` feature (used by `com_content`) for configurable stage-based transitions.
**Decision**: Do not integrate `com_campaigns` with core Workflow. Implement the five-stage `Campaignstatus` lifecycle directly as `CampaignService` methods (`activate()`, `pause()`, `complete()`, `archive()`), each enforcing its own business rule (e.g., budget must be set before `activate()`, cannot `archive()` a campaign with unresolved leads still `New`).
**Consequences**: Faster to build and reason about for a fixed, small state set; transition-specific validation logic lives naturally in typed service methods rather than generic workflow configuration. Loses core Workflow's admin-configurable stage editor and its built-in ACL-per-stage — acceptable since this component's stages are fixed by business definition, not end-user configurable.
**Alternatives considered**: Full `WorkflowServiceInterface` integration — rejected as disproportionate machinery for a fixed 5-state linear-ish lifecycle whose transitions need custom cross-field validation (budget, dates, lead counts) that doesn't map cleanly onto generic workflow "stage" transitions.

---

## 10. Cross-check against `joomla-depreciated.md`

Verified the following are **absent** from this design (deprecated patterns avoided):

- ✅ No `ToolbarHelper::` static button calls anywhere in the design — toolbar wiring for `Campaigns`/`Leads`/`Leadsources` list/form views uses `$this->getDocument()->getToolbar()` instance methods (only `ToolbarHelper::title()` is used, which remains correct).
- ✅ No `JFactory::*`, no `Factory::getDate()` — Services and Models use `new Joomla\CMS\Date\Date()` directly for any timestamp needs beyond what Table/Model boilerplate already sets.
- ✅ No `$this->get('Items')`/`$this->get('Form')` magic-method view access — all `HtmlView` classes call `$this->getModel()->getItems()`/`getForm()`/`getPagination()` directly.
- ✅ No Bootstrap modals — the `CampaignField` modal picker and any confirmation dialogs use `<joomla-dialog>` / `data-joomla-dialog`.
- ✅ No `$app->input` / `Factory::getApplication()->input` direct property access — all input reads use `getInput()`.
- ✅ No raw SQL writes in Models or Services — every write (including the link table and the two log tables) goes through a `Table` class's `bind()`/`check()`/`store()`/`delete()`.
- ✅ No `InputFilter::getInstance()` — any framework `InputFilter` usage (e.g., sanitising lead-capture free-text fields) uses `new InputFilter(...)`.
- ✅ No Repository-pattern classes — data access uses Joomla's native `ListModel`/`AdminModel`/`BaseDatabaseModel` exclusively.
- ✅ No Service injecting `DatabaseInterface` — confirmed in §2/§3.2, all Services depend only on DataModels and other Services.

---

## 11. Deliverables checklist

- [x] Namespace Map (§1)
- [x] DI Wiring Plan (§2)
- [x] Class Hierarchy & Contracts (§3)
- [x] Database Schema (§4)
- [x] Event Flow (§5)
- [x] ACL Matrix (§6)
- [x] Routing (§7) — included, justified by site-facing lead-capture form + landing page
- [x] API Design (§8) — included, justified by external lead-ingestion webhook use case
- [x] ADRs (§9) — 4 recorded
