

## 1.1

- Add social network to blog widget.

Please run this :
ALTER TABLE `simpleblogs_blogpostwidget` ADD COLUMN `display_social_network_widget` TINYINT NULL  AFTER `display_template` ;
