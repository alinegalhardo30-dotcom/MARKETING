<?php

defined('_JEXEC') or die;

use Joomla\CMS\Document\HtmlDocument;
use Joomla\CMS\Factory;
use Joomla\CMS\HTML\HTMLHelper;

/** @var HtmlDocument $this */

$app = Factory::getApplication();
$wa  = $this->getWebAssetManager();
$wa->usePreset('template.nextpro');
?>
<!DOCTYPE html>
<html lang="<?php echo $this->language; ?>" dir="<?php echo $this->direction; ?>">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?php echo htmlspecialchars($app->get('sitename')); ?> — Em manutenção</title>
    <jdoc:include type="metas" />
    <jdoc:include type="styles" />
    <jdoc:include type="scripts" />
</head>
<body class="tpl-nextpro tpl-nextpro--offline">
    <main id="main-content" class="container tpl-offline">
        <h1><?php echo htmlspecialchars($app->get('sitename')); ?></h1>
        <p><?php echo htmlspecialchars($app->get('offline_message', 'Este site está temporariamente em manutenção. Volte em breve.')); ?></p>
        <?php if ($app->get('offline_image')) : ?>
            <img src="<?php echo htmlspecialchars($app->get('offline_image')); ?>" alt="">
        <?php endif; ?>
        <?php if ($app->get('display_offline_login', 1)) : ?>
            <jdoc:include type="component" />
        <?php endif; ?>
    </main>
</body>
</html>
