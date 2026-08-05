<?php

defined('_JEXEC') or die;

use Joomla\CMS\Document\HtmlDocument;
use Joomla\CMS\Factory;
use Joomla\CMS\Language\Text;
use Joomla\CMS\Uri\Uri;

/** @var HtmlDocument $this */
/** @var Throwable $this->error */

$app = Factory::getApplication();
$wa  = $this->getWebAssetManager();
$wa->usePreset('template.nextpro');

$code = $this->error->getCode();
?>
<!DOCTYPE html>
<html lang="<?php echo $this->language; ?>" dir="<?php echo $this->direction; ?>">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?php echo htmlspecialchars($app->get('sitename')); ?> — <?php echo (int) $code; ?></title>
    <jdoc:include type="metas" />
    <jdoc:include type="styles" />
    <jdoc:include type="scripts" />
</head>
<body class="tpl-nextpro tpl-nextpro--error">
    <main id="main-content" class="container tpl-error">
        <h1 class="tpl-error__code"><?php echo (int) $code; ?></h1>
        <p class="tpl-error__message"><?php echo htmlspecialchars($this->error->getMessage()); ?></p>
        <a class="tpl-error__home" href="<?php echo Uri::root(); ?>">Voltar para a página inicial</a>
    </main>
</body>
</html>
