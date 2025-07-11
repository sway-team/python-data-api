/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 80028 (8.0.28)
 Source Host           : localhost:3306
 Source Schema         : python_data_api

 Target Server Type    : MySQL
 Target Server Version : 80028 (8.0.28)
 File Encoding         : 65001

 Date: 11/07/2025 19:07:06
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for app
-- ----------------------------
DROP TABLE IF EXISTS `app`;
CREATE TABLE `app` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'CODE',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '名称',
  `desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '描述',
  `ownerid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '创建者',
  `level` int NOT NULL DEFAULT '0' COMMENT '等级',
  `parent` int NOT NULL DEFAULT '0' COMMENT '父节点ID',
  `price` int NOT NULL DEFAULT '0' COMMENT '资金量',
  `mission` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '使命',
  `vision` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '愿景',
  `corevalue` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '核心价值观',
  `meta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `type` tinyint NOT NULL DEFAULT '0' COMMENT '类型',
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '状态',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='组织';

-- ----------------------------
-- Records of app
-- ----------------------------
BEGIN;
INSERT INTO `app` (`id`, `code`, `name`, `desc`, `ownerid`, `level`, `parent`, `price`, `mission`, `vision`, `corevalue`, `meta`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (1, 'workflow', '工作流系统', '默认节点', '{{ADMIN_TOKEN}}', 0, 0, 0, '快速搭建自己的应用', '一站式服务', '想要什么，就做什么', NULL, '{{ADMIN_TOKEN}}', '{{ADMIN_TOKEN}}', 0, 0, '2019-10-23 16:36:07', '2023-03-14 18:26:05');
COMMIT;

-- ----------------------------
-- Table structure for configbox
-- ----------------------------
DROP TABLE IF EXISTS `configbox`;
CREATE TABLE `configbox` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'CODE',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '名称',
  `desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '描述',
  `ownerid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '创建者',
  `level` int NOT NULL DEFAULT '0' COMMENT '等级',
  `group` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '父节点ID',
  `meta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `type` tinyint NOT NULL DEFAULT '0' COMMENT '类型',
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '状态',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='组织';

