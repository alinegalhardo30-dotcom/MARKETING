<?php

defined('_JEXEC') or die;

use Joomla\CMS\Document\HtmlDocument;
use Joomla\CMS\Factory;
use Joomla\CMS\HTML\HTMLHelper;
use Joomla\CMS\Uri\Uri;

/** @var HtmlDocument $this */

$app = Factory::getApplication();
$wa  = $this->getWebAssetManager();
$wa->usePreset('template.nextpro');

$params        = $this->params;
$logo          = $params->get('logoFile', '');
$tagline       = $params->get('siteDescription', '');
$colorScheme   = $params->get('colorScheme', 'dark');
$containerMax  = $params->get('containerWidth', '1200');
$sidebarPos    = $params->get('sidebarPosition', 'none');
$hasSidebar    = $sidebarPos !== 'none' && $this->countModules('sidebar');

$this->setHtml5(true);
?>
<!DOCTYPE html>
<html lang="<?php echo $this->language; ?>" dir="<?php echo $this->direction; ?>" data-color-scheme="<?php echo htmlspecialchars($colorScheme); ?>">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#14171a">
    <jdoc:include type="metas" />
    <jdoc:include type="styles" />
    <jdoc:include type="scripts" />
    <style>:root { --container-max-width: <?php echo (int) $containerMax; ?>px; }</style>
</head>
<body class="tpl-nextpro<?php echo $hasSidebar ? ' has-sidebar has-sidebar--' . htmlspecialchars($sidebarPos) : ''; ?>">
    <a href="#main-content" class="visually-hidden-focusable skip-link">Ir para o conteúdo principal</a>

    <?php if ($this->countModules('topbar')) : ?>
        <div class="tpl-topbar">
            <div class="container">
                <jdoc:include type="modules" name="topbar" style="none" />
            </div>
        </div>
    <?php endif; ?>

    <header class="tpl-header">
        <div class="container tpl-header__inner">
            <a class="tpl-brand" href="<?php echo Uri::root(); ?>">
                <?php if ($logo) : ?>
                    <img src="<?php echo Uri::root() . htmlspecialchars($logo); ?>" alt="<?php echo htmlspecialchars($app->get('sitename')); ?>" class="tpl-brand__logo">
                <?php else : ?>
                    <?php // Placeholder mark — replace by setting the "Logo" template parameter to the real exported file. ?>
                    <svg class="tpl-brand__mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">
                        <path d="M2 6 L14 20 L2 34" stroke="currentColor" stroke-width="4" fill="none" opacity="0.35"/>
                        <path d="M10 6 L22 20 L10 34" stroke="currentColor" stroke-width="4" fill="none" opacity="0.65"/>
                        <path d="M18 6 L30 20 L18 34" stroke="currentColor" stroke-width="4" fill="none"/>
                    </svg>
                    <span class="tpl-brand__text"><?php echo htmlspecialchars($app->get('sitename')); ?></span>
                <?php endif; ?>
                <?php if ($tagline) : ?>
                    <span class="tpl-brand__tagline"><?php echo htmlspecialchars($tagline); ?></span>
                <?php endif; ?>
            </a>

            <button class="tpl-nav-toggle" type="button" data-action="toggle-nav" aria-expanded="false" aria-controls="tpl-main-nav">
                <span class="visually-hidden">Abrir menu</span>
                <span class="tpl-nav-toggle__bar"></span>
            </button>

            <nav id="tpl-main-nav" class="tpl-nav" aria-label="Menu principal">
                <jdoc:include type="modules" name="menu" style="none" />
            </nav>
        </div>
    </header>

    <?php if ($this->countModules('breadcrumbs')) : ?>
        <div class="tpl-breadcrumbs">
            <div class="container">
                <jdoc:include type="modules" name="breadcrumbs" style="none" />
            </div>
        </div>
    <?php endif; ?>

    <?php if ($this->countModules('banner')) : ?>
        <div class="tpl-banner">
            <jdoc:include type="modules" name="banner" style="none" />
        </div>
    <?php endif; ?>

    <div class="container tpl-layout">
        <main id="main-content" class="tpl-content">
            <jdoc:include type="message" />
            <jdoc:include type="component" />
        </main>

        <?php if ($hasSidebar) : ?>
            <aside class="tpl-sidebar" aria-label="Barra lateral">
                <jdoc:include type="modules" name="sidebar" style="card" />
            </aside>
        <?php endif; ?>
    </div>

    <footer class="tpl-footer">
        <div class="container">
            <jdoc:include type="modules" name="footer" style="none" />
            <p class="tpl-footer__copy">&copy; <?php echo date('Y'); ?> <?php echo htmlspecialchars($app->get('sitename')); ?>. Todos os direitos reservados.</p>
        </div>
    </footer>

    <jdoc:include type="modules" name="debug" style="none" />
</body>
</html>
