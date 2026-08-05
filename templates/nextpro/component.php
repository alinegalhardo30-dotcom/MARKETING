<?php

defined('_JEXEC') or die;

use Joomla\CMS\Document\HtmlDocument;
use Joomla\CMS\Factory;

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
    <jdoc:include type="metas" />
    <jdoc:include type="styles" />
    <jdoc:include type="scripts" />
</head>
<body class="tpl-nextpro tpl-nextpro--bare">
    <jdoc:include type="message" />
    <jdoc:include type="component" />
</body>
</html>