-- ----------------------------
-- Records of configbox
-- ----------------------------
BEGIN;
INSERT INTO `configbox` (`id`, `code`, `name`, `desc`, `ownerid`, `level`, `group`, `meta`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (172, 'common:topbar', 'topbar', '顶部导航', '', 0, 'common', '{\n\"url\":\"{{$SERVICE_HOST}}/service/getlist\",\"param\":{\"dataset\":\"workflow_tree\",\"group\":\"后台导航栏\"}\n}', 'b8b0278e93bfbbee36af8f7bcb909467', '{{ADMIN_TOKEN}}', 0, 1, '2025-07-07 00:13:14', '2025-07-07 00:30:26');
COMMIT;

-- ----------------------------
-- Table structure for datafilter
-- ----------------------------
DROP TABLE IF EXISTS `datafilter`;
CREATE TABLE `datafilter` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `datasetcode` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `code` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `cname` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `index` int NOT NULL DEFAULT '0',
  `meta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `status` tinyint NOT NULL DEFAULT '0',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of datafilter
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for datain
-- ----------------------------
DROP TABLE IF EXISTS `datain`;
CREATE TABLE `datain` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `meta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `stype` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `type` tinyint NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '0',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of datain
-- ----------------------------
BEGIN;
INSERT INTO `datain` (`id`, `code`, `meta`, `stype`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (1, 'workflow_db', '{\n  \"dev\":{\n      \"db_type\":\"mysql\",\n      \"db_host\":\"127.0.0.1\",\n      \"db_name\":\"python_data_api\",\n      \"db_port\":\"3306\",\n      \"db_user\":\"root\",\n      \"db_pwd\" :\"\"\n  },\n  \"prod\":{\n      \"db_type\":\"mysql\",\n      \"db_host\":\"127.0.0.1\",\n      \"db_name\":\"python_data_api\",\n      \"db_port\":\"3306\",\n      \"db_user\":\"root\",\n      \"db_pwd\" :\"\"\n  }\n}', 'mysql', '{{ADMIN_TOKEN}}', 0, 0, '2019-09-08 11:13:59', '2025-07-11 18:52:29');
COMMIT;

-- ----------------------------
-- Table structure for dataprop
-- ----------------------------
DROP TABLE IF EXISTS `dataprop`;
CREATE TABLE `dataprop` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `datasetcode` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `code` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `cname` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `index` int NOT NULL DEFAULT '0',
  `meta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `status` tinyint NOT NULL DEFAULT '0',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- ----------------------------
-- Table structure for dataset
-- ----------------------------
DROP TABLE IF EXISTS `dataset`;
CREATE TABLE `dataset` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `datain` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `datatable` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `code` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `cname` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `meta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `type` tinyint NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '0',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of dataset
-- ----------------------------
BEGIN;
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (1, 'workflow_db', 'inlog', 'workflow_inlog', '日志', NULL, '{{ADMIN_TOKEN}}', 0, 0, '2019-09-08 10:47:34', '2020-03-17 02:58:45');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (2, 'workflow_db', 'datain', 'workflow_datain', '数据源', NULL, '{{ADMIN_TOKEN}}', 0, 0, '2019-10-22 21:26:32', '2020-03-17 02:58:36');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (3, 'workflow_db', 'dataset', 'workflow_dataset', '数据集', NULL, '{{ADMIN_TOKEN}}', 0, 0, '2019-10-22 21:26:41', '2020-03-17 02:58:34');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (4, 'workflow_db', 'tree', 'workflow_tree', '元数据', '{}', '{{ADMIN_TOKEN}}', 0, 0, '2020-02-16 13:26:56', '2020-03-17 02:58:32');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (5, 'workflow_db', 'dataprop', 'workflow_dataprop', '数据字段', NULL, '{{ADMIN_TOKEN}}', 0, 0, '2020-02-24 01:29:25', '2020-03-17 02:58:31');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (11, 'workflow_db', 'datafilter', 'workflow_datafilter', '数据集过滤器', '{\n    \"index\":{\n        \"search\":[{\n            \"field\":\"meta\",\n            \"type\":\"like\"\n        }]\n    }\n}', '{{ADMIN_TOKEN}}', 0, 0, '2020-02-29 16:48:05', '2023-04-27 15:36:07');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (61, 'workflow_db', 'configbox', 'workflow_configbox', '配置盒', '{\n    \"list\" : {\n        \"search\":[\n            {\"type\":\"in\",\"field\":\"group\"}\n        ]\n    }\n}', '{{ADMIN_TOKEN}}', 0, 0, '2021-12-27 18:19:35', '2022-11-13 16:59:15');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (86, 'workflow_db', 'framebox', 'workflow_framebox', '结构盒', '{\n    \"list\" : {\n        \"search\":[\n            {\"type\":\"in\",\"field\":\"group\"}\n        ]\n    }\n}', '{{ADMIN_TOKEN}}', 0, 0, '2022-11-09 18:54:47', '2022-11-13 16:55:02');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (136, 'workflow_db', 'entity', 'workflow_entity', '单元实体', '{\n    \"list\" : {\n        \"search\":[\n            {\"type\":\"in\",\"field\":\"group\"}\n        ]\n    }\n}', '{{ADMIN_TOKEN}}', 0, 0, '2023-12-17 06:51:58', '2023-12-25 00:58:34');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (172, 'workflow_db', 'app', 'workflow_app', '', NULL, '{{ADMIN_TOKEN}}', 0, 0, '2025-07-09 18:33:39', '2025-07-09 18:33:39');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (176, 'workflow_db', 'user', 'workflow_user', '用户', NULL, '{{ADMIN_TOKEN}}', 0, 0, '2025-07-09 23:18:17', '2025-07-09 23:18:17');
INSERT INTO `dataset` (`id`, `datain`, `datatable`, `code`, `cname`, `meta`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (177, 'workflow_db', 'sms', 'workflow_sms', '注册短信', NULL, '{{ADMIN_TOKEN}}', 0, 0, '2025-07-10 02:23:45', '2025-07-10 02:23:45');
COMMIT;

-- ----------------------------
-- Table structure for entity
-- ----------------------------
DROP TABLE IF EXISTS `entity`;
CREATE TABLE `entity` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `group` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `name` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `prototypecode` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `meta` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `stype` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `type` tinyint NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '0',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`,`code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4473 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of entity
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for framebox
-- ----------------------------
DROP TABLE IF EXISTS `framebox`;
CREATE TABLE `framebox` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `group` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `parentid` bigint NOT NULL DEFAULT '0',
  `root` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `code` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `cname` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `relate` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `extend` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `meta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `index` int NOT NULL DEFAULT '0',
  `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `type` tinyint NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '0',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of framebox
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for inlog
-- ----------------------------
DROP TABLE IF EXISTS `inlog`;
CREATE TABLE `inlog` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `content` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `action` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `group` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `meta` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `type` tinyint NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '0',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;


-- ----------------------------
-- Table structure for sms
-- ----------------------------
DROP TABLE IF EXISTS `sms`;
CREATE TABLE `sms` (
  `mobile` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `code` smallint NOT NULL,
  `type` tinyint NOT NULL DEFAULT '0',
  `expiretime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`mobile`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of sms
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tree
-- ----------------------------
DROP TABLE IF EXISTS `tree`;
CREATE TABLE `tree` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `group` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `parentid` bigint NOT NULL DEFAULT '0',
  `code` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `cname` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `meta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `index` int NOT NULL DEFAULT '0',
  `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `createtoken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `type` tinyint NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '0',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of tree
-- ----------------------------
BEGIN;
INSERT INTO `tree` (`id`, `group`, `parentid`, `code`, `cname`, `desc`, `meta`, `index`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (22, 'datamanage', 0, 'workflow_datain', '数据源', '/app/datamanage?dataset=workflow_datain', 'fa-solid fa-database', 1, 'c46f9d71f3016b0eba84b2ebe67445f7', '{{ADMIN_TOKEN}}', 0, 0, '2020-02-16 03:05:07', '2025-07-11 11:27:57');
INSERT INTO `tree` (`id`, `group`, `parentid`, `code`, `cname`, `desc`, `meta`, `index`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (23, 'datamanage', 0, 'workflow_dataset', '数据集', '/app/datamanage?dataset=workflow_dataset', 'fa-solid fa-database', 2, 'b19905d787bbb78703b42f6c371a5d51', '{{ADMIN_TOKEN}}', 0, 0, '2020-02-16 03:05:47', '2025-07-11 11:28:14');
INSERT INTO `tree` (`id`, `group`, `parentid`, `code`, `cname`, `desc`, `meta`, `index`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (24, 'datamanage', 0, 'workflow_tree', '配置树', '/app/datamanage?dataset=workflow_tree', 'fa-solid fa-tree', 7, '8b3f99239128c83fc2af600a9403b0ed', '{{ADMIN_TOKEN}}', 0, 0, '2020-02-24 00:53:45', '2025-07-11 11:29:07');
INSERT INTO `tree` (`id`, `group`, `parentid`, `code`, `cname`, `desc`, `meta`, `index`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (25, 'datamanage', 0, 'workflow_dataprop', '字段配置', '/app/datamanage?dataset=workflow_dataprop', 'fa-solid fa-table', 3, 'ec9ad9a53b7c5d19f5ff1c28cd3b838c', '{{ADMIN_TOKEN}}', 0, 0, '2020-02-25 12:06:01', '2025-07-11 11:29:01');
INSERT INTO `tree` (`id`, `group`, `parentid`, `code`, `cname`, `desc`, `meta`, `index`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (26, 'datamanage', 0, 'workflow_datafilter', '过滤器', '/app/datamanage?dataset=workflow_datafilter', 'fa-solid fa-filter', 4, '10fd2712dd38bba0e4e24038547758a6', '{{ADMIN_TOKEN}}', 0, 0, '2020-03-01 16:17:05', '2025-07-11 11:29:15');
INSERT INTO `tree` (`id`, `group`, `parentid`, `code`, `cname`, `desc`, `meta`, `index`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (27, 'usercenter', 0, 'usercenter', '程序管理', '/app/usercenter', NULL, 1, 'c46f9d71f3016b0eba84b2ebe67445f7', '{{ADMIN_TOKEN}}', 0, 0, '2020-02-16 03:05:07', '2025-07-11 11:28:30');
INSERT INTO `tree` (`id`, `group`, `parentid`, `code`, `cname`, `desc`, `meta`, `index`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (28, 'datamanage', 0, 'workflow_configbox', '配置盒', '/app/datamanage?dataset=workflow_configbox', 'fa-solid fa-gear', 5, '9cc672f25238c16c34f7178e8babfe6e', '{{ADMIN_TOKEN}}', 0, 0, '2021-12-27 18:20:52', '2025-07-11 11:29:22');
INSERT INTO `tree` (`id`, `group`, `parentid`, `code`, `cname`, `desc`, `meta`, `index`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (29, 'datamanage', 0, 'workflow_framebox', '框架盒', '/app/datamanage?dataset=workflow_framebox', 'fa-solid fa-file-code', 6, '19e78820094f84976c5c91a60a425907', '{{ADMIN_TOKEN}}', 0, 0, '2022-11-09 19:22:55', '2025-07-11 11:29:28');
INSERT INTO `tree` (`id`, `group`, `parentid`, `code`, `cname`, `desc`, `meta`, `index`, `token`, `createtoken`, `type`, `status`, `createtime`, `updatetime`) VALUES (30, 'datamanage', 0, 'workflow_entity', '实体单元', '/app/datamanage?dataset=workflow_entity', 'fa-solid fa-inbox', 8, '62f0c43e0cd80d50898533e55321f167', '{{ADMIN_TOKEN}}', 0, 0, '2023-12-17 06:52:46', '2025-07-11 11:29:33');
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `nick` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `gender` tinyint NOT NULL DEFAULT '0',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `birthday` timestamp NULL DEFAULT NULL,
  `pwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mobile` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `aboutme` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `incode` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `expiretime` timestamp NULL DEFAULT NULL,
  `meta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `type` tinyint NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '0',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` (`id`, `name`, `nick`, `gender`, `avatar`, `birthday`, `pwd`, `mobile`, `token`, `aboutme`, `incode`, `expiretime`, `meta`, `type`, `status`, `createtime`, `updatetime`) VALUES (1, 'admin123', '管理员', 0, '/assets/images/avatar.jpg', NULL, '21232f297a57a5a743894a0e4a801fc3', '', '{{ADMIN_TOKEN}}', '', '7e16a7bdf20fd9a5906df902519c2448', '2025-07-12 19:02:00', '', 1, 0, '2018-02-21 23:33:47', '2025-07-11 19:06:49');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
